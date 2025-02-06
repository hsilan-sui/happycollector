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