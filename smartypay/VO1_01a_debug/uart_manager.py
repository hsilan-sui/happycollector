"""這只負責UART初始化 連線 與 發送封包 搭配uart_handler.py解析處理網卡收到的封包"""

from machine import UART
import utime
import _thread #執行緒模組
import gc

class UartManager:
    def __init__(
            self, claw_1, KindFEILOLIcmd, uart_handler, mqtt_handler):
        
        '''初始化 UART 連接'''
        self.uart_FEILOLI = UART(2, baudrate=19200, tx=17, rx=16)
        self.packet_id = 0
    
        #傳參
        self.claw_1 = claw_1
        self.KindFEILOLIcmd = KindFEILOLIcmd
        self.uart_handler = uart_handler  # 讓 UART 解析封包時用
        self.mqtt_handler = mqtt_handler  # 讓 UART 也能直接發送 MQTT 訊息

        # 在UartManager __init__中添加
        self.rx_queue = []
        self.uart_lock = _thread.allocate_lock() #啟用互斥鎖

        # 定義帳目與封包index對應
        self.clawcleanitems_positions = {
            'Epayplaytimes': 5,
            'Giftplaytimes': 7,
            'Coinplaytimes': 9,
            'GiftOuttimes': 11,
        }

    def _calculate_xor_checksum(self, packet):
        """計算封包的 XOR 校驗碼"""
        checksum = 0x00
        for i in range(2, 15):  # 校驗範圍: 2 到 14
            checksum ^= packet[i]
        return checksum

    def send_packet(self, command, parameters=None):
        """發送 UART 指令至娃娃機"""
        self.packet_id = (self.packet_id + 1) % 256  # 封包 ID 遞增

        # 指令對應的封包 (標準封包)
        packet_map = {
            self.KindFEILOLIcmd.Ask_Machine_status: [0xBB, 0x73, 0x01, 0x01, 0x00],
            self.KindFEILOLIcmd.Send_Machine_reboot: [0xBB, 0x73, 0x01, 0x01, 0x05],
            self.KindFEILOLIcmd.Ask_Transaction_account: [0xBB, 0x73, 0x02, 0x01, 0x00],
        }

        # **(1) 標準封包**
        if command in packet_map:
            packet = bytearray(packet_map[command] + [0x00] * 8 + [self.packet_id, 0x00, 0xAA])

        # **(2) 啟動遊戲 (可帶參數)**
        elif command == self.KindFEILOLIcmd.Send_Starting_once_game:
            packet = bytearray([
                0xBB, 0x73, 0x01, 0x02, 0x01, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, self.packet_id, 0x00, 0xAA
            ])

            if parameters:
                if 'epays' in parameters:
                    packet[5] = parameters['epays']
                if 'freeplays' in parameters:
                    packet[6] = parameters['freeplays']

        # **(3) 清除遠端帳目**
        elif command == self.KindFEILOLIcmd.Send_Clean_transaction_account:
            packet = bytearray([
                0xBB, 0x73, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, self.packet_id, 0x00, 0xAA
            ])

            if not parameters or set(parameters) == set(self.clawcleanitems_positions.keys()):
                for pos in self.clawcleanitems_positions.values():
                    packet[pos] = 0x01
            else:
                for item in parameters:
                    if item in self.clawcleanitems_positions:
                        packet[self.clawcleanitems_positions[item]] = 0x01

        # **(4) 查詢機台設定**
        elif command == self.KindFEILOLIcmd.Ask_Machine_setting:
            if parameters and parameters in self.uart_handler.clawsettingdict:
                setting_code = self.uart_handler.clawsettingdict[parameters]

                packet = bytearray([
                    0xBB, 0x73, 0x03, 0x01, setting_code,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    self.packet_id, 0x00, 0xAA
                ])
            else:
                print(f"未知的機台設定項目: {parameters}")
                return
        else:
            print(f"未知的指令: {command}")
            return

        # **統一計算 XOR 校驗碼**
        packet[15] = self._calculate_xor_checksum(packet)

        # **發送 UART 封包**
        self.uart_FEILOLI.write(packet)
        print(f"Sent packet to 娃娃機: {self._format_packet(packet)}")

    
        #執行緒
    def receive_packet(self):
        """接收 UART 封包並交由 uart_handler 處理
        這裡只做「封包重組」及「校驗」，真正的內容解析在 uart_handler 裡 parse_packet() 負責"""
        print("debug: [uart_manager.receive_packet 執行緒啟動中..]:")
        while True:
            try:
                if self.uart_FEILOLI.any(): # 如果 UART 裝置有資料可讀，先把所有可讀資料一次讀完
                    receive_data = self.uart_FEILOLI.read()
                    if receive_data:
                        with self.uart_lock:  # 加入互斥鎖保護
                            self.rx_queue.extend(receive_data) #將 bytes append 進 rx_queue
                        print(f"DEBUG: Received Raw Data 收到執行緒receive_packet: {receive_data}")

                        # 累積rx_queue佇列足夠後，就嘗試解析
                        self._process_rx_queue()
                    else:
                        # 沒資料就稍作休眠
                        print("DEBUG: No data received from UART")
                        utime.sleep_ms(100)  
                utime.sleep_ms(50)  # 避免CPU被卡死
                gc.collect()
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

    def _format_packet(self, packet):
        """格式化封包輸出"""
        return " ".join(f"{byte:02X}" for byte in packet)
