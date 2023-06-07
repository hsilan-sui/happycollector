# Happy Collector

資料蒐集板

# 待做事項 To do list

## Sam
* 編寫好要更新的程式碼放在FotaReleaseCode
* main.py的108行working_dir，改成MQTT的FOTA指令提供
* 整理V1.02，並且Release到FotaReleaseCode的資料夾

## Thomas
* GET STATUS
* CMD ACK
* Data_Collection_Main.py可以相容 單吃Wifi檔，單獨跑
* MQTT封包的time


# 修改日誌 Modify log

## 2023/6/7_V1.02,  Thomas
* 完成ping-pong
* main while delay方式修改
* MQTT Publish中，Freeplaytimes不打負數
* server_check timer 改名成 server_report
負責每1秒鐘更新 MQTT Subscribe，每3分鐘做Publish
* MQTT Publish status改成跟MQTT Publish sales一起送，不理會getstatus的cmd
* 狀態轉換的class中，把noInternet修正好，之前沒改好。
正確是在main while中才做跳轉，不是在transition中跳轉
* 狀態機 print log的調整，狀態轉換時會做換行，增加易讀性
* 更新一些log的敘述

## 2023/6/7_V1.01
* Data_Collection_Main_0525v4RX_task.py改名成Data_Collection_Main.py
* 在程式碼標題打修改日期，版本號以此為V1.01開始 (內容和上版一樣2023/05/30_V1.0)

## 2023/6/7
* 從alpha複製出新的Thomas_Branch，調整資料夾位置和檔名