import os

def get_wifi_signal_strength(wlan):
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
    

# http備援(uscoket寫法)
# urequests的寫法(待測)
def get_http_time():
    import usocket
    from machine import RTC
    try:
        # ex:[(2, 1, 6, '', ('142.250.190.196', 80))]
        addr = usocket.getaddrinfo("www.google.com", 80)[0][-1]
        # 建立 TCP 連線
        s = usocket.socket() #建立一個 TCP socket 物件
        s.connect(addr) #連線到 www.google.com，埠號 80（HTTP）
        # 發送head請求(輕量 ) #scoket傳輸
        s.send(b"HEAD / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n")
        # 接收+解析伺服器回應
        ## recv(512) 最多 512 字節 的資料（將接收到的二進位資料轉換為 UTF-8 文字)
        response = s.recv(512).decode("utf-8")  # **減少 buffer，節省 RAM**
        # 關閉 TCP 連線，釋放資源
        s.close()

        for line in response.split("\r\n"):
            if line.startswith("Date: "):
                date_str = line[6:].strip()
                print("Google 時間:", date_str)

                try:
                    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
                    
                    parts = date_str.split(" ")
                    day, month, year = int(parts[1]), months[parts[2]], int(parts[3])
                    hour, minute, second = map(int, parts[4].split(":")) 

                    # 轉換 UTC → 台北時間 (UTC+8)
                    hour += 8
                    if hour >= 24:
                        hour -= 24
                        day += 1  

                        if month in [4, 6, 9, 11] and day > 30:  # **30 天的月份**
                            day, month = 1, month + 1
                        elif month == 2 and day > 28:  # **2 月 (簡化處理，假設不考慮閏年)**
                            day, month = 1, 3
                        elif day > 31:  # **31 天的月份 & 跨年**
                            day, month = 1, (month + 1) if month < 12 else (1, year + 1)

                    # RTC
                    RTC().datetime((year, month, day, 0, hour, minute, second, 0))
                    print(f"ESP32 時間已更新: {year}-{month}-{day} {hour}:{minute}:{second}")
                    return True
                except Exception as e:
                    print("解析時間失敗:", e)
                    return None
        print("無法獲取 Google 時間")
        return None
    except Exception as e:
        print("Google 時間 API 失敗:", e)
        return None

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