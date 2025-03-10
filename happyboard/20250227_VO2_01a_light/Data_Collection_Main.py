VERSION = "VO2.01a_light"

import micropython
print("Debugger:[Data_Collection_Main] 首行，記憶體:")
micropython.mem_info()
#標準庫
import os
import utime
import gc
import _thread
import ujson
#外部依賴
from machine import UART, Timer, WDT
from umqtt.simple import MQTTClient
#本地
from uart_handler import UartHandler
from uart_manager import UartManager
from mqtt_manager import MqttManager
from timer_manager import TimerManager
from received_claw_data import ReceivedClawData

# =============================
# 定義狀態類型
# =============================
# print(f"wifi_manager: {wifi_manager}")
# print(f"network_info:{network_info},{wifi_manager.ssid}")
# =============================
# 定義狀態類型
class MainStatus:
    NONE_WIFI = 0       # 還沒連上WiFi
    NONE_INTERNET = 1   # 連上WiFi，但還沒連上外網      現在先不做這個判斷
    NONE_MQTT = 2       # 連上外網，但還沒連上MQTT Broker
    NONE_FEILOLI = 3    # 連上MQTT，但還沒連上FEILOLI娃娃機
    STANDBY_FEILOLI = 4 # 連上FEILOLI娃娃機，正常運行中
    WAITING_FEILOLI = 5 # 連上FEILOLI娃娃機，等待娃娃機回覆
    GOING_TO_OTA = 6    # 接收到要OTA，但還沒完成OTA
    UNEXPECTED_STATE = -1

# =============================
# 定義狀態類型 (狀態機)
# =============================
class MainStateMachine:
    def __init__(self):
        self.state = MainStatus.NONE_WIFI
        # 
        self.LCD_update_flag = {
            'Uniform': True,
            'WiFi': False,
            'Time': False,
            'Claw_State': False,
            'Claw_Value': False
        }

        self.main_while_delay_seconds = 1
        print('[MainStateMachine] 初始化: NONE_WIFI')

    def transition(self, action): 
        # 把if-else變成字典映射{ action: MainStatus.state}
        state_map = {
            'WiFi is disconnect': MainStatus.NONE_WIFI,
            'WiFi is OK': MainStatus.NONE_INTERNET,
            'Internet is OK': MainStatus.NONE_MQTT,
            'MQTT is OK': MainStatus.NONE_FEILOLI,
            'FEILOLI UART is OK': MainStatus.STANDBY_FEILOLI,
            'FEILOLI UART is waiting': MainStatus.WAITING_FEILOLI,
            'FEILOLI UART is not OK': MainStatus.NONE_FEILOLI,
            'MQTT is not OK': MainStatus.NONE_MQTT,
        }

        #這裡做if-else邏輯
        if action in state_map:
            #根據當前的action映射state
            self.state = state_map[action]
            print(f"[Action]: {action}, [MainStatus]: {self.state}")

            self.main_while_delay_seconds = 10 if 'FEILOLI' in action or 'MQTT' in action else 1

            if 'WiFi' in action or 'MQTT' in action:
                self.LCD_update_flag['WiFi'] = True
            
            if 'FEILOLI' in action:
                self.LCD_update_flag['Claw_State'] = True
        else:
            print(f"[Invalid action]: {action}, 當前狀態", {self.state})
            self.main_while_delay_seconds = 1

def get_file_info(filename):
    try:
        file_stat = os.stat(filename)
        file_size = file_stat[6]  # Index 6 is the file size
        file_mtime = file_stat[8]  # Index 8 is the modification time
        return file_size, file_mtime
    except OSError:
        return None, None

class KindFEILOLIcmd:
    Ask_Machine_status = 210
    Send_Machine_reboot = 215
    Send_Machine_shutdown = 216
    Send_Payment_countdown_Or_fail = 231
    #     Send_Starting_games = 220
    Send_Starting_once_game = 221
    Ask_Transaction_account = 321 # 查詢:遠端帳目
    #Ask_Coin_account = 322 # 查詢:投幣帳目
    
    Send_Clean_transaction_account = 323 # 清除:遠端帳目
    #Clean_Coin_account = 324 ## 清除:投幣帳目
    Ask_Machine_setting = 431


