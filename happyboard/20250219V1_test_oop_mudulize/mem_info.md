# mem_info

## 執行緒啟動成功但從遠端 mqtt 發布消息 牽涉 uart 會發生 stackover flow 的問題

- 試著加入互斥鎖來守住這個執行緒 設置 stack_size 大小
  - 開機後有自動呈報 sales 的情況
  -

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
WiFi Signal Strength: -51 dBm
ESP OK
(2025, 2, 17, 17, 49, 43, 0, 48)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_handler.py', 'uart_manager.py', 'utils.py', 'wifi.dat', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33456, free: 74576
 No. of 1-blocks: 330, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 44112, free: 63920
 No. of 1-blocks: 432, 2-blocks: 110, max blk sz: 640, max free sz: 2474
debug flag 1
debug flag 2
debug flag 3
debug flag 4

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 129.493
1開機秒數: 129.494
2開機秒數: 129.496
3開機秒數: 129.498

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
GC: total: 108032, used: 69840, free: 38192
 No. of 1-blocks: 800, 2-blocks: 205, max blk sz: 640, max free sz: 1996
執行緒開始
stack: 1184 out of 15360
GC: total: 108032, used: 63136, free: 44896
 No. of 1-blocks: 667, 2-blocks: 187, max blk sz: 640, max free sz: 1996
debug: [啟動執行緒]: 1073508000
debug: [uart_manager.receive_packet 執行緒啟動中..]:
debug: [UART 設定] UART(2, baudrate=19200, bits=8, parity=None, stop=1, tx=17, rx=16, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=1)

now_main_state: WiFi is disconnect, 開機秒數: 132.204
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 133.329

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 134.397
MQTT broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota
debug: [Step 5: MQTT 訂閱主題]
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
44528
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB
DEBUG: Received Raw Data 收到執行緒receive_packet: b'-\x8a\x81\x01\x01\xff\x00\x00\x00\x00\x00\x00\x08\x01\x00\xdd'
debug: 收到有效封包: 2D 8A 81 01 01 FF 00 00 00 00 00 00 08 01 00 DD
debug: 解析uart封包ing: 2D 8A 81 01 01 FF 00 00 00 00 00 00 08 01 00 DD
Recive 娃娃機 : 二、主控制\æ��台狀態

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 81 01 01 FF 00 00 00 00 00 00 08 01 00 DD

now_main_state: FEILOLI UART is OK, 開機秒數: 144.767
44128
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機: BB 73 02 01 00 00 00 00 00 00 00 00 00 02 00 AB

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
DEBUG: Received Raw Data 收到執行緒receive_packet: b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x02\x00#'
debug: 收到有效封包: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 02 00 23
debug: 解析uart封包ing: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 02 00 23
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 82 01 00 00 00 00 00 00 00 00 08 02 00 23

now_main_state: FEILOLI UART is OK, 開機秒數: 154.769
44128
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機: BB 73 02 01 00 00 00 00 00 00 00 00 00 03 00 AA

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
DEBUG: Received Raw Data 收到執行緒receive_packet: b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x03\x00"'
debug: 收到有效封包: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 03 00 22
debug: 解析uart封包ing: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 03 00 22
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 82 01 00 00 00 00 00 00 00 00 08 03 00 22

now_main_state: FEILOLI UART is OK, 開機秒數: 164.769
44128
MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/sales
MQTT Publish data(JSON_str): {"Giftplaytimes": 0, "GiftOuttimes": 0, "Freeplaytimes": 0, "time": 793129837, "Epayplaytimes": 0, "Coinplaytimes": 0}
MQTT Publish Successful
無此MQTT發佈的API: status
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機: BB 73 02 01 00 00 00 00 00 00 00 00 00 04 00 AD

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
DEBUG: Received Raw Data 收到執行緒receive_packet: b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x04\x00%'
debug: 收到有效封包: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 04 00 25
debug: 解析uart封包ing: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 04 00 25
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 82 01 00 00 00 00 00 00 00 00 08 04 00 25

now_main_state: FEILOLI UART is OK, 開機秒數: 175.291
44416
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機: BB 73 02 01 00 00 00 00 00 00 00 00 00 05 00 AC

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
DEBUG: Received Raw Data 收到執行緒receive_packet: b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x05\x00$'
debug: 收到有效封包: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 05 00 24
debug: 解析uart封包ing: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 05 00 24
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 82 01 00 00 00 00 00 00 00 00 08 05 00 24

