# Complete project details at https://RandomNerdTutorials.com
#測試記憶體內存
import micropython
micropython.mem_info()

import wifimgr
from utime import sleep
#import machine
import senko
import os
#from dr.st7735.st7735_4bit import ST7735
from machine import SPI, Pin, WDT
import network
import ntptime
from BN165DKBDriver import readKBData
#　lcd 模組
from lcd_manager import LCDManager
# 165D键盘的四根数据线对应的GPIO
CP = Pin(0, Pin.OUT)
CE = Pin(0, Pin.OUT)
PL = Pin(32, Pin.OUT)
Q7 = Pin(33, Pin.IN)
 

#led = Pin(2, Pin.OUT)
LCD_EN = Pin(27, Pin.OUT, value=1)#第三個參數是預設輸出電 #LCD_EN.value(1)
# keyMenu = Pin(0, Pin.IN, Pin.PULL_UP) #尚未使用先comment掉
# keyU = Pin(36, Pin.IN, Pin.PULL_UP)
# keyD = Pin(39, Pin.IN, Pin.PULL_UP)
ESP32_TXD2_FEILOLI = Pin(17, Pin.IN)

# 把st7735所有相關的模組都寫在lcd_manager
# 獲取 LCD 單例singleton
lcd_mgr = LCDManager.get_instance() 
# LCD單例初始化
lcd_mgr.initialize()

lcd_mgr.fill()  # 使用預設顏色（黑色）
# 繪製文字
lcd_mgr.draw_text(0, 0, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLUE, bgmode=-1) 
#bgmode預設是0 ==>使用預設的bgcolor 例如:.fill()所指定的
#bgmode預設是-1 ==>使用當前參數所指定的bgcolor bg=lcd_mgr.color.BLUE

lcd_mgr.show()
gc.collect()
print(gc.mem_free())


#　待優化為工具函式
def UDP_Load_Wifi():
    try:
        import usocket as socket
    except:
        import socket
    lcd_mgr.draw_text(0, 16,text='wait UDP Wi-Fi.', fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1) 
    lcd_mgr.show()
    # Connect to Wi-Fi
    wifi_ssid = "Sam"
    wifi_password = "0928666624"

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(wifi_ssid, wifi_password)

    while not station.isconnected():
        pass

    print("Connected to Wi-Fi")
    print('\nConnected. Network config: ', station.ifconfig())
    lcd_mgr.draw_text(0, 32, text='UDP Wi-Fi OK')
    lcd_mgr.draw_text(0, 48, text='IP:') 
    lcd_mgr.draw_text(3, 64, text=station.ifconfig()[0]) 
    lcd_mgr.show()

    # Set up UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 1234))

    print("Listening for UDP messages on port 1234")
    lcd_mgr.draw_text(0, 80, text='wait UDP...')
    lcd_mgr.show()

    while True:
        data, addr = udp_socket.recvfrom(1024)
        print("Received message: {}".format(data.decode('utf-8')))
        lcd_mgr.draw_text(0, 96,text=data.decode('utf-8'))
        lcd_mgr.show()
        with open('wifi.dat', "w") as f:
            f.write(data.decode('utf-8'))
        sleep(3)
        reset()


if readKBData(1,CP,CE,PL,Q7)[0] == 0 :
    print("SW4被按下，進入UDP load wifi")
    UDP_Load_Wifi()
elif ESP32_TXD2_FEILOLI.value() == 0 :
    print("ESP32_TXD2_FEILOLI被拉Low，進入UDP load wifi")
    UDP_Load_Wifi()

#　這裡有重複待優化(移到utils.py)
# def get_wifi_signal_strength(wlan):
#     if wlan.isconnected():
#         signal_strength = wlan.status('rssi')
#         return signal_strength
#     else:
#         print("請確認WiFi 未連接，無法檢測信號強度。")
#         return None

sleep(3)
wdt=WDT(timeout=1000*60*5) 

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

from utils import get_wifi_signal_strength
signal_strength = get_wifi_signal_strength(wlan)
if signal_strength is not None:
    print("WiFi Signal Strength:", signal_strength, "dBm")
else:
    print("Unable to retrieve signal strength.")

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")

lcd_mgr.draw_text(0 , 16, text='SSID:')

lcd_mgr.draw_text(5 * 8 , 16, text=wlan.config('essid'))