#############################################初始化
# =============================
# 初始化硬體與網路
# =============================
#############################################
def initialize():
    print(f"\n[Data_Collection_Main]: 開始執行Data_Collection_Main初始化，版本為: {VERSION}")
    
    print(f"開機秒數: {utime.ticks_ms() / 1000}")

    wdt=WDT(timeout=1000*60*10)

    # 創建狀態機
    now_main_state = MainStateMachine()

    # 創建娃娃機資料
    claw_1 = ReceivedClawData()

    # 創建 MQTT Client 1 資料
    mq_client_1 = None

    uart_handler = UartHandler(claw_1, None, now_main_state.LCD_update_flag, now_main_state) # 但先不設定 mqtt_handler=None
    uart_manager = UartManager(claw_1=claw_1,
    KindFEILOLIcmd=KindFEILOLIcmd,
    uart_handler=uart_handler,
    mqtt_handler=None)

    mqtt_manager = MqttManager(
    mac_id=network_info["mac"],
    claw_1=claw_1,
    KindFEILOLIcmd=KindFEILOLIcmd,
    version=VERSION,
    wifi_manager=wifi_manager,
    uart_manager=uart_manager,
    LCD_update_flag=now_main_state.LCD_update_flag
    ) #並在其中建立 mqtt_handler()

    mqtt_handler = mqtt_manager.mqtt_handler  # 直接用 `MqttManager` 內建的 `MqttHandler`

    # 已有了mqtt_handler，設定 MQTT Handler 到 UART Manager
    uart_manager.mqtt_handler = mqtt_handler

    # 已有了mqtt_handler，設定 MQTT Handler 到 UART Handler
    uart_handler.mqtt_handler = mqtt_handler

    # 已有了uart_manager，，設定 UART Manager 到 MQTT Manager
    mqtt_manager.uart_manager = uart_manager

    timer_manager = TimerManager(now_main_state, MainStatus, wifi_manager, uart_manager, mqtt_manager, mqtt_handler, lcd_mgr, wdt, now_main_state.LCD_update_flag, claw_1)

    gc.collect()

    # 啟動 UART 執行緒
    _thread.stack_size(16 * 1024)
    _thread.start_new_thread(uart_manager.receive_packet, ())

    utime.sleep(2)
    timer_manager.start_timers()

    return now_main_state, mqtt_manager, wifi_manager, network_info

    
# =============================
# 主迴圈
# =============================
def run_data_collection_main_loop(now_main_state, mqtt_manager, wifi_manager, network_info):
    last_time = 0

    while True:
        utime.sleep_ms(500)
        current_time = utime.ticks_ms()

        if utime.ticks_diff(current_time, last_time) >= now_main_state.main_while_delay_seconds * 1000:
            last_time = current_time

            # WiFi 檢查與自動重連
            if now_main_state.state == MainStatus.NONE_WIFI:
                print(f"[now_main_state]: WiFi is disconnect, 開機秒數: { current_time / 1000}")

                print(f'[IP]: {network_info["ip"]}\n[MAC]: {network_info["mac"]}')
                now_main_state.transition('WiFi is OK')

            elif now_main_state.state == MainStatus.NONE_INTERNET:
                print(f"\n\r[now_main_state]: WiFi is OK, 開機秒數: { current_time} / 1000")
                now_main_state.transition('Internet is OK')

            elif now_main_state.state == MainStatus.NONE_MQTT:
                print(f"\n\r[now_main_state]: Internet is OK, 開機秒數: {current_time / 1000}")
                mqtt_manager.connect_mqtt()

                if mqtt_manager.client:
                    now_main_state.transition('MQTT is OK')
                else:
                    print('\n\r[now_main_state]: MQTT Client is None,subscription has failed')
                gc.collect()

            elif now_main_state.state == MainStatus.NONE_FEILOLI:
                print(f"\n\r[now_main_state]: MQTT is OK (FEILOLI UART is not OK), 開機秒數: {current_time / 1000}")   

            elif now_main_state.state == MainStatus.STANDBY_FEILOLI:
                print('\n\r[now_main_state]: FEILOLI UART is OK, 開機秒數:', current_time / 1000)
                #print('[FEILOLI] UART 運行正常')

            elif now_main_state.state == MainStatus.WAITING_FEILOLI:
                print('\n\r[now_main_state]: FEILOLI UART is witing, 開機秒數:', current_time / 1000)
                #print('[FEILOLI] UART 等待中')
            else:
                print(f"\n\r[Invalid action] ==> [now_main_state]: {now_main_state.state}, 開機秒數: {current_time / 1000}")

            now_main_state.LCD_update_flag['Time'] = True
            gc.collect()

print("Debugger:[__name__=__main__] ，記憶體:")
micropython.mem_info()

if __name__ == "__main__":
    now_main_state, mqtt_manager, wifi_manager, network_info = initialize()
    run_data_collection_main_loop(now_main_state, mqtt_manager, wifi_manager, network_info)