now_main_state: FEILOLI UART is OK, 開機秒數: 185.314
44416
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機: BB 73 02 01 00 00 00 00 00 00 00 00 00 06 00 AF

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
DEBUG: Received Raw Data 收到執行緒receive_packet: b"-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x06\x00'"
debug: 收到有效封包: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 06 00 27
debug: 解析uart封包ing: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 06 00 27
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 82 01 00 00 00 00 00 00 00 00 08 06 00 27

now_main_state: FEILOLI UART is OK, 開機秒數: 195.333
44416
Updating 娃娃機 遠端帳目、投幣帳目 ...
Sent packet to 娃娃機: BB 73 02 01 00 00 00 00 00 00 00 00 00 07 00 AE

Action: FEILOLI UART is waiting, MainStatus: WAITING_FEILOLI
DEBUG: Received Raw Data 收到執行緒receive_packet: b'-\x8a\x82\x01\x00\x00\x00\x00\x00\x00\x00\x00\x08\x07\x00&'
debug: 收到有效封包: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 07 00 26
debug: 解析uart封包ing: 2D 8A 82 01 00 00 00 00 00 00 00 00 08 07 00 26
Recive 娃娃機 : 三、 帳目查詢=>遠端帳目

Action: FEILOLI UART is OK, MainStatus: STANDBY_FEILOLI
debug: 已發送給解析封包 parse_packet 功能去了 2D 8A 82 01 00 00 00 00 00 00 00 00 08 07 00 26

now_main_state: FEILOLI UART is OK, 開機秒數: 205.767
44128
```

## 確認有沒有啟動執行緒

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
WiFi Signal Strength: -44 dBm
ESP OK
(2025, 2, 17, 11, 9, 13, 0, 48)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_helper.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_handler.py', 'uart_manager.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33392, free: 74640
 No. of 1-blocks: 331, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 44096, free: 63936
 No. of 1-blocks: 434, 2-blocks: 111, max blk sz: 640, max free sz: 2475
debug flag 1
debug flag 2
debug flag 3
debug flag 4

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 79.101
1開機秒數: 79.101
2開機秒數: 79.104
3開機秒數: 79.10501

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
GC: total: 108032, used: 68816, free: 39216
 No. of 1-blocks: 794, 2-blocks: 208, max blk sz: 640, max free sz: 2072
執行緒開始
debug: [啟動執行緒]: 1073508000
DEBUG: Data available in UART buffer
DEBUG: No data received from UART
debug: [UART 設定] UART(2, baudrate=19200, bits=8, parity=None, stop=1, tx=17, rx=16, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=1)
執行失敗，改跑Data_Collection_Main.mpy 'UART' object has no attribute 'tx'
stack: 1376 out of 15360
GC: total: 108032, used: 77600, free: 30432
 No. of 1-blocks: 901, 2-blocks: 232, max blk sz: 640, max free sz: 373
debug flag 1
debug flag 2
debug flag 3
debug flag 4

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 85.062
1開機秒數: 85.06301
2開機秒數: 85.066
3開機秒數: 85.06801

Init, MainStatus: NONE_WIFI
debug: [Step 1: 初始化 UART Handler]
debug: [Step 2: 初始化 UART Manager]
```

## 一堆有 bug

- lcd 沒有顯示值 沒有獨到 claw_1
- receive_packet 沒有運作
  送 clawreboot 指令 會發生以下 (mqtt 回報 ok)
- mqtt received new topic
  MQTT Subscribe topic: b'3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands'
  MQTT Subscribe data(JSON_str): b'{\n"commands":"clawreboot",\n"state" : "3d64d18f-aa0b-4735-b1f2-bd549531feb0",\n"time":15000\n}'
  MQTT Subscribe data (parsed): {'time': 15000, 'commands': 'clawreboot', 'state': '3d64d18f-aa0b-4735-b1f2-bd549531feb0'}
  MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commandack-clawreboot
  MQTT Publish data(JSON_str): {"ack": "OK", "state": "3d64d18f-aa0b-4735-b1f2-bd549531feb0", "time": 792859299}
  MQTT Publish Successful
  MQTT 回調函式錯誤: 'NoneType' object has no attribute 'send_packet'
