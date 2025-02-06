import network # 配置WiFi接口
import socket
import ure
import utime
import binascii
import machine
import random

## AP 基地台(我手機分享網路的概念)
## STA 工作站(我現在筆電的概念)
## AP+STA

# 透過 machine.unique_id() 獲取硬體唯一 ID，並組合成一個獨特的 SSID 和 DHCP 名稱
unique_id_hex = binascii.hexlify(machine.unique_id()[-3:]).decode().upper()
ap_ssid = "HappyWifi" + unique_id_hex
ap_password = "happywifi"

DHCP_NAME = "Happy_" + unique_id_hex

ap_authmode = 3  # WPA2

NETWORK_PROFILES = 'wifi.dat'

# 1.network.WLAN()建立網路連線的對象 (配置WiFi街口)
# #預設是network.STA_IF 用戶端
## 參數支援:network.AP_IF 以及 network.STA_IF 用戶端
wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

# 2. 使用.active()啟動上述所配置的接口
# 3. 使用.connect(ssid, pwd)建立連線
# 4. ifconfig()顯示連線的ip位置(ip,子網路遮罩,閘道,DNS伺服器)
server_socket = None

# 自動連線Wi-Fi
def get_connection():
    """嘗試連接已知 Wi-Fi，若失敗則啟用 AP 模式"""

    # 確認network.STA_IF 用戶端是否存在
    if wlan_sta.isconnected():
        return wlan_sta

    connected = False
    max_retries = 999999 
    retry_delay_range = (5, 15)  # Range of delay in seconds between retries

    for _ in range(max_retries):
        try:
            # ESP connecting to WiFi takes time, wait a bit before retrying:
            utime.sleep(random.randint(*retry_delay_range))
            
            # 確認network.WLAN(network.STA_IF)建立網路連線的對象 (配置WiFi接口)是否已存在
            if wlan_sta.isconnected():
                connected = True # 旗標
                break
            
            # 從檔案讀取已知的 Wi-Fi 設定
            profiles = read_profiles()

            # 2. 使用.active()啟動上述所配置的接口
            wlan_sta.active(True)
            # 掃描周遭可用的wifi
            networks = wlan_sta.scan()
            #存入物件裡 
        # {propsky: wifi.dat的pas, 
        #   name: propsky}
       # profiles[ssid] = password
        #profiles["name"] = ssid
            connected = do_connect(profiles["name"], profiles[profiles["name"]])

        except OSError as e:
            print("exception", str(e))

        if connected:
            break
        
        print("no wifi try again")

    # If still not connected, start web server for connection manager:
    if not connected:
        connected = start()

    return wlan_sta if connected else None

#讀取wifi設定:從本地檔案讀取 SSID 和密碼，返回一個字典
def read_profiles():
    #TWORK_PROFILES => 'wifi.dat'
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        # 從wifi.dat讀取 ssid;password
        ssid, password = line.strip("\n").split(";")
        #存入物件裡 
        # {propsky: wifi.dat的pas, 
        #   name: propsky}
        profiles[ssid] = password
        profiles["name"] = ssid
    return profiles

#寫入wifi設定:將新的 Wi-Fi 設定寫入檔案
def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))


def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None 
    print('Trying to connect to %s...' % ssid)
    wlan_sta.config(dhcp_hostname=DHCP_NAME)
    wlan_sta.connect(ssid, password)
    for retry in range(200):
        connected = wlan_sta.isconnected()
        if connected:
            break
        utime.sleep(0.1)
        print('.', end='')
    if connected:
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
        
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

def send_header(client, status_code=200, content_length=None ):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
      client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")


def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()


def handle_root(client):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    send_header(client)
    client.sendall("""\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Wi-Fi Client Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """)
    while len(ssids):
        ssid = ssids.pop(0)
        client.sendall("""\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid))
    client.sendall("""\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
        </html>
    """ )
    client.close()


def handle_configure(client, request):
    match = ure.search("ssid=([^&]*)&password=(.*)", request)

    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return False
    # version 1.9 compatibility
    try:
        ssid = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
    except Exception:
        ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
        password = match.group(2).replace("%3F", "?").replace("%21", "!")

    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return False

    if do_connect(ssid, password):
        response = """\
            <html>
                <center>
                    <br><br>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP successfully connected to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client, response)
        utime.sleep(1)
        wlan_ap.active(False)
        try:
            profiles = read_profiles()
        except OSError:
            profiles = {}
        profiles[ssid] = password
        write_profiles(profiles)

        utime.sleep(5)

        return True
    else:
        response = """\
            <html>
                <center>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP could not connect to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                    <form>
                        <input type="button" value="Go back!" onclick="history.back()"></input>
                    </form>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client, response)
        return False


def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None

# 啟用 AP 模式
def start(port=80):
    global server_socket

    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    stop()

    wlan_sta.active(True)
    wlan_ap.active(True)

    wlan_ap.config(essid=ap_ssid, password=ap_password, authmode=ap_authmode)

    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)

    print('Connect to WiFi ssid ' + ap_ssid + ', default password: ' + ap_password)
    print('and access the ESP via your favorite web browser at 192.168.4.1.')
    print('Listening on:', addr)

    while True:
        if wlan_sta.isconnected():
            wlan_ap.active(False)
            return True

        client, addr = server_socket.accept()
        print('client connected from', addr)
        try:
            client.settimeout(5.0)

            request = b""
            try:
                while "\r\n\r\n" not in request:
                    request += client.recv(512)
            except OSError:
                pass

            # Handle form data from Safari on macOS and iOS; it sends \r\n\r\nssid=<ssid>&password=<password>
            try:
                request += client.recv(1024)
                print("Received form data after \\r\\n\\r\\n(i.e. from Safari on macOS or iOS)")
            except OSError:
                pass

            print("Request is: {}".format(request))
            if "HTTP" not in request:  # skip invalid requests
                continue

            # version 1.9 compatibility
            try:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
            print("URL is {}".format(url))

            if url == "":
                handle_root(client)
            elif url == "configure":
                handle_configure(client, request)
            else:
                handle_not_found(client, url)

        finally:
            client.close()

