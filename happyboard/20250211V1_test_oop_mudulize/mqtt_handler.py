
import ujson
import utime
import gc
#from mqtt_helper import process_fota, process_commands  # 引入訂閱處理函數

class MqttHandler:
    def __init__(self, mqtt_manager, claw_1, uart_FEILOLI_send_packet):
        """
        初始化 MQTT 處理器
        :param mqtt_manager: MQTT 管理器
        :param claw_1: 娃娃機資料對象
        :param uart_FEILOLI_send_packet: 傳送 UART 指令的函數
        :param uart_manager.py
        """
        self.mqtt_manager = mqtt_manager
        self.claw_1 = claw_1
        self.uart_FEILOLI_send_packet = uart_FEILOLI_send_packet  # 用於發送 UART 指令(把uart物件類也傳進來)

    def process_message(self, topic, message):
        """
        訂閱訊息的回調函數 (MQTT 訂閱接收)
        :param topic: 訂閱的 MQTT 主題
        :param message: 接收到的 MQTT 訊息
        """
        try:
            topic = topic.decode()
            message = message.decode()
            print(f"收到 MQTT 訊息: {topic} => {message}")

            # 嘗試解析 JSON 訊息
            data = ujson.loads(message)
            mac_id = self.mqtt_manager.mac_id
            token = self.mqtt_manager.token

            # 設定 MQTT topic 前綴
            topic_prefix = f"{mac_id}/{token}"

            # 判斷 MQTT 主題並執行相應處理函數
            ## /fota  ===> 處理fota 訊息
            if topic == f"{topic_prefix}/fota":
                self.process_fota(data)

            ##/commands ===> 處理commands訊息
            elif topic == f"{topic_prefix}/commands":
                #self.process_commands(data, self.publish_MQTT_claw_data, self.self.uart_FEILOLI_send_packet, self.claw_1)
                self.process_commands(data)
                print(f"debug 成功處理MQTT指令{data}")

            else:
                print(f"未知的 MQTT 主題: {topic}")

        except ValueError as ve:
            print(f"JSON 解析錯誤: {ve}")
        except Exception as e:
            print(f"MQTT 訊息處理錯誤: {e}")

    #fota先不寫
    def process_fota(self, data): 
        pass
    # 先處理commands
    def process_commands(self, data):
        """ 專門處理 接收到 /commands 的訊息 並進行下一步"""
        commands_handler = {
            'ping': self.handle_ping, # 收到ping的mqtt訊息 ==> 回應pong OK
            'version': self.handle_version, # 收到ping的mqtt訊息 ==> 回應pong OK
            # 'clawreboot': self.handle_claw_reboot,
            # 'clawstartgame': self.handle_claw_start_game,
            # 'clawcleantransaccount': self.handle_claw_clean_trans_account,
            # 'clawmachinesetting': self.handle_claw_machine_setting
        }

        command = data.get('commands') # 取出訊息(物件中)的commands欄位的值
        handler = commands_handler.get(command) #例如: 'ping' ===> 值是 self.handle_ping 這個函式的調用

        if handler:
            handler(data) # 調用self.handle_ping(ping') 
        else:
            print(f"指令有誤: {command}")

    ### ========= commands_handle 指令 所對應的函式  =============###
    def handle_ping(self, data):
        #'ping': self.handle_ping
        self.publish_MQTT_claw_data("commandack-pong")

    def handle_version(self, data):
        #'version': self.handle_version
        self.publish_MQTT_claw_data('commandack-version')


    ### ========= 發佈 publish函式  =============###
    def publish_MQTT_claw_data(self, api, para1=""):
        """
        發佈 MQTT 娃娃機數據
        :param api: API 路由名稱 (e.g., 'sales', 'status', 'commandack-*')
        :param para1: 可能的附加參數
        """
        if api == 'sales':
            data = self.build_sales_data()
        elif api.startswith("commandack"):
            data = self.handle_ack_with_state(api, para1)
        else:
            print(f"無此MQTT發佈的API: {api}")
            return
        
        ## 發佈消息 到 MQTT 
        ## 調用mqtt_manager的發佈方法
        self.mqtt_manager.publish_data(f"{self.mqtt_manager.mac_id}/{self.mqtt_manager.token}/{api}", data)
        gc.collect()

    ### 發佈娃娃機數據 相關的主題 #####
    def build_sales_data(self):
        return {
            "Epayplaytimes": self.claw_1.Number_of_Original_Payment,
            "Coinplaytimes": self.claw_1.Number_of_Coin,
            "Giftplaytimes": self.claw_1.Number_of_Gift_Payment,
            "GiftOuttimes": self.claw_1.Number_of_Award,
            "time": utime.time(),
        }
    ### 整合原本 helper 的數據處理函數  ###
    ## 發佈"commandack"為前綴的消息(回傳相關資料)
    def handle_ack_with_state(self, api_select, para1=None):
        ack_value = {
            "commandack-pong": "pong",
            "commandack-version": self.mqtt_manager.version,
        }.get(api_select, "OK")

        return {
            "ack": ack_value,
            "state": para1,
            "time": utime.time()
        }