- 送 clawstartgame (mqtt 回報 ok)
- Updating 娃娃機 機台狀態 ...
  Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 73 00 D9
  mqtt received new topic
  MQTT Subscribe topic: b'3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands'
  MQTT Subscribe data(JSON_str): b'{\n"commands":"clawstartgame",\n"epays":1, \n"freeplays":10,\n"time":15000,\n"state" : "3d64d18f-aa0b-4735-b1f2-bd549531feb0"\n}'
  MQTT Subscribe data (parsed): {'state': '3d64d18f-aa0b-4735-b1f2-bd549531feb0', 'commands': 'clawstartgame', 'freeplays': 10, 'time': 15000, 'epays': 1}
  MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commandack-clawstartgame
  MQTT Publish data(JSON_str): {"ack": "OK", "state": "3d64d18f-aa0b-4735-b1f2-bd549531feb0", "time": 792859368}
  MQTT Publish Successful
  Error handling clawstartgame: 'NoneType' object has no attribute 'send_packet'
  debug: 有完成發送 MQTT 主題

- 送 clawcleantransaccount (mqtt 回報 is ok)
- now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 4147.595
  46032
  mqtt received new topic
  MQTT Subscribe topic: b'3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands'
  MQTT Subscribe data(JSON_str): b'{\n"commands":"clawcleantransaccount",\n"account":"Epayplaytimes, Coinplaytimes, Giftplaytimes, GiftOuttimes",\n"state" : "3d64d18f-aa0b-4735-b1f2-bd549531feb0",\n"time": 15000\n}'
  MQTT Subscribe data (parsed): {'account': 'Epayplaytimes, Coinplaytimes, Giftplaytimes, GiftOuttimes', 'commands': 'clawcleantransaccount', 'state': '3d64d18f-aa0b-4735-b1f2-bd549531feb0', 'time': 15000}
  MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commandack-clawcleantransaccount
  MQTT Publish data(JSON_str): {"ack": "OK", "state": "3d64d18f-aa0b-4735-b1f2-bd549531feb0", "time": 792859491}
  MQTT Publish Successful
  MQTT 回調函式錯誤: 'NoneType' object has no attribute 'send_packet'
  Updating 娃娃機 機台狀態 ...
  Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 80 00 2A

- 送 clawmachingsetting (claw_1 沒有讀值 顯示在螢幕上 | )
- mqtt received new topic
  MQTT Subscribe topic: b'3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands'
  MQTT Subscribe data(JSON_str): b'{\n"commands":"clawmachinesetting",\n"setting":"BasicsettingA",\n"state" : "3d64d18f-aa0b-4735-b1f2-bd549531feb0",\n"time": 15000\n}'
  MQTT Subscribe data (parsed): {'time': 15000, 'commands': 'clawmachinesetting', 'state': '3d64d18f-aa0b-4735-b1f2-bd549531feb0', 'setting': 'BasicsettingA'}
  MQTT 回調函式錯誤: 'NoneType' object has no attribute 'send_packet'

- 沒有自動上報 mqtt sales 參數

