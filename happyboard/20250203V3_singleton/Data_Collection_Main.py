VERSION = "V1.07b5_sui"
# [待整合]: Data_Collection_Main.py還是需要繼續優化記憶體 接下來繼續新增功能 仍然會容易出現memory error (這就是micropython.mem_info()所顯示出的max free size有關)
## 雖然透過gc.collect()可以將一些記憶體釋出,但是當全域變數所佔用的記憶體是{連續一整塊的max free size},這種最大連續內存是很難從gc釋出全部 ---> 內存碎片化的意思 <--- 
# -----------------------------------------------------
# test V1.07b5_sui  # 將mqtt中publish_mqtt_clawdata拆解為mqtt_helper.py
# --------------------------------------------------------
# test V1.07b4_sui 不使用單例模式 st7735 模組
# --------------------------------------------------------
# test V1.07b3_sui  # 將ST7735模組抽離lcd_manager為單例模式/唯一實例
# test V1.07b2_sui  # 四 機台設定查詢:  加入抓力電壓 
# test V1.07b2_sui  # 四 機台設定查詢:  拆模組ReceivedClawData&整理模組
# test V1.07b1_sui  # 更改了startoncegame的參數 可以透過mqtt從遠端發送ep:1-40 FP(Giftplaytimes):1-10的數值
# test V1.07b0_sui  # 一鍵清除sales內容 or 單一清除
import micropython
micropython.mem_info()
#標準庫
#import binascii
import os
import utime
import gc
import _thread
import ujson
#外部依賴
from machine import UART, Timer, WDT
#from machine import UART, Pin, SPI, Timer, WDT
from umqtt.simple import MQTTClient
#本地
from received_claw_data import ReceivedClawData

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


# 定義狀態機類別
class MainStateMachine:

    def __init__(self):
        self.state = MainStatus.NONE_WIFI
        # 以下執行"狀態機初始化"相應的操作
        print('\n\rInit, MainStatus: NONE_WIFI')
        global main_while_delay_seconds, LCD_update_flag
        main_while_delay_seconds = 1
        LCD_update_flag['Uniform'] = True

    def transition(self, action):
        global main_while_delay_seconds, LCD_update_flag
        if action == 'WiFi is disconnect':
            self.state = MainStatus.NONE_WIFI
            # 以下執行"未連上WiFi後"相應的操作
            print('\n\rAction: WiFi is disconnect, MainStatus: NONE_WIFI')
            main_while_delay_seconds = 1
            LCD_update_flag['WiFi'] = True

        elif self.state == MainStatus.NONE_WIFI and action == 'WiFi is OK':
            self.state = MainStatus.NONE_INTERNET
            # 以下執行"連上WiFi後"相應的操作
            print('\n\rAction: WiFi is OK, MainStatus: NONE_INTERNET')
            main_while_delay_seconds = 1
            LCD_update_flag['WiFi'] = True

        elif self.state == MainStatus.NONE_INTERNET and action == 'Internet is OK':
            self.state = MainStatus.NONE_MQTT
            # 以下執行"連上Internet後"相應的操作
            print('\n\rAction: Internet is OK, MainStatus: NONE_MQTT')
            main_while_delay_seconds = 1
            LCD_update_flag['WiFi'] = True

        elif self.state == MainStatus.NONE_MQTT and action == 'MQTT is OK':
            self.state = MainStatus.NONE_FEILOLI
            # 以下執行"連上MQTT後"相應的操作
            print('\n\rAction: MQTT is OK, MainStatus: NONE_FEILOLI')
            main_while_delay_seconds = 10
            LCD_update_flag['WiFi'] = True
            LCD_update_flag['Claw_State'] = True

        elif (self.state == MainStatus.NONE_FEILOLI or self.state == MainStatus.WAITING_FEILOLI) and action == 'FEILOLI UART is OK':
            self.state = MainStatus.STANDBY_FEILOLI
            # 以下執行"連上FEILOLI娃娃機後"相應的操作
            print('\n\rAction: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI')
            main_while_delay_seconds = 10
            LCD_update_flag['Claw_State'] = True

        elif self.state == MainStatus.STANDBY_FEILOLI and action == 'FEILOLI UART is waiting':
            self.state = MainStatus.WAITING_FEILOLI
            # 以下執行"等待FEILOLI娃娃機後"相應的操作
            print('\n\rAction: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI')
            main_while_delay_seconds = 10

        elif self.state == MainStatus.WAITING_FEILOLI and action == 'FEILOLI UART is not OK':
            self.state = MainStatus.NONE_FEILOLI
            # 以下執行"等待失敗後"相應的操作
            print('\n\rAction: FEILOLI UART is not OK, MainStatus: NONE_FEILOLI')
            main_while_delay_seconds = 10    
            LCD_update_flag['Claw_State'] = True

        elif (self.state == MainStatus.NONE_FEILOLI or self.state == MainStatus.STANDBY_FEILOLI or self.state == MainStatus.WAITING_FEILOLI) and action == 'MQTT is not OK':
            self.state = MainStatus.NONE_MQTT
            # 以下執行"MQTT失敗後"相應的操作
            print('\n\rAction: MQTT is not OK, MainStatus: NONE_MQTT')
            main_while_delay_seconds = 1
            LCD_update_flag['WiFi'] = True

        else:
            print('\n\rInvalid action:', action, 'for current state:', self.state)
            main_while_delay_seconds = 1
 
