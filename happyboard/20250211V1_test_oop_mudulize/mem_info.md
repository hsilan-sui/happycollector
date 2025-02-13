# mem_info

## mqtt_helper (使用函式 x) ==>使用 mqtt_handler

- 接收消息 並且發布消息

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75552
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -42 dBm
ESP OK
(2025, 2, 13, 15, 2, 13, 3, 44)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33456, free: 74576
 No. of 1-blocks: 330, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 47920, free: 60112
 No. of 1-blocks: 466, 2-blocks: 116, max blk sz: 640, max free sz: 1605

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 909.349
1開機秒數: 909.3499
2開機秒數: 909.3499
3開機秒數: 909.3499

Init, MainStatus: NONE_WIFI
wifi_manager: <WiFiManager object at 3ffe5410>
V1.07b3_sui
3CE90E4DD7E4
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe

now_main_state: WiFi is disconnect, 開機秒數: 909.9509
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 911.204

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 912.205
MQTT broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
48896
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機:     BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
Recive packet from 娃娃機: bytearray(b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd')
Recive 娃娃機 : 二、主控制\æ��台狀態

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
```

- 連線 mqtt 訂閱與回調訂閱 ok

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Tring to connect to : propsky ...
嘗試連線中... 1/10
嘗試連線中... 2/10
Wi-Fi 連線成功！
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -40 dBm
ESP OK
(2025, 2, 12, 15, 15, 13, 2, 43)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33456, free: 74576
 No. of 1-blocks: 330, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 49728, free: 58304
 No. of 1-blocks: 487, 2-blocks: 128, max blk sz: 640, max free sz: 1254

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 81.868
1開機秒數: 81.868
2開機秒數: 81.868
3開機秒數: 81.868

Init, MainStatus: NONE_WIFI
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe

now_main_state: WiFi is disconnect, 開機秒數: 82.445
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 83.69

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 84.691
MQTT broker connected!
訂閱 MQTT 主題: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
訂閱 MQTT 主題: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota
mqtt: <MqttManager object at 3fff1fa0>
mqtt_client: <MQTTClient object at 3ffe5830>
訂閱 MQTT 主題: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
訂閱 MQTT 主題: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
39632
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機:     BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
Recive packet from 娃娃機: bytearray(b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd')
Recive 娃娃機 : 二、主控制\æ��台狀態

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 94.943
39552
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 02 00 AB

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILRecive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x02\x00#')
Recive 娃�OLI
�機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 105.428
39536
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 03 00 AA

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x03\x00"')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 115.438
39552
Traceback (most recent call last):
  File "Data_Collection_Main.py", line 880, in server_report_timer_callback
  File "Data_Collection_Main.py", line 380, in publish_MQTT_claw_data
NameError: name 'token' isn't defined
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 04 00 AD

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLRecive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x04\x00%')
Recive 娃�I
�機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 125.441
39536
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 05 00 AC

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEIRecive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x05\x00$')
Recive 娃�LOLI
�機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

```

- 訂閱需要再改

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -40 dBm
ESP OK
(2025, 2, 12, 15, 11, 32, 2, 43)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33456, free: 74576
 No. of 1-blocks: 330, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 49712, free: 58320
 No. of 1-blocks: 487, 2-blocks: 128, max blk sz: 640, max free sz: 1248

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 313.536
1開機秒數: 313.536
2開機秒數: 313.536
3開機秒數: 313.537

Init, MainStatus: NONE_WIFI
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe

now_main_state: WiFi is disconnect, 開機秒數: 314.095
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 315.293

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 316.294
執行失敗，改跑Data_Collection_Main.mpy name 'mqtt_manager' isn't defined
Traceback (most recent call last):
  File "main.py", line 284, in <module>
MemoryError: memory allocation failed, allocating 240 bytes
MicroPython v1.18-9-gd8e35d0e0-dirty on 2022-02-19; MPYBLOCKLY Micropython Borad with ESP32

  - wait until it completes current work;
  - use Ctrl+C to interrupt current work;
  - reset the device and try again;
  - check connection properties;
  - make sure the device has suitable MicroPython / CircuitPython / firmware;
  - make sure the device is not in bootloader mode.

stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Tring to connect to : propsky ...
嘗試連線中... 1/10
嘗試連線中... 2/10
Wi-Fi 連線成功！
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -44 dBm
ESP OK
(2025, 2, 12, 13, 59, 44, 2, 43)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33360, free: 74672
 No. of 1-blocks: 328, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1248 out of 15360
GC: total: 108032, used: 51184, free: 56848
 No. of 1-blocks: 508, 2-blocks: 141, max blk sz: 640, max free sz: 898

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 32.085
1開機秒數: 32.085
2開機秒數: 32.086
3開機秒數: 32.086
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
取得token: 445ccb69-2923-4f8f-b7d5-484132226ebe

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 32.656
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 33.84

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 34.841
MQTT broker connected！
MQTT connect fail: Subscribe callback is not set
mqtt: <MqttManager object at 3ffecbb0>
mqtt_client: <MQTTClient object at 3ffe5830>

```

- 雖然可以增加功能但缺點是函式參數傳遞過多
- debug 不易(但目前穩定--這裡也拆出 class)

```bash

MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75552
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -46 dBm
ESP OK
嘗試 clock.stdtime.gov.tw 失敗: Timeout,ntp server not response.
(2025, 2, 12, 13, 37, 6, 2, 43)
NTP 時間同步成功，使用 time.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33360, free: 74672
 No. of 1-blocks: 328, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1248 out of 15360
GC: total: 108032, used: 51216, free: 56816
 No. of 1-blocks: 508, 2-blocks: 141, max blk sz: 640, max free sz: 890

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 96.31301
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
1開機秒數: 96.344
2開機秒數: 96.344
3開機秒數: 96.34501
取得token: <bound_method>

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 96.869
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 98.058

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 99.061
MQTT broker connected！
MQTT connect fail: Subscribe callback is not set
mqtt: <MqttManager object at 3ffefc00>
執行失敗，改跑Data_Collection_Main.mpy 'MQTTClient' object isn't callable
```

## 把 UART 功能集中為一個 class

## 把 wifi 功能集中為一個 class

- 刪掉 connect_wifi() |951|
- debug global wifi

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -40 dBm
ESP OK
(2025, 2, 12, 11, 22, 51, 2, 43)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33328, free: 74704
 No. of 1-blocks: 326, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1248 out of 15360
GC: total: 108032, used: 50912, free: 57120
 No. of 1-blocks: 502, 2-blocks: 141, max blk sz: 640, max free sz: 951

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 2060.229
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
1開機秒數: 2060.277
2開機秒數: 2060.278
3開機秒數: 2060.278

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 2060.783
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 2062.001

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 2063.003
MQTT Broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
51648
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機:     BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
Recive packet from 娃娃機: bytearray(b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd')
Recive 娃娃機 : 二、主控制\æ��台狀態

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
```

- 把 class InternetData 刪除 |731

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -42 dBm
ESP OK
嘗試 clock.stdtime.gov.tw 失敗: Timeout,ntp server not response.
(2025, 2, 12, 11, 12, 26, 2, 43)
NTP 時間同步成功，使用 time.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33328, free: 74704
 No. of 1-blocks: 326, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1248 out of 15360
GC: total: 108032, used: 51856, free: 56176
 No. of 1-blocks: 513, 2-blocks: 148, max blk sz: 640, max free sz: 731

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 1435.304
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
1開機秒數: 1435.335
2開機秒數: 1435.335
3開機秒數: 1435.335

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 1435.841
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4
-------------------------------
Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/sales
MQTT Publish data(JSON_str): {"Giftplaytimes": 0, "GiftOuttimes": 0, "Freeplaytimes": 0, "time": 792674172, "Epayplaytimes": 0, "Coinplaytimes": 0}
MQTT Publish Successful
Traceback (most recent call last):
  File "Data_Collection_Main.py", line 875, in server_report_timer_callback
  File "Data_Collection_Main.py", line 389, in publish_MQTT_claw_data
NameError: name 'wifi' isn't defined

```

- 把 Data_Collection_Main.py 中的 my_interner_data 都改成 class 讀值|690

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -40 dBm
ESP OK
嘗試 clock.stdtime.gov.tw 失敗: Timeout,ntp server not response.
(2025, 2, 12, 11, 3, 54, 2, 43)
NTP 時間同步成功，使用 time.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33328, free: 74704
 No. of 1-blocks: 326, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1248 out of 15360
GC: total: 108032, used: 52032, free: 56000
 No. of 1-blocks: 517, 2-blocks: 150, max blk sz: 640, max free sz: 690

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 923.348
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
1開機秒數: 923.398
2開機秒數: 923.399
3開機秒數: 923.399

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 923.9039
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 925.13

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 926.131
MQTT Broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
50400
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機:     BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
Recive packet from 娃娃機: bytearray(b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd')
Recive 娃娃機 : 二、主控制\æ��台狀態

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 936.374
50304

```

- 把兩個檔案的 wifi 模組都封裝在 wifiManager 的記憶體狀態
  - main.py 連線沒問題
  - Data_Collection_Main.py 也讀的到這個 WIFImanager 實例
    - 這裡檔案到時候在 WIFImanager 實例加一個函式做失去連線的備援 reconnect()之類的
    - 讓他也需不用重啟?

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75568
讀取 Wi-Fi 設定: SSID=propsky
Tring to connect to : propsky ...
嘗試連線中... 1/10
嘗試連線中... 2/10
Wi-Fi 連線成功！
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -41 dBm
ESP OK
(2025, 2, 12, 10, 49, 11, 2, 43)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_class.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK

執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33328, free: 74704
 No. of 1-blocks: 326, 2-blocks: 89, max blk sz: 640, max free sz: 4067

stack: 1248 out of 15360
GC: total: 108032, used: 52192, free: 55840
 No. of 1-blocks: 519, 2-blocks: 152, max blk sz: 640, max free sz: 659

wifi_manager: <WiFiManager object at 3ffe53f0>
network_info:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'},propsky

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 39.824
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
1開機秒數: 39.855
2開機秒數: 39.856
3開機秒數: 39.856

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 40.361
Start to connect WiFi, SSID : propsky
Try to connect WiFi in 0s
WiFi connection OK!
Network Config= ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 42.198

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 43.199
MQTT Broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
50128
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機:     BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
Recive packet from 娃娃機: bytearray(b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd')
Recive 娃娃機 : 二、主控制\æ��台狀態

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 53.295
50016
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 02 00 AB

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x02\x00#')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 63.305
50016


```

## OTA test ok

## RTC 時間備援機制 ok

## max free sz

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6224, free: 101808
 No. of 1-blocks: 63, 2-blocks: 20, max blk sz: 78, max free sz: 5622
初始化 SPI 和 LCD...
LCD 初始化完成
73232
WiFi Signal Strength: -43 dBm
ESP OK
(2025, 2, 7, 17, 27, 7, 4, 38)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
(2025, 2, 7, 17, 27, 7, 4, 38)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_helper.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'utils.py', 'wifi.dat', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 37488, free: 70544
 No. of 1-blocks: 331, 2-blocks: 96, max blk sz: 640, max free sz: 3934

stack: 1248 out of 15360
GC: total: 108032, used: 56720, free: 51312
 No. of 1-blocks: 522, 2-blocks: 157, max blk sz: 640, max free sz: 391

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 1451.544

```