```bash
MPY: soft reboot
stack: 640 out of 15360
GC: total: 108032, used: 6704, free: 101328
 No. of 1-blocks: 72, 2-blocks: 24, max blk sz: 81, max free sz: 5548
初始化 SPI 和 LCD...
LCD 初始化完成
75488
讀取 Wi-Fi 設定: SSID=propsky
Wi-Fi connected!
Network config: ('192.168.2.182', '255.255.255.0', '192.168.2.1', '8.8.8.8')
網路資料:{'ip': '192.168.2.182', 'mac': '3CE90E4DD7E4'}
WiFi Signal Strength: -36 dBm
ESP OK
(2025, 2, 14, 14, 23, 16, 4, 45)
NTP 時間同步成功，使用 clock.stdtime.gov.tw
['BN165DKBDriver.py', 'Data_Collection_Main.py', 'boot.py', 'lcd_manager.py', 'main.py', 'mqtt_handler.py', 'mqtt_manager.py', 'received_claw_data.py', 'senko.py', 'token.dat', 'uart_handler.py', 'uart_manager.py', 'utils.py', 'wifi.dat', 'wifiManager.py', 'wifi_manager.py', 'wifimgr.py']
OTA檔案不存在
ESP OTA OK
執行Data_Collection_Main.py...
stack: 640 out of 15360
GC: total: 108032, used: 33536, free: 74496
 No. of 1-blocks: 335, 2-blocks: 89, max blk sz: 640, max free sz: 4067
stack: 1184 out of 15360
GC: total: 108032, used: 43952, free: 64080
 No. of 1-blocks: 433, 2-blocks: 108, max blk sz: 640, max free sz: 2523
debug flag 1
debug flag 2
debug flag 3
debug flag 4

開始執行Data_Collection_Main初始化，版本為: V1.07b3_sui
開機秒數: 2869.545
1開機秒數: 2869.546
2開機秒數: 2869.548
3開機秒數: 2869.55

Init, MainStatus: NONE_WIFI
debug: [Step 1: 初始化 UART Handler]
debug: [Step 2: 初始化 UART Manager]
wifi_manager: <WiFiManager object at 3ffe53f0>
V1.07b3_sui
3CE90E4DD7E4
debug: [Step 3: 初始化 MQTT Manager | MqttHandler也在其中初始化]
Get token: 445ccb69-2923-4f8f-b7d5-484132226ebe
debug: [Step 4: 解決相互依賴]
DEBUG: Data available in UART buffer
DEBUG: No data received from UART

now_main_state: WiFi is disconnect, 開機秒數: 2870.131
My IP Address: 192.168.2.182
My MAC Address: 3CE90E4DD7E4

Action: WiFi is OK, MainStatus: NONE_INTERNET

now_main_state: WiFi is OK, 開機秒數: 2871.316

Action: Internet is OK, MainStatus: NONE_MQTT
now_main_state: Internet is OK, 開機秒數: 2872.317
MQTT broker connection OK!
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota
debug: [Step 5: MQTT 訂閱主題]
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands
MQTT Subscribe topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/fota

Action: MQTT is OK, MainStatus: NONE_FEILOLI
46048
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 01 00 AB

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2882.544
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 02 00 A8

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2892.56
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 03 00 A9

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2902.577
46032
Traceback (most recent call last):
  File "Data_Collection_Main.py", line 481, in server_report_timer_callback
  File "mqtt_handler.py", line 153, in publish_MQTT_claw_data
AttributeError: 'ReceivedClawData' object has no attribute 'startswith'
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 04 00 AE

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2912.59
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 05 00 AF

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2922.603
46032
mqtt received new topic
MQTT Subscribe topic: b'3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commands'
MQTT Subscribe data(JSON_str): b'{\n"commands":"clawstartgame",\n"epays":1,   \n"freeplays":2,\n"time":15000,\n"state" : "3d64d18f-aa0b-4735-b1f2-bd549531feb0"\n}'
MQTT Subscribe data (parsed): {'state': '3d64d18f-aa0b-4735-b1f2-bd549531feb0', 'commands': 'clawstartgame', 'freeplays': 2, 'time': 15000, 'epays': 1}
MQTT Publish topic: 3CE90E4DD7E4/445ccb69-2923-4f8f-b7d5-484132226ebe/commandack-clawstartgame
MQTT Publish data(JSON_str): {"ack": "OK", "state": "3d64d18f-aa0b-4735-b1f2-bd549531feb0", "time": 792858265}
MQTT Publish Successful
Error handling clawstartgame: 'NoneType' object has no attribute 'send_packet'
debug: 有完成發送MQTT主題
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 06 00 AC

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2932.96
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 07 00 AD

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2942.972
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 08 00 A2

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2952.984
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 09 00 A3

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2962.996
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 0A 00 A0

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2973.008
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 0B 00 A1

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2983.021
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 0C 00 A6

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 2993.033
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 0D 00 A7

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 3003.045
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 0E 00 A4

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 3013.058
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 0F 00 A5

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 3023.07
46032
Updating 娃娃機 機台狀態 ...
Sent packet to 娃娃機: BB 73 01 01 00 00 00 00 00 00 00 00 00 10 00 BA

now_main_state: MQTT is OK (FEILOLI UART is not OK), 開機秒數: 3033.083
46032
```

## uart_manager 與 uart_handler <==> mqtt_manager 與 mqtt_handler

- 初始化先後順序的問題 架構大致如下：

  - MqttManager 需要 UartManager，因為 MQTT 指令有時會透過 UART 發送指令給娃娃機
  - UartManager 需要 UartHandler，因為 UART 回傳的封包需要由 UartHandler 解析
  - MqttHandler 需要 MqttManager，因為 需要訂閱 MQTT 主題
  - MqttHandler 需要 UartManager，因為 MQTT 指令有時要轉為 UART 命令 ====>這裡出現 BUG
  - UartHandler 需要 MqttHandler，因為 UART 接收到的資料有時要發送到 MQTT

- 這樣的架構會有 循環依賴 (circular dependency) 的問題，因此需要調整 初始化順序。

- 分析依賴關係最少的物件 要先初始化
  按照「依賴關係最少的物件先初始化」的原則來調整順序：

- 初始化 UartHandler (它只依賴 claw_1，無其他依賴)
- 初始化 UartManager (它需要 UartHandler)
- 初始化 MqttManager (它不直接依賴 UartManager，但稍後要傳入)
- 初始化 MqttHandler (它需要 MqttManager 和 UartManager)
- 將 UartManager 傳入 MqttManager（確保 MQTT 可以發送 UART 指令）

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
