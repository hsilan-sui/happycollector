from machine import Timer, WDT
import gc

class TimerManager:
    def __init__(self, main_state, mqtt_manager, uart_manager, lcd_mgr, wdt, lcd_update_flag, claw_1):
        self.main_state = main_state
        self.mqtt_manager = mqtt_manager
        self.uart_manager = uart_manager
        self.lcd_mgr = lcd_mgr
        self.wdt = wdt
        self.lcd_update_flag = lcd_update_flag
        self.claw_1 = claw_1
        self.server_report_sales_period = 180
        self.server_report_sales_counter = self.server_report_sales_period - 30

        self.server_report_timer = Timer(0)
        self.claw_check_timer = Timer(1)
        self.lcd_update_timer = Timer(2)

    def server_report_timer_callback(self, timer):
        try:
            self.mqtt_manager.check_messages()
        except OSError:
            print("WiFi is disconnect")
            self.main_state.transition('WiFi is disconnect')
            self.mqtt_manager.reconnect_mqtt()
            return

        self.server_report_sales_counter = (self.server_report_sales_counter + 1) % self.server_report_sales_period
        if self.server_report_sales_counter == 0:
            self.wdt.feed()
            if self.main_state.state in [4, 5]:
                self.mqtt_manager.mqtt_handler.publish_MQTT_claw_data('sales')
            self.mqtt_manager.mqtt_handler.publish_MQTT_claw_data('status')
        gc.collect()

    def claw_check_timer_callback(self, timer):
        #global counter_of_WAITING_FEILOLI
        if now_main_state.state == MainStatus.NONE_FEILOLI:
            print("Updating 娃娃機 機台狀態 ...")
            #uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Machine_status)
            uart_manager.send_packet(KindFEILOLIcmd.Ask_Machine_status)

        elif now_main_state.state == MainStatus.STANDBY_FEILOLI:
            print("Updating 娃娃機 遠端帳目、投幣帳目 ...")
            #uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Transaction_account)
            uart_manager.send_packet(KindFEILOLIcmd.Ask_Transaction_account)
            # uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Coin_account)
            now_main_state.transition('FEILOLI UART is waiting')
            counter_of_WAITING_FEILOLI = 0

        if now_main_state.state == MainStatus.WAITING_FEILOLI:
            counter_of_WAITING_FEILOLI = counter_of_WAITING_FEILOLI + 1
            if counter_of_WAITING_FEILOLI >= 2:
                if counter_of_WAITING_FEILOLI == 2:
                    print("Updating 娃娃機 失敗 ...")
                    now_main_state.transition('FEILOLI UART is not OK')
                print("Updating 娃娃機 機台狀態 ...")
                #uart_FEILOLI_send_packet(KindFEILOLIcmd.Ask_Machine_status)
                uart_manager.send_packet(KindFEILOLIcmd.Ask_Machine_status)

    def lcd_update_timer_callback(self, timer):
        import binascii
        import machine
        if LCD_update_flag['Uniform']:
            LCD_update_flag['Uniform'] = False
            unique_id_hex = binascii.hexlify(machine.unique_id()).decode().upper()

            # 清空屏幕並繪製基本資訊
            lcd_mgr.fill()  # 使用黑色清空整個畫面

            lcd_mgr.draw_text(0, 0, text='Happy Collector', bg=lcd_mgr.color.BLUE, bgmode=-1)

            lcd_mgr.draw_text(5, 8 * 16 + 5, text=unique_id_hex, fg=lcd_mgr.color.RED, bg=lcd_mgr.color.WHITE,bgmode=-1, scale=1.3)


            lcd_mgr.draw_text(0, 1 * 16, text='IN:--------', fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
            lcd_mgr.draw_text(0, 2 * 16, text='OUT:--------')
            lcd_mgr.draw_text(0, 3 * 16, text='EP:--------')
            lcd_mgr.draw_text(0, 4 * 16, text='GP:--------')
            lcd_mgr.draw_text(0, 5 * 16, text='ST:--')
            lcd_mgr.draw_text(0, 6 * 16, text='Time:mm/dd hh:mm')
            lcd_mgr.draw_text(0, 7 * 16, text='Wifi:-----')
            
        elif LCD_update_flag['WiFi']:
            LCD_update_flag['WiFi'] = False
            if now_main_state.state == MainStatus.NONE_WIFI or now_main_state.state == MainStatus.NONE_INTERNET:
                #顯示wifi和MQTT狀態
                lcd_mgr.draw_text(5*8, 7*16, text='dis  ',fg=lcd_mgr.color.RED, bg=lcd_mgr.color.BLACK, bgmode=-1)
            elif now_main_state.state == MainStatus.NONE_MQTT:
                #顯示wifi和MQTT狀態
                lcd_mgr.draw_text(5*8, 7*16, text='error',fg=lcd_mgr.color.RED, bg=lcd_mgr.color.BLACK, bgmode=-1)
            elif now_main_state.state == MainStatus.NONE_FEILOLI or now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
                #顯示wifi和MQTT狀態
                lcd_mgr.draw_text(5*8, 7*16, text='OK   ',fg=lcd_mgr.color.GREEN, bg=lcd_mgr.color.BLACK, bgmode=-1)

        elif LCD_update_flag['Claw_State']:
            LCD_update_flag['Claw_State'] = False  
            if now_main_state.state == MainStatus.NONE_FEILOLI :
                lcd_mgr.draw_text(3 * 8, 5 * 16, text="%02d" % 99)   
                #顯示娃娃機狀態
            elif now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
                lcd_mgr.draw_text(3 * 8, 5 * 16, text="%02d" % claw_1.Error_Code_of_Machine)
                #顯示娃娃機狀態
            else:
                lcd_mgr.draw_text(3 * 8, 5 * 16, text="--")

        elif LCD_update_flag['Claw_Value']:
            LCD_update_flag['Claw_Value'] = False
            if now_main_state.state == MainStatus.STANDBY_FEILOLI or now_main_state.state == MainStatus.WAITING_FEILOLI:
                lcd_mgr.draw_text(3 * 8, 1 * 16, text="%-8d" % claw_1.Number_of_Coin, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
                lcd_mgr.draw_text(4 * 8, 2 * 16, text="%-8d" % claw_1.Number_of_Award, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
                lcd_mgr.draw_text(3 * 8, 3 * 16, text="%-8d" % claw_1.Number_of_Original_Payment, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
                lcd_mgr.draw_text(3 * 8, 4 * 16, text="%-8d" % claw_1.Number_of_Gift_Payment, fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)

        elif (LCD_update_flag['Time']):
            LCD_update_flag['Time'] = False  
            # 获取当前时间戳
            timestamp = utime.time()
            # 转换为本地时间
            local_time = utime.localtime(timestamp)
            # 格式化为 "mm/dd hh:mm" 格式的字符串
            formatted_time = "{:02d}/{:02d} {:02d}:{:02d}".format(local_time[1], local_time[2], local_time[3], local_time[4])
            lcd_mgr.draw_text(5 * 8, 6 * 16, text=formatted_time,fg=lcd_mgr.color.WHITE, bg=lcd_mgr.color.BLACK, bgmode=-1)
            #顯示時間
        lcd_mgr.show()
        gc.collect()

    def start_timers(self):
        self.server_report_timer.init(period=1000, mode=Timer.PERIODIC, callback=self.server_report_timer_callback)
        self.claw_check_timer.init(period=10000, mode=Timer.PERIODIC, callback=self.claw_check_timer_callback)
        self.lcd_update_timer.init(period=1000, mode=Timer.PERIODIC, callback=self.lcd_update_timer_callback)
        gc.collect()