# 開啟 token 檔案
def load_token():
    global token
    try:
        with open('token.dat') as f:
            token = f.readlines()[0].strip()
        print('Get token:', token)
        len_token = len(token)
        if len_token != 36:
            while True:
                print('token的長度不對:', len_token)
                utime.sleep(30)
    except Exception as e:
        print("Open token.dat failed:", e)
        while True:
            print('遺失 token 檔案')
            utime.sleep(30)


def get_wifi_signal_strength(wlan):
    if wlan.isconnected():
        signal_strength = wlan.status('rssi')
        return signal_strength
    else:
        return None


def connect_wifi():
    global wifi
    wifi = network.WLAN(network.STA_IF)

    if not wifi.config('essid'):
        print('沒有經過wifimgr.py')
        wifi_ssid = 'paypc'
        wifi_password = 'abcd1234'
        wifi.active(True)
        wifi.connect(wifi_ssid, wifi_password)

    print('Start to connect WiFi, SSID : {}'.format(wifi.config('essid')))

    while True:
        for i in range(20):
            print('Try to connect WiFi in {}s'.format(i))
            utime.sleep(1)
            if wifi.isconnected():
                break
        if wifi.isconnected():
            print('WiFi connection OK!')
            print('Network Config=', wifi.ifconfig())
            connect_internet_data = InternetData()
            connect_internet_data.ip_address = wifi.ifconfig()[0]
            tmp_mac_address = wifi.config('mac')
            connect_internet_data.mac_address = ''.join(['{:02X}'.format(byte) for byte in tmp_mac_address])
            return connect_internet_data
        else:
            print('WiFi({}) connection Error'.format(wifi.config('essid')))
            for i in range(30, -1, -1):
                print("倒數{}秒後重新連線WiFi".format(i))
                utime.sleep(1)


class InternetData:
    def __init__(self):
        self.ip_address = ""
        self.mac_address = ""


def connect_mqtt():
    mq_server = 'happycollect.propskynet.com'
    mq_id = my_internet_data.mac_address
    mq_user = 'myuser'
    mq_pass = 'propskymqtt'
    while True:
        try:
            #建立MQTTClient用戶端物件
            mq_client = MQTTClient(mq_id, mq_server, user=mq_user, password=mq_pass)
            #連接MQTT SERVER
            mq_client.connect()
            print('MQTT Broker connection OK!')
            return mq_client
        except Exception as e:
            print("MQTT Broker connection failed:", e)
            for i in range(10, -1, -1):
                print("倒數{}秒後重新連線MQTT Broker".format(i))
                utime.sleep(1)




def subscribe_MQTT_claw_recive_callback(topic, message):
    """
    MQTT Subscribe 回調函式。
    處理接收到的 topic 和 message，並調用對應的邏輯。
    """
    print("MQTT Subscribe recive data")
    print("MQTT Subscribe topic:", topic)
    print("MQTT Subscribe data(JSON_str):", message)

    try:
        # 解碼訊息
        data = ujson.loads(message)
        print("MQTT Subscribe data (parsed):", data)

        # 獲取 topic 前綴
        macid = my_internet_data.mac_address
        mq_topic_prefix = f"{macid}/{token}"

        # 分派邏輯
        if topic.decode() == f"{mq_topic_prefix}/fota":
            from mqtt_helper import process_fota
            process_fota(data, publish_MQTT_claw_data, claw_1)

        #這裡要處理的傳入參數比較多
        elif topic.decode() == f"{mq_topic_prefix}/commands":
            from mqtt_helper import process_commands
            process_commands(data, publish_MQTT_claw_data, uart_FEILOLI_send_packet, claw_1, KindFEILOLIcmd)
        else:
            print(f"Unknown topic received: {topic.decode()}")

    except ValueError as ve:
        print(f"JSON decode error: {ve}")
    except Exception as e:
        print(f"Error in MQTT callback: {e}")



 # 設定接收MQTT訊息的回呼函式.set_callback(fn_CALLBACK)
    # ==>有新訊息時 會自動執行這個 callback執行這個 callback
    #下面這個callback 只接受兩個參數topic和msg
# def subscribe_MQTT_claw_recive_callback(topic, message):
#     print("MQTT Subscribe recive data")
#     print("MQTT Subscribe topic:", topic)
#     print("MQTT Subscribe data(JSON_str):", message)
#     try:
#         data = ujson.loads(message)
#         print("MQTT Subscribe data:", data)

