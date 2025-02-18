"""這只負責UART初始化 連線 與 發送封包 搭配uart_handler.py解析處理網卡收到的封包"""

from machine import UART
import utime
import gc
#rom uart_handler import UartHandler

class UartManager:
    def __init__(
            self, claw_1, KindFEILOLIcmd, uart_handler, mqtt_handler):
        
        '''初始化 UART 連接'''
        self.uart_FEILOLI = UART(2, baudrate=19200, tx=17, rx=16)
        self.packet_id = 0
        self.claw_1 = claw_1
        self.KindFEILOLIcmd = KindFEILOLIcmd
        self.uart_handler = uart_handler  # 讓 UART 解析封包時用
        self.mqtt_handler = mqtt_handler  # 讓 UART 也能直接發送 MQTT 訊息
        # 在UartManager __init__中添加
        self.rx_queue = []

    def send_packet(self, command, parameters=None):
        """發送 UART 指令至娃娃機"""
        self.packet_id = (self.packet_id + 1) % 256  # 封包 ID 遞增

        # self.uart_manager.send_packet(self.KindFEILOLIcmd.Send_Starting_once_game, game_data)
        # 指令對應封包
        packet_map = {
            self.KindFEILOLIcmd.Ask_Machine_status: [0xBB, 0x73, 0x01, 0x01, 0x00],
            self.KindFEILOLIcmd.Send_Machine_reboot: [0xBB, 0x73, 0x01, 0x01, 0x05],
            #Send_Machine_shutdown
            #Send_Payment_countdown_Or_fail
            self.KindFEILOLIcmd.Send_Starting_once_game: [0xBB, 0x73, 0x01, 0x02, 0x01],
            self.KindFEILOLIcmd.Ask_Transaction_account: [0xBB, 0x73, 0x02, 0x01, 0x00],
            #Send_Clean_transaction_account
            #Ask_Machine_setting
        }

        if command in packet_map:
            packet = bytearray(packet_map[command] + [0x00] * 8 + [self.packet_id, 0x00, 0xAA])

            # 計算 XOR 校驗碼
            for i in range(2, 14):
                packet[15] ^= packet[i]

            # 寫入 UART
            self.uart_FEILOLI.write(packet)
            print(f"Sent packet to 娃娃機: {self._format_packet(packet)}")
    #執行緒
    def receive_packet(self):
        """接收 UART 封包並交由 uart_handler 處理
        這裡只做「封包重組」及「校驗」，真正的內容解析在 uart_handler 裡 parse_packet() 負責"""
        print("debug: [uart_manager.receive_packet 執行緒啟動中..]:")
        while True:  # 持續執行接收任務|執行緒需要持續運作，等待 UART 接收資料 加入Try except 
            try:
                if self.uart_FEILOLI.any(): # 如果 UART 裝置有資料可讀，先把所有可讀資料一次讀完
                    receive_data = self.uart_FEILOLI.read()
                    if receive_data:
                        self.rx_queue.extend(receive_data) #將 bytes append 進 rx_queue
                        print(f"DEBUG: Received Raw Data 收到執行緒receive_packet: {receive_data}")

                        # 累積rx_queue佇列足夠後，就嘗試解析
                        self._process_rx_queue()
                    else:
                        # 沒資料就稍作休眠
                        print("DEBUG: No data received from UART")
                        utime.sleep_ms(100)  

                    # while len(self.rx_queue) >= 16:
                    #     packet = bytearray(16)
                    #     packet[0] = self.rx_queue.pop(0)

                    #     if packet[0] == 0x2D and self.rx_queue[0] == 0x8A:
                    #         packet[1] = self.rx_queue.pop(0)
                    #         checksum = 0xAA
                    #         for i in range(2, 16):
                    #             packet[i] = self.rx_queue.pop(0)
                    #             checksum ^= packet[i]
                            
                    #         if checksum == 0x00:  # 校驗成功
                    #             print("debug: 收到有效封包:", self._format_packet(packet))
                    #             self.uart_handler.parse_packet(packet)  # 交由 uart_handler 處理詳細的封包內容
                    #             print("debug: 已發送給解析封包parse_packet功能去了", self._format_packet(packet))
                    #         else:
                    #             print("封包校驗失敗")
                # else:
                #     print("DEBUG: No data received from UART")
                #     utime.sleep_ms(100)
            except Exception as e: 
                #避免任何未預期讓整個執行緒退出
                print("debug: receive_packet() 執行緒拋出例外錯誤",e)
                utime.sleep_ms(100)

    def _process_rx_queue(self):
        """
        處理已累積的 self.rx_queue，找封包起始 0x2D 0x8A，
        一次擷取滿 16 Bytes 後校驗；校驗成功就交由 uart_handler。
        """
        while True:
            # 先確定至少有 2 bytes 可以檢查封包起始
            if len(self.rx_queue) < 2:
                break

            # 若前兩個 bytes 不是封包起始 (0x2D 0x8A)，丟棄第一個 byte，繼續尋找
            if not (self.rx_queue[0] == 0x2D and self.rx_queue[1] == 0x8A):
                self.rx_queue.pop(0)
                continue

            # 如果已知前兩個符合，還要確保整個封包 16 bytes 是否已到齊
            if len(self.rx_queue) < 16:
                # 未滿 16 bytes，先等下一次再來判斷
                break

            # 取出前 16 bytes 當成一個完整封包
            packet_bytes = self.rx_queue[:16]
            # 從佇列中移除
            del self.rx_queue[:16]

            # 計算校驗
            checksum = 0xAA
            for i in range(2, 16):
                checksum ^= packet_bytes[i]

            if checksum == 0x00:  # 校驗成功
                print("debug: 收到有效封包:", self._format_packet(packet_bytes))
                # 交由 uart_handler 作進一步解析
                self.uart_handler.parse_packet(packet_bytes)
                print("debug: 已發送給解析封包 parse_packet 功能去了", self._format_packet(packet_bytes))
            else:
                print("封包校驗失敗")
    # def receive_packet(self):
    #     """接收 UART 封包並交由 uart_handler 處理
    #     這裡只做「封包重組」及「校驗」，真正的內容解析在 uart_handler 裡 parse_packet() 負責"""
    #     print("debug: [uart_manager.receive_packet 執行緒啟動中..]:")
    #     while True:  # 持續執行接收任務|執行緒需要持續運作，等待 UART 接收資料 加入Try except 
    #         if self.uart_FEILOLI.any(): # 如果 UART 裝置有資料可讀，先把所有可讀資料一次讀完
    #             receive_data = self.uart_FEILOLI.read()
    #             print(f"DEBUG: Received Raw Data: {receive_data}")
    #             self.rx_queue.extend(receive_data)

    #             while len(self.rx_queue) >= 16:
    #                 packet = bytearray(16)
    #                 packet[0] = self.rx_queue.pop(0)

    #                 if packet[0] == 0x2D and self.rx_queue[0] == 0x8A:
    #                     packet[1] = self.rx_queue.pop(0)
    #                     checksum = 0xAA
    #                     for i in range(2, 16):
    #                         packet[i] = self.rx_queue.pop(0)
    #                         checksum ^= packet[i]
                        
    #                     if checksum == 0x00:  # 校驗成功
    #                         print("debug: 收到有效封包:", self._format_packet(packet))
    #                         self.uart_handler.parse_packet(packet)  # 交由 uart_handler 處理詳細的封包內容
    #                         print("debug: 已發送給解析封包parse_packet功能去了", self._format_packet(packet))
    #                     else:
    #                         print("封包校驗失敗")
    #         else:
    #             print("DEBUG: No data received from UART")
    #             utime.sleep_ms(100)

    def _format_packet(self, packet):
        """格式化封包輸出"""
        return " ".join(f"{byte:02X}" for byte in packet)

