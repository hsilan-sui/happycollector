import os
import utime
from utils import get_wifi_signal_strength, get_file_info

##### 這裡跟subscribe_MQTT_claw_recive_callback 回調函式有關的

def process_fota(data, publish_func, claw):
    """
    處理 FOTA 邏輯。
    """
    otafile = 'otalist.dat'
    try:
        if 'file_list' in data and 'password' in data:
            if data['password'] == 'c0b82a2c-4b03-42a5-92cd-3478798b2a90':  # 驗證密碼
                publish_func(claw, 'fotaack')
                with open(otafile, 'w') as f:
                    f.write(''.join(data['file_list']))
                print("FOTA file saved. Rebooting...")
                utime.sleep(3)
                reset()
            else:
                print("Invalid FOTA password")
        else:
            print("Incomplete FOTA data received")
    except Exception as e:
        print(f"Error handling FOTA: {e}")


# 這裡要處理的傳參數比較多

def process_commands(data, publish_func, uart_func, claw, KindFEILOLIcmd=None):
    """
    處理指令邏輯，根據指令名稱分派至對應的處理函式。
    """
    # 指令映射表
    command_handlers = {
        'ping': handle_ping,
        'version': handle_version,
        'clawreboot': handle_claw_reboot,  # 需要 KindFEILOLIcmd
        'clawstartgame': handle_claw_start_game,  # 需要 KindFEILOLIcmd
        'clawcleantransaccount': handle_claw_clean_trans_account,  # 需要 KindFEILOLIcmd
        'clawmachinesetting': handle_claw_machine_setting,  # 需要 KindFEILOLIcmd
        'fileinfo': handle_file_commands,
        'fileremove': handle_file_commands,
    }

    # 取得指令名稱
    command = data.get('commands')
    handler = command_handlers.get(command)

    # 呼叫處理函式
    if handler:
        if command in ['clawreboot', 'clawstartgame', 'clawcleantransaccount', 'clawmachinesetting']:
            # 傳遞需要 KindFEILOLIcmd 的函式
            if KindFEILOLIcmd:
                handler(data, publish_func, uart_func, claw, KindFEILOLIcmd)
            else:
                print(f"Command {command} requires KindFEILOLIcmd but it was not provided.")
        else:
            # 不需要 KindFEILOLIcmd 的函式
            handler(data, publish_func, uart_func, claw)
    else:
        print(f"Unknown command: {command}")


# 個別指令處理函式
def handle_ping(data, publish_func, uart_func, claw):
    publish_func(claw, 'commandack-pong')


def handle_version(data, publish_func, uart_func, claw):
    publish_func(claw, 'commandack-version')


def handle_claw_reboot(data, publish_func, uart_func, claw, KindFEILOLIcmd):
    state = data.get('state', '')
    publish_func(claw, 'commandack-clawreboot', state)
    uart_func(KindFEILOLIcmd.Send_Machine_reboot)


def handle_claw_start_game(data, publish_func, uart_func, claw, KindFEILOLIcmd):
    try:
        state = data.get('state', '')
        epays = data.get('epays', 0)
        freeplays = data.get('freeplays', 0)

        if not (1 <= epays <= 40):
            raise ValueError(f"Invalid epays: {epays}")
        if not (0 <= freeplays <= 10):
            raise ValueError(f"Invalid freeplays: {freeplays}")

        game_data = {"epays": epays, "freeplays": freeplays}
        publish_func(claw, 'commandack-clawstartgame', state)
        uart_func(KindFEILOLIcmd.Send_Starting_once_game, game_data)
    except Exception as e:
        print(f"Error handling clawstartgame: {e}")


def handle_claw_clean_trans_account(data, publish_func, uart_func, claw, KindFEILOLIcmd):
    state = data.get('state', '')
    account = data.get('account', '').split(", ")
    publish_func(claw, 'commandack-clawcleantransaccount', state)
    uart_func(KindFEILOLIcmd.Send_Clean_transaction_account, account)


def handle_claw_machine_setting(data, publish_func, uart_func, claw, KindFEILOLIcmd):
    setting = data.get('setting', '').strip()
    valid_settings = ["BasicsettingA", "BasicsettingB", "BasicsettingC", "Clawvoltage", "Motorspeed"]
    if setting in valid_settings:
        uart_func(KindFEILOLIcmd.Ask_Machine_setting, setting)
    else:
        print(f"Invalid machine setting: {setting}")


def handle_file_commands(data, publish_func, uart_func, claw):
    command = data.get('commands')
    filename = data.get('filename', '')

    if command == 'fileinfo':
        publish_func(claw, 'commandack-fileinfo', filename)
    elif command == 'fileremove':
        publish_func(claw, 'commandack-fileremove', filename)


#####　這裡是跟publish_MQTT_claw_data(claw_1, MQTT_API_select, para1="")　發布消息的函式有關的


# 生成銷售數據
def build_sales_data(claw_data):
    WCU_Freeplaytimes = max(
        claw_data.Number_of_Total_games -
        claw_data.Number_of_Original_Payment -
        claw_data.Number_of_Coin -
        claw_data.Number_of_Gift_Payment,
        0
    )

    return {
        "Epayplaytimes": claw_data.Number_of_Original_Payment,
        "Coinplaytimes": claw_data.Number_of_Coin,
        "Giftplaytimes": claw_data.Number_of_Gift_Payment,
        "GiftOuttimes": claw_data.Number_of_Award,
        "Freeplaytimes": WCU_Freeplaytimes,
        "time": utime.time(),
    }