#         macid = my_internet_data.mac_address
#         mq_topic = macid + '/' + token
#         if topic.decode() == (mq_topic + '/fota'):
#             otafile = 'otalist.dat'
#             if ('file_list' in data) and ('password' in data):
#                 if data['password'] == 'c0b82a2c-4b03-42a5-92cd-3478798b2a90':
#                     #print("password checked")
#                     publish_MQTT_claw_data(claw_1, 'fotaack')                    
#                     with open(otafile, "w") as f:
#                         f.write(''.join(data['file_list']))
#                     print("otafile 輸出完成，即將重開機...")
#                     utime.sleep(3)
#                     reset()
#                 else:
#                     print("password failed")
#         elif topic.decode() == (mq_topic + '/commands'):
#             if data['commands'] == 'ping':
#                 publish_MQTT_claw_data(claw_1, 'commandack-pong')
#             elif data['commands'] == 'version':
#                 publish_MQTT_claw_data(claw_1, 'commandack-version')
#             elif data['commands'] == 'clawreboot':
#                 if 'state' in data:
#                     publish_MQTT_claw_data(claw_1, 'commandack-clawreboot',data['state'])
#                     uart_FEILOLI_send_packet(KindFEILOLIcmd.Send_Machine_reboot)
#                 # else:
#                 #     publish_MQTT_claw_data(claw_1, 'commandack-clawreboot')
#                 #     uart_FEILOLI_send_packet(KindFEILOLIcmd.Send_Machine_reboot)
#             elif data['commands'] == 'clawstartgame':
#                 if 'state' in data:
#                     publish_MQTT_claw_data(claw_1, 'commandack-clawstartgame',data['state'])
#                     # 提取mqtt 傳送來的epays 和freeplays值並驗證參數範圍
#                     epays = data.get('epays', None)
#                     freeplays = data.get('freeplays', None)
#                     # 將接收mqtt server的指令轉為dict(啟動次數 與 贈局數)
#                     if not (1 <= epays <= 40):
#                         raise ValueError(f"錯誤的epays值: {epays} 範圍在1~40")
#                     if not (0 <= freeplays <= 10):
#                         raise ValueError(f"錯誤的freeplays值: {freeplays} 範圍在0~10")
                    
#                     # 將 epays 和 freeplays 組成參數物件
#                     clawstartgamesitem = {
#                         "epays": epays,
#                         "freeplays": freeplays
#                     }
#                     # 調用 UART 發送遊戲啟動指令 帶參數或不帶參數
#                     uart_FEILOLI_send_packet(KindFEILOLIcmd.Send_Starting_once_game, clawstartgamesitem)
#             elif data['commands'] == 'clawcleantransaccount':
#                 if 'state' in data and 'account' in data:
#                     clawcleanitems = data['account'].split(', ')  # 將接收的account項目轉為list
#                     publish_MQTT_claw_data(claw_1, 'commandack-clawcleantransaccount', data['state'])
#                     # 統一把mqtt驅動傳過來的account內容 組成list 變成參數 傳送封包那裏再做判斷 這裡簡化處理
#                     uart_FEILOLI_send_packet(KindFEILOLIcmd.Send_Clean_transaction_account, clawcleanitems)
#             #機台設定:抓力電壓
#             elif data['commands'] == 'clawmachinesetting':  
#                 if 'setting' in data:
#                     clawsettingitem = data['setting'].strip()  # 取得單一的設定項目
                    
#                     valid_settings = ["BasicsettingA", "BasicsettingB", "BasicsettingC", "Clawvoltage", "Motorspeed"]
                    
#                     if clawsettingitem in valid_settings:           
#                         # 發送 UART 指令
#                         uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Machine_setting, clawsettingitem)
#                     else:
#                         # 無效的設定項目
#                         print(f"Invalid setting received: {clawsettingitem}")
#                         # # 發布 MQTT 訊息 =>改寫到收到娃娃機封包回傳再上傳
#                         # publish_MQTT_claw_data(claw_1, 'commandack-clawclaw', clawsettingitem)
#                 else:
#                     print("Missing 'setting' field in the received data") 
#             elif data['commands'] == 'fileinfo':
#                 publish_MQTT_claw_data(claw_1, 'commandack-fileinfo',data['filename'])
#                 pass
#             elif data['commands'] == 'fileremove':
#                 publish_MQTT_claw_data(claw_1, 'commandack-fileremove',data['filename'])
#                 pass

#     #       elif data['commands'] == 'getstatus':

#     except Exception as e:
#         print("MQTT Subscribe data to JSON Error:", e)

def subscribe_MQTT_claw_topic():  # MQTT_client暫時固定為mq_client_1
    # 設定接收MQTT訊息的回呼函式.set_callback(fn_CALLBACK)
    # ==>有新訊息時 會自動執行這個 callback執行這個 callback
    mq_client_1.set_callback(subscribe_MQTT_claw_recive_callback)
    macid = my_internet_data.mac_address

    # 訂閱 Commands 主題
    command_topic = f"{macid}/{token}/commands"
    mq_client_1.subscribe(command_topic)
    print("MQTT Subscribe topic:", command_topic)

    # 訂閱 FOTA 主題
    fota_topic = f"{macid}/{token}/fota"
    mq_topic = mq_client_1.subscribe(fota_topic)
    print("MQTT Subscribe topic:", fota_topic)

def publish_data(mq_client, topic, data):
    try:
        # mq_message = ujson.dumps(data)
        print("MQTT Publish topic:", topic)
        print("MQTT Publish data(JSON_str):", data)
        mq_client.publish(topic, data)
        print("MQTT Publish Successful")
    except Exception as e:
        print("MQTT Publish Error:", e)
        now_main_state.transition('MQTT is not OK')

def get_file_info(filename):
    try:
        file_stat = os.stat(filename)
        file_size = file_stat[6]  # Index 6 is the file size
        file_mtime = file_stat[8]  # Index 8 is the modification time
        return file_size, file_mtime
    except OSError:
        return None, None
    
