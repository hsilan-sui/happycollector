import machine
#待優化為工具函式
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
        machine.reset()