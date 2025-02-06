# import network
# import socket
# from utime import 
import os
import network

# def load_token(file_path='token.dat'):
#     """
#     讀取 token 檔案內容。
    
#     :param file_path: token 檔案的路徑
#     :return: token 字符串
#     """
#     try:
#         with open(file_path, 'r') as f:
#             token = f.readlines()[0].strip()
#         print('Get token:', token)
#         if len(token) != 36:
#             raise ValueError(f"token的長度不對: {len(token)}")
#         return token
#     except Exception as e:
#         print("Open token.dat failed:", e)
#         while True:
#             print('遺失 token 檔案或內容有誤')
#             sleep(30)
# # 預設的 WiFi SSID 和密碼
# WIFI_SSID_DEFAULT = 'paypc'
# WIFI_PASSWORD_DEFAULT = 'abcd1234'

# class InternetData:
#     """儲存 IP 與 MAC 地址的資料結構"""
#     def __init__(self, ip_address="", mac_address=""):
#         self.ip_address = ip_address
#         self.mac_address = mac_address

# def connect_wifi(wifi=None, wifi_ssid=None, wifi_password=None):
#     """
#     連接 WiFi 並返回連線資料。如果未提供 WiFi 物件，將自動建立一個。
    
#     :param wifi: network.WLAN 的實例（可選）
#     :param wifi_ssid: WiFi 名稱（可選）
#     :param wifi_password: WiFi 密碼（可選）
#     :return: InternetData 包含 IP 與 MAC 地址
#     """
#     if wifi is None:
#         wifi = network.WLAN(network.STA_IF)  # 如果未傳入 WiFi 物件，自動建立
#         wifi.active(True)

#     if wifi_ssid is None:
#         wifi_ssid = WIFI_SSID_DEFAULT
#     if wifi_password is None:
#         wifi_password = WIFI_PASSWORD_DEFAULT

#     if not wifi.config('essid'):
#         print('未經過 wifimgr.py，開始連接 WiFi...')
#         wifi.connect(wifi_ssid, wifi_password)

#     print(f'嘗試連接 WiFi，SSID: {wifi_ssid}')

#     while True:
#         for i in range(20):
#             print(f'剩餘 {20 - i} 秒...')
#             sleep(1)
#             if wifi.isconnected():
#                 break
#         if wifi.isconnected():
#             print('WiFi 連接成功！')
#             ip_address = wifi.ifconfig()[0]
#             mac_address = ''.join(['{:02X}'.format(byte) for byte in wifi.config('mac')])
#             gc.collect()  # 手動回收垃圾以避免內存碎片化
#             return InternetData(ip_address=ip_address, mac_address=mac_address)
#         else:
#             print(f'WiFi({wifi_ssid}) 連接失敗，等待重試...')
#             for i in range(30, -1, -1):
#                 print(f"倒數 {i} 秒後重試")
#                 sleep(1)


def get_wifi_signal_strength(wlan):
    """
    獲取 WiFi 信號強度 (RSSI)。
    :param wlan: 已連接的 WLAN 實例
    :return: 信號強度 (RSSI) 或 None
    """
    if wlan.isconnected():
        try:
            signal_strength = wlan.status('rssi')
            return signal_strength
        except AttributeError:
            print("此設備不支援 RSSI 功能。")
            return None
    else:
        print("WiFi 未連接，無法檢測信號強度。")
        return None


# def UDP_Load_Wifi(lcd_mgr):
#     """
#     使用 UDP 設置 Wi-Fi 配置。
#     :param lcd_mgr: LCD 管理器，用於顯示信息
#     """
#     lcd_mgr.draw_text(0, 16, text='wait UDP Wi-Fi.', fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1) 
#     lcd_mgr.show()

#     # 默認 Wi-Fi 配置
#     wifi_ssid = "Sam"
#     wifi_password = "0928666624"

#     # 初始化 Wi-Fi STA 模式
#     station = network.WLAN(network.STA_IF)
#     station.active(True)
#     station.connect(wifi_ssid, wifi_password)

#     while not station.isconnected():
#         pass

#     print("Connected to Wi-Fi")
#     print('\nConnected. Network config: ', station.ifconfig())
#     lcd_mgr.draw_text(0, 32, text='UDP Wi-Fi OK')
#     lcd_mgr.draw_text(0, 48, text='IP:') 
#     lcd_mgr.draw_text(3, 64, text=station.ifconfig()[0]) 
#     lcd_mgr.show()

#     # 配置 UDP socket
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.bind(("0.0.0.0", 1234))

#     print("Listening for UDP messages on port 1234")
#     lcd_mgr.draw_text(0, 80, text='wait UDP...')
#     lcd_mgr.show()

#     while True:
#         data, addr = udp_socket.recvfrom(1024)
#         message = data.decode('utf-8')
#         print(f"Received message: {message}")
#         lcd_mgr.draw_text(0, 96, text=message)
#         lcd_mgr.show()
#         # 保存 Wi-Fi 配置
#         with open('wifi.dat', "w") as f:
#             f.write(message)
#         sleep(3)
#         # 重啟系統以應用新配置
#         reset()
def get_file_info(filename):
    """
    獲取指定文件的大小和修改時間。
    
    :param filename: 文件名
    :return: (size, mtime) 文件大小（以字節為單位）和修改時間戳，如果文件不存在則返回 (None, None)
    """
    try:
        file_stat = os.stat(filename)
        file_size = file_stat[6]  # 第 6 個索引是文件大小
        file_mtime = file_stat[8]  # 第 8 個索引是最後修改時間
        return file_size, file_mtime
    except OSError:
        # 文件不存在時返回 None
        return None, None