# import ujson
# import gc
# import utime

# class MQTTHandler:
#     def __init__(self, mqtt_manager, claw, uart_func):
#         """
#         初始化 MQTT 訊息處理器
#         :param mqtt_manager: MQTT 管理器
#         :param claw: 娃娃機資料對象
#         :param uart_func: 傳送 UART 指令的函數
#         """
#         self.mqtt_manager = mqtt_manager
#         self.claw = claw
#         self.uart_func = uart_func

#     def process_message(self, topic, message):
#         """ 處理 MQTT 訂閱的訊息 """
#         try:
#             topic = topic.decode()
#             message = message.decode()
#             print(f"收到 MQTT 訊息: {topic} => {message}")

#             data = ujson.loads(message)
#             mac_id = self.mqtt_manager.mac_id
#             token = self.mqtt_manager.token

#             topic_prefix = f"{mac_id}/{token}"

#             if topic == f"{topic_prefix}/fota":
#                 self.process_fota(data)

#             elif topic == f"{topic_prefix}/commands":
#                 self.process_commands(data)

#             else:
#                 print(f"未知的 MQTT 主題: {topic}")

#         except ValueError as ve:
#             print(f"JSON 解析錯誤: {ve}")
#         except Exception as e:
#             print(f"MQTT 訊息處理錯誤: {e}")

#     ### ✅ ✅ ✅ 整合 mqtt_helper.py 內的 helper 函數 ✅ ✅ ✅ ###

#     def process_fota(self, data):
#         """ 處理 FOTA 訊息 """
#         otafile = 'otalist.dat'
#         try:
#             if 'file_list' in data and 'password' in data:
#                 if data['password'] == 'c0b82a2c-4b03-42a5-92cd-3478798b2a90':
#                     self.publish_MQTT_claw_data("fotaack")
#                     with open(otafile, 'w') as f:
#                         f.write(''.join(data['file_list']))
#                     print("FOTA file saved. Rebooting...")
#                     utime.sleep(3)
#                     import machine
#                     machine.reset()
#                 else:
#                     print("Invalid FOTA password")
#             else:
#                 print("Incomplete FOTA data received")
#         except Exception as e:
#             print(f"Error handling FOTA: {e}")

#     def process_commands(self, data):
#         """ 處理 commands 訊息 """
#         command_handlers = {
#             'ping': self.handle_ping,
#             'version': self.handle_version,
#             'clawreboot': self.handle_claw_reboot,
#             'clawstartgame': self.handle_claw_start_game,
#             'clawcleantransaccount': self.handle_claw_clean_trans_account,
#             'clawmachinesetting': self.handle_claw_machine_setting,
#         }

#         command = data.get('commands')
#         handler = command_handlers.get(command)