# # # UART配置
# # uart_FEILOLI = UART(2, baudrate=19200, tx=17, rx=16)
# class UartManager:
#     def __init__(self, uart_port=2,baudrate=19200, tx=17, rx=16, claw_1="claw_1", KindFEILOLIcmd="KindFEILOLIcmd"):
       
#        '''初始化UART連接'''
#        self.uart_FEILOLI = UART(uart_port,baudrate, tx, rx)

#        self.packet_id = 0
#        self.rx_queue = []
#        self.clawsettingdict = {
#             "BasicsettingA": 0x00,
#             "BasicsettingB": 0x01,
#             "BasicsettingC": 0x02,
#             "Clawvoltage": 0x03,#抓力電壓
#             "Motorspeed": 0x04,
#        }
#        #娃娃機數據
#        self.claw_1 = claw_1 
#        #娃娃機指令
#        self.KindFEILOLIcmd = KindFEILOLIcmd

#     def send_packet(self, command, parameters=None):

#         """發送 UART 指令至娃娃機"""
#         self.packet_id = (self.packet_id + 1) % 256 #封包id遞增

#         #指令<==>封包 映射map
#         packet_map = {
#             # 詢問機台狀態
#             self.KindFEILOLIcmd.Ask_Machine_status: [0xBB, 0x73, 0x01, 0x01, 0x00],
#             # 暖重置
#             self.KindFEILOLIcmd.Send_Machine_reboot: [0xBB, 0x73, 0x01, 0x01, 0x05],
#             #關機
#             self.KindFEILOLIcmd.Send_Machine_shutdown: [],
#             #倒數付款
#             self.KindFEILOLIcmd.Send_Payment_countdown_Or_fail: [],
#             #啟動遊戲
#             self.KindFEILOLIcmd.Send_Starting_once_game: [0xBB, 0x73, 0x01, 0x02, 0x01],
#             #查詢:遠端帳目
#             self.KindFEILOLIcmd.Ask_Transaction_account: [0xBB, 0x73, 0x02, 0x01, 0x00],
#             #清除:遠端帳目
#             self.KindFEILOLIcmd.Send_Clean_transaction_account: [0xBB, 0x73, 0x02, 0x01, 0x00],
#             #查詢:機台設定
#             self.KindFEILOLIcmd.Ask_Machine_setting: [0xBB, 0x73, 0x03, 0x01, self.clawsettingdict[parameters]] if parameters else [0xBB, 0x73, 0x03, 0x01,0x00] 
#         }

