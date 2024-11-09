
import SiOt_connection_tool
import time

ST = SiOt_connection_tool.SiOt_TCP("192.168.0.150", 40001)

def result_out(check_flag, ST = ST):
    ST.EtherFlag_change("00000000")
    
    if check_flag == 1:
        # 青フラグオン
        ST.EtherFlag_change("10000000")
        return "OK flag ON"

    elif check_flag == 2:
        # 赤フラグオン
        ST.EtherFlag_change("01000000")
        return "NG flag ON"
    
    else:
        return "flag input error"

def check_buttom_flag(ST = ST):
    response = ST.FLAG_state_check()
    
    if response[0] == "0":
        return 0
    elif response[0] == "1":
        return 1
    else:
        return "response error"