#         if handler:
#             handler(data)
#         else:
#             print(f"未知的指令: {command}")

#     ### ✅ ✅ ✅ 整合 command 處理函數 ✅ ✅ ✅ ###

#     def handle_ping(self, data):
#         self.publish_MQTT_claw_data("commandack-pong")

#     def handle_version(self, data):
#         self.publish_MQTT_claw_data("commandack-version")

#     def handle_claw_reboot(self, data):
#         self.publish_MQTT_claw_data("commandack-clawreboot", data.get("state"))
#         self.uart_func(KindFEILOLIcmd.Send_Machine_reboot)

#     def handle_claw_start_game(self, data):
#         try:
#             epays = data.get('epays', 0)
#             freeplays = data.get('freeplays', 0)

#             if not (1 <= epays <= 40):
#                 raise ValueError(f"Invalid epays: {epays}")
#             if not (0 <= freeplays <= 10):
#                 raise ValueError(f"Invalid freeplays: {freeplays}")

#             game_data = {"epays": epays, "freeplays": freeplays}
#             self.publish_MQTT_claw_data("commandack-clawstartgame", data.get("state"))
#             self.uart_func(KindFEILOLIcmd.Send_Starting_once_game, game_data)
#         except Exception as e:
#             print(f"Error handling clawstartgame: {e}")

#     def handle_claw_clean_trans_account(self, data):
#         account = data.get('account', '').split(", ")
#         self.publish_MQTT_claw_data("commandack-clawcleantransaccount", data.get("state"))
#         self.uart_func(KindFEILOLIcmd.Send_Clean_transaction_account, account)

#     def handle_claw_machine_setting(self, data):
#         setting = data.get('setting', '').strip()
#         valid_settings = ["BasicsettingA", "BasicsettingB", "BasicsettingC", "Clawvoltage", "Motorspeed"]
#         if setting in valid_settings:
#             self.uart_func(KindFEILOLIcmd.Ask_Machine_setting, setting)
#         else:
#             print(f"Invalid machine setting: {setting}")

#     ### ✅ ✅ ✅ 整合 publish 相關函數 ✅ ✅ ✅ ###

#     def publish_MQTT_claw_data(self, api, para1=""):
#         """ 發佈 MQTT 娃娃機數據 """
#         if api == "sales":
#             data = self.build_sales_data()
#         elif api == "status":
#             wifi_signal_strength = self.mqtt_manager.wifi_manager.get_signal_strength()
#             data = self.build_status_data(wifi_signal_strength)
#         elif api.startswith("commandack"):
#             data = self.handle_ack_with_state(api, para1)
#         else:
#             print(f"未知的 MQTT 發佈 API: {api}")
#             return

#         self.mqtt_manager.publish(f"{self.mqtt_manager.mac_id}/{self.mqtt_manager.token}/{api}", data)
#         gc.collect()

#     ### ✅ ✅ ✅ 整合原本 helper 的數據處理函數 ✅ ✅ ✅ ###

#     def build_sales_data(self):
#         return {
#             "Epayplaytimes": self.claw.Number_of_Original_Payment,
#             "Coinplaytimes": self.claw.Number_of_Coin,
#             "Giftplaytimes": self.claw.Number_of_Gift_Payment,
#             "GiftOuttimes": self.claw.Number_of_Award,
#             "time": utime.time(),
#         }

#     def build_status_data(self, wifi_signal_strength):
#         return {
#             "status": f"{self.claw.Error_Code_of_Machine:02d}",
#             "wifirssi": wifi_signal_strength,
#             "time": utime.time(),
#         }

#     def handle_ack_with_state(self, api_select, para1=None):
#         ack_value = {
#             "commandack-pong": "pong",
#             "commandack-version": self.mqtt_manager.version,
#             "fotaack": "OK",
#         }.get(api_select, "OK")

#         return {
#             "ack": ack_value,
#             "state": para1,
#             "time": utime.time(),
#         }