def publish_MQTT_claw_data(claw_1, MQTT_API_select, para1=""):
    """
    根據 MQTT_API_select 執行不同的 MQTT 發布邏輯。
    """
    global wifi,VERSION
    macid = my_internet_data.mac_address
    mq_topic = f"{macid}/{token}/{MQTT_API_select}"

    # 使用 mqtt_helper 中的函數生成對應的數據
    if MQTT_API_select == "sales":
        from mqtt_helper import build_sales_data
        MQTT_claw_data = build_sales_data(claw_1)

    elif MQTT_API_select == "status":#沒效果
        from mqtt_helper import build_status_data
        # 需要將 WiFi 的 RSSI 信號作為參數傳入
        wifi_signal = get_wifi_signal_strength(wifi)
        MQTT_claw_data = build_status_data(claw_1, wifi_signal)

    elif MQTT_API_select == "commandack-clawmachinesetting":
        from mqtt_helper import build_clawmachinesetting_data
        MQTT_claw_data = build_clawmachinesetting_data(claw_1, para1)

    elif MQTT_API_select == "commandack-fileinfo":
        from mqtt_helper import build_fileinfo_data
        MQTT_claw_data = build_fileinfo_data(para1)

    elif MQTT_API_select == "commandack-fileremove":
        from mqtt_helper import build_fileremove_data
        MQTT_claw_data = build_fileremove_data(para1)
    
    elif MQTT_API_select.startswith("commandack"):
        from mqtt_helper import handle_ack_with_state
        MQTT_claw_data = handle_ack_with_state(MQTT_API_select, para1, version=VERSION)

    else:
        print(f"未處理的 MQTT_API_select: {MQTT_API_select}")
        return  # 結束函式執行

    # 發布資料到 MQTT
    if MQTT_claw_data:
        mq_json_str = ujson.dumps(MQTT_claw_data)
        try:
            publish_data(mq_client_1, mq_topic, mq_json_str)
            MQTT_claw_data.clear()  # 清除字典節省內存
            gc.collect()  # 強制執行垃圾回收
        except Exception as e:
            print(f"MQTT 發布失敗: {e}")



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


# 发送封包給娃娃機的副程式
FEILOLI_packet_id = 0

# 機台設定封包:index[4]
clawsettingdict = {
    "BasicsettingA": 0x00,
    "BasicsettingB": 0x01,
    "BasicsettingC": 0x02,
    "Clawvoltage": 0x03,#抓力電壓
    "Motorspeed": 0x04,
}

def uart_FEILOLI_send_packet(FEILOLI_cmd, new_parameters=None):
    global FEILOLI_packet_id, clawsettingdict
    FEILOLI_packet_id = (FEILOLI_packet_id + 1) % 256
    if FEILOLI_cmd == KindFEILOLIcmd.Ask_Machine_status:
        uart_send_packet = bytearray([0xBB, 0x73, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, FEILOLI_packet_id, 0x00, 0xAA])
    elif FEILOLI_cmd == KindFEILOLIcmd.Send_Machine_reboot:
        uart_send_packet = bytearray([0xBB, 0x73, 0x01, 0x01, 0x05, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, FEILOLI_packet_id, 0x00, 0xAA])
    elif FEILOLI_cmd == KindFEILOLIcmd.Send_Machine_shutdown:
        pass
    elif FEILOLI_cmd == KindFEILOLIcmd.Send_Payment_countdown_Or_fail:
        pass
    elif FEILOLI_cmd == KindFEILOLIcmd.Send_Starting_once_game:
        # 初始化遊戲啟動封包
        uart_send_packet = bytearray([
            0xBB, 0x73, 0x01, 0x02, 0x01, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, FEILOLI_packet_id, 0x00, 0xAA
        ])

        # 如果沒有帶入參數是None，遊戲啟動一次
        if new_parameters is None:
            uart_send_packet[5] = 0x01  # 默認啟動次數1次
        else:
            # 定義啟動次數 啟動贈局數 與封包index對應
            clawitems_positions = {
                'epays': 5,       # 啟動次數對應封包索引
                'freeplays': 6    # 贈局數對應封包索引
            }
            for key, value in new_parameters.items():
                if key in clawitems_positions:
                    uart_send_packet[clawitems_positions[key]] = value
                    
    elif FEILOLI_cmd == KindFEILOLIcmd.Ask_Transaction_account: #查詢:遠端帳目
        uart_send_packet = bytearray([0xBB, 0x73, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00, 0x00, FEILOLI_packet_id, 0x00, 0xAA])
    elif FEILOLI_cmd == KindFEILOLIcmd.Send_Clean_transaction_account: #清除:遠端帳目
        # 初始化封包:以下是查詢:遠端帳目封包 只要是清除 該封包的位置就會是0x01 
        uart_send_packet = bytearray([
            0xBB, 0x73, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, FEILOLI_packet_id, 0x00, 0xAA
        ])

        # 定義帳目與封包index對應
        clawcleanitems_positions = {
            'Epayplaytimes': 5,
            'Giftplaytimes': 7,
            'Coinplaytimes': 9,
            'GiftOuttimes': 11,
        }

        if new_parameters is None or set(new_parameters) == set(clawcleanitems_positions.keys()):
            # 全部清除
            ## 取出clawcleanitems_positions中定義的key值對應封包index
            for pos in clawcleanitems_positions.values():
                #將該封包對應的index位置 寫入0x01代表清除該項目
                uart_send_packet[pos] = 0x01
        else:
            # 部分清除(從MQTT驅動過來 傳入的參數)
            for item in new_parameters:
                # 比對clawcleanitems_positions的key
                if item in clawcleanitems_positions:
                    #透過key取得封包index 來寫入清除的cmd 0x01
                    uart_send_packet[clawcleanitems_positions[item]] = 0x01
                else:
                    print(f"未知的封包清除項目: {item}")
    #機台設定
    elif FEILOLI_cmd == KindFEILOLIcmd.Ask_Machine_setting: 
        if new_parameters:
            clawsettingitem = new_parameters
            uart_send_packet = bytearray([0xBB, 0x73, 0x03, 0x01, clawsettingdict[clawsettingitem], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, FEILOLI_packet_id, 0x00, 0xAA])
    if uart_send_packet[13] == FEILOLI_packet_id:
        for i in range(2, 14):
            uart_send_packet[15] ^= uart_send_packet[i]
        uart_FEILOLI.write(uart_send_packet)
        print("Sent packet to 娃娃機:    ", ''.join(['{:02X} '.format(byte) for byte in uart_send_packet]))
    else:
        print("FEILOLI_cmd 是無效的指令:", FEILOLI_cmd)