#         # 
#         if command in packet_map:
#             #組織16位封包
#             packet = bytearray(packet_map[command] + [0x00] * 8 + [self.packet_id, 0x00, 0xAA])
#             # 啟動遊戲封包
#             if command == self.KindFEILOLIcmd.Send_Starting_once_game and parameters:
#                 packet[5] = parameters.get("epay", 1)
#                 packet[6] = parameters.get("freeplays", 1)

#             # 遠端清除封包
#             elif command == self.KindFEILOLIcmd.Send_Clean_transaction_account:
#                 # 定義帳目與封包index對應
#                 clawcleanitems_positions = {
#                     'Epayplaytimes': 5,
#                     'Giftplaytimes': 7,
#                     'Coinplaytimes': 9,
#                     'GiftOuttimes': 11,
#                 }

#                 if not parameters or set(parameters) == set(clawcleanitems_positions.keys()): 
#                     # 全部清除
#             ## 取出clawcleanitems_positions中定義的key值對應封包index
#                     for pos in clawcleanitems_positions.values():
#                         packet[pos] = 0x01
#                     else: 
#                         for item in parameters:
#                             if item in clawcleanitems_positions:
#                                 packet[clawcleanitems_positions[item]] = 0x01

#             self._calculate_checksums(packet)
#             self.uart.write(packet)
#             print("Sent packet to 娃娃機:    ", self._format_packet(packet))

#     def receive_packet(self):
        
#         """從UART 讀取封包"""
#         if self.uart_FEILOLI.any():
#             receive_data = self.uart_FEILOLI.read()
#             self.rx_queue.extend(receive_data)

#             while len(self.rx_queue) >= 16:
#                 packet = bytearray(16)
#                 packet[0] = self.rx_queue.pop(0)

#                 if packet[0] == 0x2D and self.rx_queue[0] == 0x8A:
#                     packet[1] = self.rx_queue.pop(0)
#                     checksum = 0xAA
#                     for i in range(2, 16):
#                         packet[i] = self.rx_queue.pop(0)
#                         checksum ^= packet[i]
#                     if checksum == 0x00:
#                         self._parse_packet(packet)

#     #這裡要處理 因為有分為|網卡=>娃娃機 [2:14]
#     def _calculate_checksum(self, packet):
#         """計算封包 xor 校驗"""
#         checksum = 0
#         for i in range(2, 14):
#             checksum ^= packet[i]
#         packet[15] = checksum

#     def _format_packet(self, packet):
#         """格式化封包"""
#         return ''.join('{:02X}'.format(byte) for byte in packet)
    
        
#     def _parse_packet(self, packet):
#         """解析 UART 接收的封包並存入 self.received_data"""
#         print("收到封包:", self._format_packet(packet))

#         if packet[2] == 0x81 and packet[3] == 0x01:
#             """機台狀態回應"""
#             self.claw_1.CMD_Control_Machine = packet[4]
#             self.claw_1.Status_of_Current_machine = [packet[5], packet[6]]
#             self.claw_1.Time_of_Current_game = packet[7]
#             self.claw_1.Game_amount_of_Player = packet[8] * 256 + packet[9]
#             self.claw_1.Way_of_Starting_game = packet[10]
#             self.claw_1.Cumulation_amount_of_Sale_card = packet[11] * 256 + packet[14]
#             self.claw_1.Error_Code_of_Machine = packet[12]