lcd_mgr.draw_text(0 , 16 * 2, text=wlan.ifconfig()[0])

lcd_mgr.show()

# 增加多個NTP伺服器選項(失敗就會跳下一個嘗試)
def tw_ntp(must=False):
    ntp_servers = [
        "clock.stdtime.gov.tw", 
        "time.stdtime.gov.tw",
        "watch.stdtime.gov.tw", 
        "tick.stdtime.gov.tw", 
        "pool.ntp.org",  # 全球可用 NTP 伺服器 test ok
        "time.google.com" #Google NTP 伺服器，全球適用 
    ]  
    ntptime.NTP_DELTA = 3155673600 # UTC+8 的 magic number
    count = 1 if not must else 100

    for _ in  range(count):
        for server in ntp_servers:
            try:
                ntptime.host = server
                ntptime.settime()
                print(f"NTP 時間同步成功，使用 {server}")
                return True
            except Exception as e:
                print(f"嘗試 {server} 失敗: {e}")
                sleep(1)
                continue  # 不 return False，繼續嘗試下一個伺服器
    print("所有 NTP 伺服器皆無法同步，改用 HTTP 時間")
    from utils import get_http_time
    # 用http做時間同步的備援
    get_http_time()




# 時間RTC(處理有時連不上的問題)
# def tw_ntp(host='clock.stdtime.gov.tw', must=False):
#   """
#   host: 台灣可用的 ntp server 如下可任選，未指定預設為 clock.stdtime.gov.tw
#     tock.stdtime.gov.tw
#     watch.stdtime.gov.tw
#     time.stdtime.gov.tw
#     clock.stdtime.gov.tw
#     tick.stdtime.gov.tw
#   must: 是否非對到不可
#   """ 
#   ntptime.NTP_DELTA = 3155673600 # UTC+8 的 magic number
#   ntptime.host = host
#   count = 1
#   if must:
#     count = 100
#   for _ in  range(count):
#     try:
#       ntptime.settime()
#     except:
#       sleep(1)
#       continue
#     else:
#       return True
#   return False

tw_ntp(must=True)

# 檔案名稱
filename = 'otalist.dat'

# 取得目錄下的所有檔案和資料夾
file_list = os.listdir()
print(file_list)
# 檢查檔案是否存在
if filename in file_list:
    # 在這邊要做讀取OTA列表，然後進行OTA的執行
    print("OTA檔案存在")
    lcd_mgr.draw_text(0 , 16 * 3, text="OTAing...")
    lcd_mgr.show()

    try:
      with open(filename) as f:
          lines = f.readlines()[0].strip()

      lines = lines.replace(' ', '')

      # 移除字串中的雙引號和空格，然後使用逗號分隔字串
      file_list = [file.strip('"') for file in lines.split(',')]
      OTA = senko.Senko(
          user="hsilan-sui",  # Required
          repo="happycollector",  # Required
          branch="Sui_Branch",  # Optional: Defaults to "master"
          working_dir="happyboard/20230524V1",  # Optional: Defaults to "app"
          files=file_list
      )
    #   OTA = senko.Senko(
    #       user="pc0808f",  # Required
    #       repo="happycollector",  # Required
    #       branch="alpha",  # Optional: Defaults to "master"
    #       working_dir="happyboard/20230524V1",  # Optional: Defaults to "app"
    #       files=file_list
    #   )
     

      if OTA.update():
          print("Updated to the latest version! Rebooting...")
          os.remove(filename)
          reset()
    except:
      print("Updated error! Rebooting...")
    os.remove(filename)
else:
    lcd_mgr.draw_text(0, 16 * 3 ,text="No OTA")
    lcd_mgr.show()
    print("OTA檔案不存在")

print("ESP OTA OK")

while True:
    for i in range(3, 0, -1):
        lcd_mgr.draw_text(0, 16 * 3, text=f"CountDown...{str(i)}",bg=lcd_mgr.color.BLACK, bgmode=-1)
        lcd_mgr.show()
        sleep(1)

    gc.collect()
    try:
        print("執行Data_Collection_Main.py...")
        micropython.mem_info()
        execfile('Data_Collection_Main.py')
    except Exception as e:
        print("執行失敗，改跑Data_Collection_Main.mpy", e)
        __import__('Data_Collection_Main.mpy')          