# 定義最大佇列容量
# MAX_RX_QUEUE_SIZE = 200
# 建立佇列
uart_FEILOLI_rx_queue = []

# 從佇列中讀取資料的任務
def uart_FEILOLI_recive_packet_task():
    global claw_1, uart_FEILOLI, clawsettingdict
    while True:
        if uart_FEILOLI.any():
            receive_data = uart_FEILOLI.readline()
            uart_FEILOLI_rx_queue.extend(receive_data)
            while len(uart_FEILOLI_rx_queue) >= 16:
                #                 print("uart_FEILOLI_rx_queue:", bytearray(uart_FEILOLI_rx_queue))
                uart_recive_packet = bytearray(16)
                uart_recive_packet[0] = uart_FEILOLI_rx_queue.pop(0)  # 從佇列中取出第一個字元
                if uart_recive_packet[0] == 0x2D:
                    uart_recive_packet[1] = uart_FEILOLI_rx_queue.pop(0)  # 從佇列中取出下一個字元
                    if uart_recive_packet[1] == 0x8A:
                        uart_recive_check_sum = 0xAA
                        for i in range(2, 16):
                            uart_recive_packet[i] = uart_FEILOLI_rx_queue.pop(0)
                            uart_recive_check_sum ^= uart_recive_packet[i]
                        if uart_recive_check_sum == 0x00:  # check sum算完正確，得到正確16Byte
                            print("Recive packet from 娃娃機:", uart_recive_packet)
                            ######################  在這裡進行packet的處理  ############################################
                            if uart_recive_packet[2] == 0x81 and uart_recive_packet[3] == 0x01:                 # CMD => 二、主控制\機台狀態
                                claw_1.CMD_Control_Machine = uart_recive_packet[4]                                  # 回覆控制指令 (機台回覆控制代碼)
                                claw_1.Status_of_Current_machine[0] = uart_recive_packet[5]                         # 機台目前狀況
                                claw_1.Status_of_Current_machine[1] = uart_recive_packet[6]                         # 機台目前狀況
                                claw_1.Time_of_Current_game = uart_recive_packet[7]                                 # 當機台目前狀況[0]為0x10=遊戲開始(未控制搖桿)時，回傳的遊戲時間
                                claw_1.Game_amount_of_Player = uart_recive_packet[8] * 256 + uart_recive_packet[9]  # 玩家遊戲金額(累加金額)
                                claw_1.Way_of_Starting_game = uart_recive_packet[10]                                # 遊戲啟動方式
                                claw_1.Cumulation_amount_of_Sale_card = uart_recive_packet[11] * 256 + uart_recive_packet[14]  # 售價小卡顯示用累加金額
                                claw_1.Error_Code_of_Machine = uart_recive_packet[12]                   # 六、 機台故障代碼表
                                print("Recive 娃娃機 : 二、主控制\機台狀態")
                            elif uart_recive_packet[2] == 0x82 and uart_recive_packet[3] == 0x01:               # CMD => 三、 帳目查詢\遠端帳目
                                claw_1.Number_of_Original_Payment = uart_recive_packet[4] * 256 + uart_recive_packet[5]     # 悠遊卡支付次數
                                claw_1.Number_of_Gift_Payment = uart_recive_packet[6] * 256 + uart_recive_packet[7]         # 悠遊卡贈送次數
                                claw_1.Number_of_Coin = uart_recive_packet[8] * 256 + uart_recive_packet[9]                 # 投幣次數
                                claw_1.Number_of_Award = uart_recive_packet[10] * 256 + uart_recive_packet[11]              # 禮品出獎次數
                                claw_1.Error_Code_of_Machine = uart_recive_packet[12]                   # 六、 機台故障代碼表
                                print("Recive 娃娃機 : 三、 帳目查詢=>遠端帳目")     
                            # 機台設定
                            elif uart_recive_packet[2] == 0x83:
                                cmd = uart_recive_packet[3]
                                #反向查詢 透過封包查找到命令名稱
                                setting_name = {v: k for k,v in clawsettingdict.items()}.get(cmd)

                                if setting_name == "Clawvoltage": # CMD => 四、 機台設定\抓力電壓
                                    claw_1.Value_of_Hi_voltage = uart_recive_packet[4] * 0.2
                                    claw_1.Value_of_Mid_voltage = uart_recive_packet[5] * 0.2
                                    claw_1.Value_of_Lo_voltage = uart_recive_packet[6] * 0.2
                                    claw_1.Distance_of_Mid_voltage_and_Top = uart_recive_packet[7] 
                                    claw_1.Hi_voltage_of_Guaranteed_prize = uart_recive_packet[8] * 0.2 
                                    claw_1.Error_Code_of_Machine = uart_recive_packet[12]                   # 六、 機台故障代碼表
                                    print("Recive 娃娃機: 四、機台設定\抓力電壓") 
                                # 發布 MQTT 訊息(可以確定判斷式統一發布)
                                elif setting_name == "Motorspeed":
                                    claw_1.Speed_of_Moving_forward = uart_recive_packet[4]
                                    claw_1.Speed_of_Moving_back = uart_recive_packet[5]
                                    claw_1.Speed_of_Moving_left = uart_recive_packet[6]
                                    claw_1.Speed_of_Moving_right = uart_recive_packet[7]
                                    claw_1.Speed_of_Moving_down = uart_recive_packet[8]
                                    claw_1.Speed_of_Moving_up = uart_recive_packet[9]
                                    claw_1.RPM_of_All_horizontal_sides = uart_recive_packet[10]
                                    print("收到娃娃機封包:更新馬達轉速完成")
                                elif setting_name == "BasicsettingA":
                                    claw_1.Time_of_game = uart_recive_packet[4]# 遊戲時間
                                    claw_1.Amount_of_Award = uart_recive_packet[5] * 256 + uart_recive_packet[6]# 禮品售價
                                    claw_1.Amount_of_Present_cumulation = uart_recive_packet[7] * 256 + uart_recive_packet[8] # 目前累加金額
                                    claw_1.Time_of_Keeping_cumulation = uart_recive_packet[9] # 累加保留時間    
                                    claw_1.Time_of_Show_music = uart_recive_packet[10]
                                    claw_1.Enable_of_Midair_Grip = uart_recive_packet[11]
                                    claw_1.Error_Code_of_Machine = uart_recive_packet[12]
                                    print("收到娃娃機封包:更新基本設A完成")
                                elif setting_name == "BasicsettingB":
                                    claw_1.Delay_of_Push_talon = uart_recive_packet[4] # 下抓延遲
                                    claw_1.Delay_of_Suspend_pulled_talon = uart_recive_packet[5] * 0.1 # 上停延遲
                                    claw_1.Enable_random_of_Pushing_talon = uart_recive_packet[6]# 下抓夾亂數                               
                                    claw_1.Enable_random_of_Clamping = uart_recive_packet[7] # 夾亂數  
                                    claw_1.Time_of_Push_talon = uart_recive_packet[8] * 0.1# 下抓長度時間
                                    claw_1.Time_of_Suspend_and_Pull_talon = uart_recive_packet[9] # 上停上拉時間
                                    claw_1.Delay_of_Pull_talon = uart_recive_packet[10] * 0.1 # 上拉延遲
                                    claw_1.Error_Code_of_Machine = uart_recive_packet[12]
                                    print("收到娃娃機封包:更新基本設B完成")
                                elif setting_name == "BasicsettingC":
                                    claw_1.Enable_of_Sales_promotion = uart_recive_packet[4] # 促銷功能
                                    claw_1.Which_number_starting_when_Sales_promotion = uart_recive_packet[5]  # 促銷功能第幾局
                                    claw_1.Number_of_Strong_grip_when_Sales_promotion = uart_recive_packet[6] # 促銷功能強抓次數 
                                    claw_1.Error_Code_of_Machine = uart_recive_packet[12]
                                    print("收到娃娃機封包:更新基本設C完成")
                                publish_MQTT_claw_data(claw_1, 'commandack-clawmachinesetting', setting_name)    
                                gc.collect() 
                            LCD_update_flag['Claw_Value'] = True
                            now_main_state.transition('FEILOLI UART is OK')
                            utime.sleep_ms(100)     # 休眠一小段時間，避免過度使用CPU資源
                            continue
                print("佇列收到無法對齊的封包:", bytearray(uart_recive_packet))
        utime.sleep_ms(100)                         # 休眠一小段時間，避免過度使用CPU資源

