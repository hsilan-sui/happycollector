import network
import socket
import ure
import time
import binascii
import machine
import random

class WiFiManager:
    def __init__(self):
        """Wi-Fi 管理類，負責 Wi-Fi 連線 (STA) 並提供 AP 設定模式"""
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)

        self.ap_ssid, self.ap_password = self.generate_ap_credentials()

        # 讀取 wifi.dat 中的 SSID & 密碼
        self.ssid, self.password = self.load_wifi_config()

    def generate_ap_credentials(self):
        """根據 ESP32 的唯一 ID 產生 AP 熱點名稱"""
        unique_id_hex = binascii.hexlify(machine.unique_id()[-3:]).decode().upper()
        ap_ssid = "HappyWifi" + unique_id_hex
        ap_password = "happywifi"
        return ap_ssid, ap_password

    def load_wifi_config(self):
        """從 wifi.dat 讀取 Wi-Fi 設定，讀取失敗則返回 (None, None)"""
        try:
            with open('wifi.dat', 'r') as f:
                lines = f.read().strip().split("\n")
                for line in lines:
                    parts = line.split(";")
                    if len(parts) == 2:
                        ssid, password = parts
                        print(f"讀取 Wi-Fi 設定: SSID={ssid}")
                        return ssid, password
        except Exception as e:
            print("無法讀取 wifi.dat:", e)

        return None, None  # 讀取失敗則回傳 `(None, None)`

    def save_wifi_config(self, ssid, password):
        """將新的 Wi-Fi 設定寫入檔案"""
        try:
            with open('wifi.dat', 'w') as f:
                f.write(f"{ssid};{password}\n")
            print(f"Wi-Fi 設定已更新: SSID={ssid}, PASSWORD=******")
        except Exception as e:
            print("無法寫入 Wi-Fi 設定:", e)

    def disconnect(self):
        """確保 Wi-Fi 連線被清除，避免 Wi-Fi 內部錯誤"""
        if self.wifi.isconnected():
            self.wifi.disconnect()
            time.sleep(1)
        self.wifi.active(True)

    def connect(self):
        """嘗試連線 Wi-Fi，失敗時啟動 AP 設定模式"""
        if not self.ssid or not self.password:
            print("Wi-Fi 設定檔讀取失敗，啟動 AP 設定模式...")
            self.start_ap_web()
            return None

        if self.wifi.isconnected():
            print("Wi-Fi connected!")
            return self.get_ip_mac()

        print(f"Tring to connect to : {self.ssid} ...")
        self.disconnect()
        self.wifi.connect(self.ssid, self.password)

        for retry in range(10):
            if self.wifi.isconnected():
                print("Wi-Fi 連線成功！")
                return self.get_ip_mac()
            print(f"嘗試連線中... {retry+1}/10")
            time.sleep(1)

        print("Wi-Fi 連線失敗！啟動 AP 設定模式")
        self.start_ap_web()
        return None
    
    def get_signal_strength(self):
        """取得 Wi-Fi 訊號強度 (RSSI)"""
        if self.wifi.isconnected():
            # print(f"WiFi Signal Strength: {self.wifi.status('rssi')} dBm")
            return self.wifi.status('rssi')  # 取得訊號強度
        else:
            print("Unable to retrieve signal strength.")
            return None
    
    def get_ip_mac(self):
        """取得 IP 和 MAC 地址 並將 MAC 轉換為 12 碼 HEX 格式"""
        if self.wifi.isconnected():
            ip_info = self.wifi.ifconfig()  # 獲取完整的 IP 設定
            ip_address = ip_info[0] # IP位置
            raw_mac = self.wifi.config('mac')  # 取得 MAC 位元組
            mac_address = binascii.hexlify(raw_mac).decode().upper()  # 轉換為 12 碼格式
            # mac_address = ":".join(f"{b:02X}" for b in self.wifi.config('mac'))
            #print(f"IP 地址: {ip_address}, MAC: {mac_address}")
            print(f"Network config: {ip_info}")
            return {"ip": ip_address, "mac": mac_address}
        else:
            print("Wi-Fi 未連線，無法獲取 IP/MAC")
            return None

    def start_ap_web(self, port=80):
        """啟動 AP 模式，提供 Web 介面讓使用者輸入 SSID/PASSWORD"""
        wlan_ap = network.WLAN(network.AP_IF)
        wlan_ap.active(True)
        wlan_ap.config(essid=self.ap_ssid, password=self.ap_password, authmode=3)

        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        server_socket = socket.socket()
        server_socket.bind(addr)
        server_socket.listen(1)

        print(f"AP 模式啟動: SSID={self.ap_ssid}, 密碼={self.ap_password}")
        print("開啟瀏覽器，連線到 192.168.4.1 來設定 Wi-Fi")

        while True:
            if self.wifi.isconnected():
                wlan_ap.active(False)
                return

            client, addr = server_socket.accept()
            print('客戶端連線:', addr)
            self.handle_web_requests(client)

    def handle_web_requests(self, client):
        """處理 Web Server 的 HTTP 請求"""
        request = client.recv(1024).decode()
        print("請求:", request)

        if "POST" in request:
            match = ure.search("ssid=([^&]*)&password=(.*)", request)
            if match:
                ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
                password = match.group(2).replace("%3F", "?").replace("%21", "!")
                self.save_wifi_config(ssid, password)
                client.send("HTTP/1.1 200 OK\n\n Wi-Fi 設定成功！請重新啟動設備")
                time.sleep(3)
                machine.reset()
            else:
                client.send("HTTP/1.1 400 Bad Request\n\n 無效的 Wi-Fi 設定")
        else:
            client.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
            client.send('<html><h1>請輸入 Wi-Fi 設定</h1>')
            client.send('<form method="POST">SSID: <input name="ssid"><br>密碼: <input type="password" name="password"><br><button type="submit">儲存</button></form>')
            client.send('</html>')

        client.close()