# 生成狀態數據
def build_status_data(claw_data, wifi_signal_strength):
    status_code = claw_data.Error_Code_of_Machine if claw_data else 99
    return {
        "status": f"{status_code:02d}",
        "wifirssi": wifi_signal_strength,
        "time": utime.time(),
    }

# 處理帶有 ACK 狀態的回應
def handle_ack_with_state(api_select, para1=None, version=''):
    # 這裡 VERSION 需在主程式中全域定義
    ack_value = {
        "commandack-pong": "pong",
        "commandack-version": version,
        "fotaack": "OK",
    }.get(api_select, "OK")
    return {
        "ack": ack_value,
        "state": para1,
        "time": utime.time(),
    }

# 生成機台設定數據
def build_clawmachinesetting_data(claw_data, para1):
    if para1 == "Clawvoltage":
        return {
            "HiVoltageValue": claw_data.Value_of_Hi_voltage,
            "MidVoltageValue": claw_data.Value_of_Mid_voltage,
            "LoVoltageValue": claw_data.Value_of_Lo_voltage,
            "MidVoltageTopDistance": claw_data.Distance_of_Mid_voltage_and_Top,
            "GuaranteedPrizeHiVoltage": claw_data.Hi_voltage_of_Guaranteed_prize,
            "time": utime.time(),
        }
    elif para1 == 'Motorspeed':
        return {
            "SpeedMovingforward": claw_data.Speed_of_Moving_forward,
            "SpeedMovingback": claw_data.Speed_of_Moving_back,
            "SpeedMovingleft": claw_data.Speed_of_Moving_left,
            "SpeedMovingright": claw_data.Speed_of_Moving_right,
            "SpeedMovingup": claw_data.Speed_of_Moving_up,
            "SpeedMovingdown": claw_data.Speed_of_Moving_down,
            "RPMAllhorizontalsides": claw_data.RPM_of_All_horizontal_sides,
            "time": utime.time(),
        }
    elif para1 == 'BasicsettingA':  # 基本設定 A
        return {
            "TimeOfGame": claw_data.Time_of_game,  # 遊戲時間
            "AmountOfAward": claw_data.Amount_of_Award,  # 禮品售價
            "AmountOfPresentCumulation": claw_data.Amount_of_Present_cumulation,  # 目前累加金額
            "TimeOfKeepingCumulation": claw_data.Time_of_Keeping_cumulation,  # 累加保留時間
            "TimeOfShowMusic": claw_data.Time_of_Show_music,  # 展示音樂時間
            "EnableOfMidairGrip": claw_data.Enable_of_Midair_Grip,  # 空中取物
            "time": utime.time()
        }
    elif para1 == 'BasicsettingB':  # 基本設定 B
        return {
            "DelayofPushtalon": claw_data.Delay_of_Push_talon,  # 下抓延遲
            "DelayofSuspendpulledtalon": claw_data.Delay_of_Suspend_pulled_talon,  # 上停延遲
            "EnablerandomofPushingtalon": claw_data.Enable_random_of_Pushing_talon,  # 下抓夾亂數
            "EnablerandomofClamping": claw_data.Enable_random_of_Clamping,  # 夾亂數
            "TimeofPushtalon": claw_data.Time_of_Push_talon,  # 下抓長度時間
            "TimeofSuspendandPulltalon": claw_data.Time_of_Suspend_and_Pull_talon,  # 上停上拉時間
            "DelayofPulltalon": claw_data.Delay_of_Pull_talon,  # 上拉延遲
            "time": utime.time()
        }
    elif para1 == 'BasicsettingC':  # 基本設定 C
        return {
            "Enable_of_Sales_promotion": claw_data.Enable_of_Sales_promotion,  # 促銷功能
            "Which_number_starting_when_Sales_promotion": claw_data.Which_number_starting_when_Sales_promotion,  # 促銷功能第幾局
            "Number_of_Strong_grip_when_Sales_promotion": claw_data.Number_of_Strong_grip_when_Sales_promotion,  # 促銷功能強抓次數
            "time": utime.time()
        }
    else:
        return {
            "ack": "wrong!!only_do_one_cmd", 
            "state": para1, 
            "time": utime.time()
        }

# 生成文件資訊數據
def build_fileinfo_data(filename):
    file_size, file_mtime = get_file_info(filename)
    file_date = "N/A"
    file_exist = 0

    if file_size is not None:
        file_exist = 1
        if file_mtime is not None:
            local_time = utime.localtime(file_mtime)
            file_date = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5]
            )
    return {
        "ack": "OK",
        "exist": file_exist,
        "date": file_date,
        "size": file_size or 0,
        "time": utime.time(),
    }

# 生成文件刪除結果數據
def build_fileremove_data(filename):
    result = "NO FILE!"
    try:
        if filename != "main.py":
            os.remove(filename)
            result = "remove ok"
        else:
            result = "CAN NOT REMOVE main.py"
    except OSError:
        pass  # 文件不存在

    return {
        "ack": "OK",
        "result": result,
        "time": utime.time(),
    }