server_report_sales_period = 3*60  # 3分鐘 = 3*60 單位秒
# server_report_sales_period = 10   # For快速測試
server_report_sales_counter = server_report_sales_period - 30 # 開機後第一次送MQTT會縮短到30秒
 
# 定義server_report計時器回調函式 (每1秒執行1次)
def server_report_timer_callback(timer):
    global wdt, mq_client_1
    if now_main_state.state == MainStatus.NONE_FEILOLI or now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
        try:
            # 更新 MQTT Subscribe
            mq_client_1.check_msg()
            #mq_client_1.ping()
        except OSError as e:
            print("WiFi is disconnect")
            now_main_state.transition('WiFi is disconnect')
            mq_client_1.disconnect()
            return

        global server_report_sales_counter
        server_report_sales_counter = (server_report_sales_counter + 1) % server_report_sales_period
        if server_report_sales_counter == 0:
        
            wdt.feed()
            if now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI :
                publish_MQTT_claw_data(claw_1, 'sales')
            # if claw_1.Error_Code_of_Machine != 0x00 :
            publish_MQTT_claw_data(claw_1, 'status')

# 定義claw_check計時器回調函式
counter_of_WAITING_FEILOLI = 0
def claw_check_timer_callback(timer):
    global counter_of_WAITING_FEILOLI
    if now_main_state.state == MainStatus.NONE_FEILOLI:
        print("Updating 娃娃機 機台狀態 ...")
        uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Machine_status)

    elif now_main_state.state == MainStatus.STANDBY_FEILOLI:
        print("Updating 娃娃機 遠端帳目、投幣帳目 ...")
        uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Transaction_account)
        # uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Coin_account)
        now_main_state.transition('FEILOLI UART is waiting')
        counter_of_WAITING_FEILOLI = 0

    if now_main_state.state == MainStatus.WAITING_FEILOLI:
        counter_of_WAITING_FEILOLI = counter_of_WAITING_FEILOLI + 1
        if counter_of_WAITING_FEILOLI >= 2:
            if counter_of_WAITING_FEILOLI == 2:
                print("Updating 娃娃機 失敗 ...")
                now_main_state.transition('FEILOLI UART is not OK')
            print("Updating 娃娃機 機台狀態 ...")
            uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Machine_status)
            
