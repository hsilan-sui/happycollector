"""這裡放一些備援工具"""

import network
import machine
import time
import usocket as socket  # 確保 MicroPython 相容

class RescueUtility:
    def __init__(self, lcd_mgr):
        self.lcd_mgr = lcd_mgr

    def UDP_Load_Wifi(self, wifi_ssid="Sam", wifi_password="0928666624"):
        """啟動 Wi-Fi 並監聽 UDP 訊息"""
        try:
            # 顯示等待 Wi-Fi 連線
            self.lcd_mgr.draw_text(0, 16, text='等待 Wi-Fi 連線...', fg=self.lcd_mgr.color.WHITE, bg=self.lcd_mgr.color.BLACK, bgmode=-1)
            self.lcd_mgr.show()
            
            # 初始化 Wi-Fi STA 模式
            station = network.WLAN(network.STA_IF)
            station.active(True)

            if not station.active():
                raise OSError("Wi-Fi STA 模式啟動失敗")

            # 嘗試連接 Wi-Fi
            print(f"正在連接 Wi-Fi: {wifi_ssid} ...")
            station.connect(wifi_ssid, wifi_password)

            # 等待 Wi-Fi 連線，最多 10 秒
            timeout = 10
            while not station.isconnected() and timeout > 0:
                print(f"Wi-Fi 連線中... 剩餘 {timeout} 秒")
                time.sleep(1)
                timeout -= 1

            if not station.isconnected():
                raise OSError("Wi-Fi 連線失敗，請檢查 SSID/PASSWORD 或 Wi-Fi 訊號")

            print("Wi-Fi 連線成功！")
            print('Network config:', station.ifconfig())

            self.lcd_mgr.draw_text(0, 32, text='Wi-Fi 連線成功！')
            self.lcd_mgr.draw_text(0, 48, text='IP:')
            self.lcd_mgr.draw_text(3, 64, text=station.ifconfig()[0])
            self.lcd_mgr.show()

            # 設定 UDP Socket
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.bind(("0.0.0.0", 1234))

            print("正在監聽 UDP 端口 1234 ...")
            self.lcd_mgr.draw_text(0, 80, text='等待 UDP 訊息...')
            self.lcd_mgr.show()

            # 開始監聽 UDP 訊息
            while True:
                try:
                    data, addr = udp_socket.recvfrom(1024)
                    msg = data.decode('utf-8')
                    print("接收到 UDP 訊息:", msg)
                    self.lcd_mgr.draw_text(0, 96, text=msg)
                    self.lcd_mgr.show()

                    # 儲存 Wi-Fi 設定
                    with open('wifi.dat', "w") as f:
                        f.write(msg)

                    # 等待 3 秒後重啟
                    time.sleep(3)
                    machine.reset()
                except Exception as e:
                    print(f"UDP 接收錯誤: {e}")
                    self.lcd_mgr.draw_text(0, 96, text=f"UDP 錯誤: {e}")
                    self.lcd_mgr.show()
        except OSError as e:
            print(f"Wi-Fi 錯誤: {e}")
            self.lcd_mgr.draw_text(0, 32, text=f"Wi-Fi 錯誤: {e}")
            self.lcd_mgr.show()
        except Exception as e:
            print(f"未知錯誤: {e}")
            self.lcd_mgr.draw_text(0, 32, text=f"未知錯誤: {e}")
            self.lcd_mgr.show()