#             print(f"機台狀態更新: {vars(self.claw_1)}")

#         elif packet[2] == 0x82 and packet[3] == 0x01:
#             """帳目查詢回應"""
#             self.claw_1.Number_of_Original_Payment = packet[4] * 256 + packet[5]
#             self.claw_1.Number_of_Gift_Payment = packet[6] * 256 + packet[7]
#             self.claw_1.Number_of_Coin = packet[8] * 256 + packet[9]
#             self.claw_1.Number_of_Award = packet[10] * 256 + packet[11]
#             self.claw_1.Error_Code_of_Machine = packet[12]

#             print(f"帳目查詢數據: {vars(self.claw_1)}")

#         elif packet[2] == 0x83:
#             """機台設定回應"""
#             cmd = packet[3]
#             setting_name = {v: k for k, v in self.clawsettingdict.items()}.get(cmd)

#             if setting_name == "Clawvoltage":
#                 self.claw_1.Value_of_Hi_voltage = packet[4] * 0.2
#                 self.claw_1.Value_of_Mid_voltage = packet[5] * 0.2
#                 self.claw_1.Value_of_Lo_voltage = packet[6] * 0.2
#                 self.claw_1.Distance_of_Mid_voltage_and_Top = packet[7]
#                 self.claw_1.Hi_voltage_of_Guaranteed_prize = packet[8] * 0.2
#                 self.claw_1.Error_Code_of_Machine = packet[12]

#                 print(f"機台設定 - 抓力電壓: {vars(self.claw_1)}")

#             elif setting_name == "Motorspeed":
#                 self.claw_1.Speed_of_Moving_forward = packet[4]
#                 self.claw_1.Speed_of_Moving_back = packet[5]
#                 self.claw_1.Speed_of_Moving_left = packet[6]
#                 self.claw_1.Speed_of_Moving_right = packet[7]
#                 self.claw_1.Speed_of_Moving_down = packet[8]
#                 self.claw_1.Speed_of_Moving_up = packet[9]
#                 self.claw_1.RPM_of_All_horizontal_sides = packet[10]

#                 print(f"機台設定 - 馬達速度: {vars(self.claw_1)}")

#             elif setting_name == "BasicsettingA":
#                 self.claw_1.Time_of_game = packet[4]
#                 self.claw_1.Amount_of_Award = packet[5] * 256 + packet[6]
#                 self.claw_1.Amount_of_Present_cumulation = packet[7] * 256 + packet[8]
#                 self.claw_1.Time_of_Keeping_cumulation = packet[9]
#                 self.claw_1.Time_of_Show_music = packet[10]
#                 self.claw_1.Enable_of_Midair_Grip = packet[11]
#                 self.claw_1.Error_Code_of_Machine = packet[12]

#                 print(f"機台設定 - 基本設A: {vars(self.claw_1)}")

#             elif setting_name == "BasicsettingB":
#                 self.claw_1.Delay_of_Push_talon = packet[4]
#                 self.claw_1.Delay_of_Suspend_pulled_talon = packet[5] * 0.1
#                 self.claw_1.Enable_random_of_Pushing_talon = packet[6]
#                 self.claw_1.Enable_random_of_Clamping = packet[7]
#                 self.claw_1.Time_of_Push_talon = packet[8] * 0.1
#                 self.claw_1.Time_of_Suspend_and_Pull_talon = packet[9]
#                 self.claw_1.Delay_of_Pull_talon = packet[10] * 0.1
#                 self.claw_1.Error_Code_of_Machine = packet[12]

#                 print(f"機台設定 - 基本設B: {vars(self.claw_1)}")

#             elif setting_name == "BasicsettingC":
#                 self.claw_1.Enable_of_Sales_promotion = packet[4]
#                 self.claw_1.Which_number_starting_when_Sales_promotion = packet[5]
#                 self.claw_1.Number_of_Strong_grip_when_Sales_promotion = packet[6]
#                 self.claw_1.Error_Code_of_Machine = packet[12]

#                 print(f"機台設定 - 基本設C: {vars(self.claw_1)}")
#             # 解析完要發送matt消息
#             self.mqtt_handler.publish_MQTT_claw_data(claw_1, 'commandack-clawmachinesetting', setting_name)