# 定義LCD_update計時器回調函式
def LCD_update_timer_callback(timer):
    import binascii
    import machine
    if LCD_update_flag['Uniform']:
        LCD_update_flag['Uniform'] = False
        unique_id_hex = binascii.hexlify(machine.unique_id()).decode().upper()

        # 清空屏幕並繪製基本資訊
        lcd_mgr.fill()  # 使用黑色清空整個畫面

        lcd_mgr.draw_text(0, 0, text='Happy Collector', bg=lcd_mgr.color.BLUE, bgmode=-1)

        lcd_mgr.draw_text(5, 8 * 16 + 5, text=unique_id_hex, fg=lcd_mgr.color.RED, bg=lcd_mgr.color.WHITE,bgmode=-1, scale=1.3)


        lcd_mgr.draw_text(0, 1 * 16, text='IN:--------', fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
        lcd_mgr.draw_text(0, 2 * 16, text='OUT:--------')
        lcd_mgr.draw_text(0, 3 * 16, text='EP:--------')
        lcd_mgr.draw_text(0, 4 * 16, text='GP:--------')
        lcd_mgr.draw_text(0, 5 * 16, text='ST:--')
        lcd_mgr.draw_text(0, 6 * 16, text='Time:mm/dd hh:mm')
        lcd_mgr.draw_text(0, 7 * 16, text='Wifi:-----')
        
    elif LCD_update_flag['WiFi']:
        LCD_update_flag['WiFi'] = False
        if now_main_state.state == MainStatus.NONE_WIFI or now_main_state.state == MainStatus.NONE_INTERNET:
            #顯示wifi和MQTT狀態
            lcd_mgr.draw_text(5*8, 7*16, text='dis  ',fg=lcd_mgr.color.RED, bg=lcd_mgr.color.BLACK, bgmode=-1)
        elif now_main_state.state == MainStatus.NONE_MQTT:
            #顯示wifi和MQTT狀態
            lcd_mgr.draw_text(5*8, 7*16, text='error',fg=lcd_mgr.color.RED, bg=lcd_mgr.color.BLACK, bgmode=-1)
        elif now_main_state.state == MainStatus.NONE_FEILOLI or now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
             #顯示wifi和MQTT狀態
            lcd_mgr.draw_text(5*8, 7*16, text='ok   ',fg=lcd_mgr.color.GREEN, bg=lcd_mgr.color.BLACK, bgmode=-1)

    elif LCD_update_flag['Claw_State']:
        LCD_update_flag['Claw_State'] = False  
        if now_main_state.state == MainStatus.NONE_FEILOLI :
            lcd_mgr.draw_text(3 * 8, 5 * 16, text="%02d" % 99)   
             #顯示娃娃機狀態
        elif now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
            lcd_mgr.draw_text(3 * 8, 5 * 16, text="%02d" % claw_1.Error_Code_of_Machine)
            #顯示娃娃機狀態
        else:
            lcd_mgr.draw_text(3 * 8, 5 * 16, text="--")

    elif LCD_update_flag['Claw_Value']:
        LCD_update_flag['Claw_Value'] = False
        if now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
            lcd_mgr.draw_text(3 * 8, 1 * 16, text="%-8d" % claw_1.Number_of_Coin, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
            lcd_mgr.draw_text(4 * 8, 2 * 16, text="%-8d" % claw_1.Number_of_Award, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
            lcd_mgr.draw_text(3 * 8, 3 * 16, text="%-8d" % claw_1.Number_of_Original_Payment, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
            lcd_mgr.draw_text(3 * 8, 4 * 16, text="%-8d" % claw_1.Number_of_Gift_Payment, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)

    elif (LCD_update_flag['Time']):
        LCD_update_flag['Time'] = False  
        # 获取当前时间戳
        timestamp = utime.time()
        # 转换为本地时间
        local_time = utime.localtime(timestamp)
        # 格式化为 "mm/dd hh:mm" 格式的字符串
        formatted_time = "{:02d}/{:02d} {:02d}:{:02d}".format(local_time[1], local_time[2], local_time[3], local_time[4])
        lcd_mgr.draw_text(5 * 8, 6 * 16, text=formatted_time,fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
        #顯示時間
    lcd_mgr.show()
    gc.collect()


############################################# 初始化 #############################################
print('\n\r開始執行Data_Collection_Main初始化，版本為:', VERSION)
print('開機秒數:', utime.ticks_ms() / 1000)

# 開啟 token 檔案
load_token()

print('1開機秒數:', utime.ticks_ms() / 1000)

wdt=WDT(timeout=1000*60*10)

print('2開機秒數:', utime.ticks_ms() / 1000)

# # LCD配置
# try:
#     lcd_mgr = LCDManager.get_instance()
#     print(lcd_mgr)
# except Exception as e:
#     print('st7735 Error')
#     reset()

LCD_update_flag = {
    'Uniform': True,
    'WiFi': False,
    'Time': False,
    'Claw_State': False,
    'Claw_Value': False,
}

print('3開機秒數:', utime.ticks_ms() / 1000)

# 創建狀態機
now_main_state = MainStateMachine()

# 創建娃娃機資料
claw_1 = ReceivedClawData()

# 創建 MQTT Client 1 資料
mq_client_1 = None

# UART配置
uart_FEILOLI = UART(2, baudrate=19200, tx=17, rx=16)

# 創建計時器物件
server_report_timer = Timer(0)
claw_check_timer = Timer(1)
LCD_update_timer = Timer(2)

# 建立並執行uart_FEILOLI_recive_packet_task
_thread.start_new_thread(uart_FEILOLI_recive_packet_task, ())

# 設定server_report計時器的間隔和回調函式
TIMER_INTERVAL = 1000  # 設定1秒鐘 = 1000（單位：毫秒）
server_report_timer.init(period=TIMER_INTERVAL, mode=Timer.PERIODIC, callback=server_report_timer_callback)
TIMER_INTERVAL = 10 * 1000  # 設定10秒鐘 = 10*1000（單位：毫秒）
claw_check_timer.init(period=TIMER_INTERVAL, mode=Timer.PERIODIC, callback=claw_check_timer_callback)
TIMER_INTERVAL = 1000  # 設定1秒鐘 = 10*1000（單位：毫秒）
LCD_update_timer.init(period=TIMER_INTERVAL, mode=Timer.PERIODIC, callback=LCD_update_timer_callback)

last_time = 0
main_while_delay_seconds = 1
while True:

    utime.sleep_ms(500)

    current_time = utime.ticks_ms()
    if (utime.ticks_diff(current_time, last_time) >= main_while_delay_seconds * 1000):
        last_time = utime.ticks_ms()

        if now_main_state.state == MainStatus.NONE_WIFI:
            print('\n\rnow_main_state: WiFi is disconnect, 開機秒數:', current_time / 1000)

            my_internet_data = connect_wifi()
            # 打印 myInternet 内容
            print("My IP Address:", my_internet_data.ip_address)
            print("My MAC Address:", my_internet_data.mac_address)
            now_main_state.transition('WiFi is OK')

        elif now_main_state.state == MainStatus.NONE_INTERNET:
            print('\n\rnow_main_state: WiFi is OK, 開機秒數:', current_time / 1000)
            now_main_state.transition('Internet is OK')  # 目前不做判斷，狀態機直接往下階段跳轉

        elif now_main_state.state == MainStatus.NONE_MQTT:
            print('now_main_state: Internet is OK, 開機秒數:', current_time / 1000)
            # mq_client_1.set_callback(subscribe_MQTT_claw_recive_callback)
            mq_client_1 = connect_mqtt()
            if mq_client_1 is not None:
                try:
                    subscribe_MQTT_claw_topic()
                    now_main_state.transition('MQTT is OK')
                except:
                    print('MQTT subscription has failed')
            gc.collect()
            print(gc.mem_free())

        elif now_main_state.state == MainStatus.NONE_FEILOLI:
            print('\n\rnow_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數:', current_time / 1000)
            gc.collect()
            print(gc.mem_free())

        elif now_main_state.state == MainStatus.STANDBY_FEILOLI:
            print('\n\rnow_main_state: FEILOLI UART is OK, 開機秒數:', current_time / 1000)
            gc.collect()
            print(gc.mem_free())

        elif now_main_state.state == MainStatus.WAITING_FEILOLI:
            print('\n\rnow_main_state: FEILOLI UART is witing, 開機秒數:', current_time / 1000)
            gc.collect()
            print(gc.mem_free())

        else:
            print('\n\rInvalid action! now_main_state:', now_main_state.state)
            print('開機秒數:', current_time / 1000)

        LCD_update_flag['Time'] = True
    

