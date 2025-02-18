#　比對訊息

## 原先版本

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6816, free: 101216
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 82, max free sz: 5532
初始化 SPI 和 LCD...
LCD 初始化完成
72816
WiFi Signal Strength: -40 dBm
ESP OK
(2025, 2, 14, 14, 49, 59, 4, 45)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_handler.py', 'uart_manager.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 38112, free: 69920
 No. of 1-blocks: 348, 2-blocks: 98, max blk sz: 640, max free sz: 3901
stack: 1248 out of 15360
GC: total: 108032, used: 57408, free: 50624
 No. of 1-blocks: 539, 2-blocks: 159, max blk sz: 640, max free sz: 356

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 4468.913
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
1開機秒數: 4468.978
2開機秒數: 4468.978
3開機秒數: 4468.978

Init, MainStatus: NONE_WIFI

now_main_state: WiFi is disconnect, 開機秒數: 4469.483
Start to connect WiFi, SSID : propsky
Try to connect WiFi in 0s
WiFi connection OK!
Network Config= ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 4471.387

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 4472.389
MQTT Broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

##
# 所以oop那裏是這裡沒有發生 沒有action
# Sent packet to 娃娃機 (會先發送封包給娃娃機)
# Recive packet from 娃娃機 (收到封包從娃娃機)
##
Action: MQTT is OK, MainStatus: NONE_FEILOLI
46192
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機:     BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
Recive packet from 娃娃機: bytearray(b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd')
Recive 娃娃機 : 二、主控制\æ��台狀態

##
# 所以oop那裏是這裡沒有發生 沒有action
# Sent packet to 娃娃機 (會先發送封包給娃娃機)
# Recive packet from 娃娃機 (收到封包從娃娃機)
##
Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4482.483
46112
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 02 00 AB

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x02\x00#')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4492.661
46112
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 03 00 AA

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x03\x00"')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4502.97
46112
MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/sales
MQTT Publish data(JSON_str): {"Giftplaytimes": 0, "GiftOuttimes": 0, "Freeplaytimes": 0, "time": 792859848, "Epayplaytimes": 0, "Coinplaytimes": 0}
MQTT Publish Successful
MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/status
MQTT Publish data(JSON_str): {"time": 792859848, "wifirssi": -36, "status": "08"}
MQTT Publish Successful
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 04 00 AD


Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x04\x00%')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4512.97
39664
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 05 00 AC

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x05\x00$')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4522.981
39680
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 06 00 AF

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b"-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x06\x00'")
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4533.478
39680
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機:     BB 73 02 01 00 00 00 00 00 00 00 00 00 07 00 AE

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
Recive packet from 娃娃機: bytearray(b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x07\x00&')
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI

now_main_state: FEILOLI UART is OK, 開機秒數: 4543.478
39680


```

## 更改後的版本

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
WiFi Signal Strength: -44 dBm
ESP OK
(2025, 2, 14, 17, 11, 7, 4, 45)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_handler.py', 'uart_manager.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33392, free: 74640
 No. of 1-blocks: 331, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 43872, free: 64160
 No. of 1-blocks: 431, 2-blocks: 108, max blk sz: 640, max free sz: 2518
debug flag 1
debug flag 2
debug flag 3
debug flag 4

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 302.457
1開機秒數: 302.458
2開機秒數: 302.46
3開機秒數: 302.462

Init, MainStatus: NONE_WIFI
debug: [Step 1: 初始化 UART Handler]
debug: [Step 2: 初始化 UART Manager]
wifi_manager: <WiFiManager object at 3ffe53f0>
V1.07b3_sui
3CE90E4DD7E4
debug: [Step 3: 初始化 MQTT Manager | MqttHandler也在其中初始化]
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
debug: [Step 4: 解決相互依賴]
stack: 1184 out of 15360
GC: total: 108032, used: 68256, free: 39776
 No. of 1-blocks: 787, 2-blocks: 206, max blk sz: 640, max free sz: 2135
執行緒開始
DEBUG: Data available in UART buffer
DEBUG: No data received from UART

now_main_state: WiFi is disconnect, 開機秒數: 303.082
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 304.322

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 305.323
MQTT broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota
debug: [Step 5: MQTT 訂閱主題]
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

##
# 所以oop那裏是這裡沒有發生 沒有action
# Sent packet to 娃娃機 (會先發送封包給娃娃機)
# Recive packet from 娃娃機 (收到封包從娃娃機)
##

Action: MQTT is OK, MainStatus: NONE_FEILOLI
45984
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 315.488
45968
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 02 00 A8
##
# 所以oop那裏是這裡沒有發生 沒有action
# Sent packet to 娃娃機 (會先發送封包給娃娃機)
# Recive packet from 娃娃機 (收到封包從娃娃機)
##
now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 325.5
45968
```
