from datetime import datetime, date, timedelta
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# List of day off
disable_days = [
#    '2021/12/30 0:00:00',
#    '2022/01/01 0:00:00',
#    '2022/01/02 0:00:00',
#    '2022/01/03 0:00:00',
]
print(disable_days)

# Target URL
login_url   = "https://mypage-web.*************.com/MyPage/login_check.asp"
logout_url  = "https://mypage-web.*************.com/MyPage/logout.asp"
menu_url    = "https://mypage-web.*************.com/MyPage/menu.asp"
reserve_url = "https://mypage-web.*************.com/MyPage/reserve/reserve.asp"
change_url  = "https://mypage-web.*************.com/MyPage/reserve/change_reserve.asp"
ret_change_url  = "https://mypage-web.*************.com/MyPage/reserve/ret_change_reserve.asp"

# Read Login Info
f = open('./login_info', 'r')
USER = f.readline().replace('\n', '')
PASS = f.readline().replace('\n', '')
f.close()

# Login Data
login_param = {
    'UID': USER,
    'PW' : PASS
}

# Logout Data
logout_param = {
    'SID': USER
}

# Get Today
today = datetime.today()
TOP_DATE = today.strftime('%Y/%m/%d')
print(TOP_DATE)

# Start Session
session = requests.session()
response = session.get(login_url, verify=False)

# Login Action
res = session.post(login_url, data=login_param)

# Get Session Prameter
sid_index = res.text.find('SID=')
sid = res.text[sid_index + 4 : sid_index + 30]

login_index = res.text.find('LOGIN_INFO=')
login_info = res.text[login_index + 11 : login_index + 61]

## Comment out ## 
'''
## Reserve Data
reserve_param = {
    'SID'        : sid,
    'TOP_DATE'   : TOP_DATE,
    'DATE_FLG'   : 'True',
    'BTN'        : '1',
    'LOGIN_INFO' : login_info
}

## Change Data
change_param = {
    'CHK_RSV'    : all_days,
    'BTN'        : '1',
    'SID'        : sid,
    'TOP_DATE'   : TOP_DATE,
    'DATE_FLG'   : 'True',
    'LOGIN_INFO' : login_info
}

## Ret Change Data
ret_param = {
    'ERDO'                 : 'ENABLE_DAY', 
    'DISABLE_HOUR_START'   : '00',
    'DISABLE_MINUTE_START' : '00',
    'DISABLE_HOUR_END'     : '00',
    'DISABLE_MINUTE_END'   : '00',
    'ENABLE_HOUR_START'    : '00',
    'ENABLE_MINUTE_START'  : '00',
    'ENABLE_HOUR_END'      : '00',
    'ENABLE_MINUTE_END'    : '00',
    'SID'                  : sid,
    'TOP_DATE'             : TOP_DATE,
    'LOGIN_INFO'           : login_info
}

## Reserve Action
res = session.post(reserve_url, data=change_param)
print('reserve_status:'+str(res.status_code))
print(res.text)

## Change Select Action
res = session.post(change_url, data=change_param)
print('select_status:'+str(res.status_code))
print(res.text)

# Change Commit Action
res = session.post(ret_change_url, data=ret_param)
print('change_status:'+str(res.status_code))
print(res.text)
'''
## Comment End ##

# Change Data
change_param = {
    'CHK_RSV'    : disable_days,
    'BTN'        : '1',
    'SID'        : sid,
    'TOP_DATE'   : TOP_DATE,
    'DATE_FLG'   : 'True',
    'LOGIN_INFO' : login_info
}

# Ret Change Data
ret_param = {
    'ERDO'                 : 'DISABLE_DAY', 
    'DISABLE_HOUR_START'   : '00',
    'DISABLE_MINUTE_START' : '00',
    'DISABLE_HOUR_END'     : '00',
    'DISABLE_MINUTE_END'   : '00',
    'ENABLE_HOUR_START'    : '00',
    'ENABLE_MINUTE_START'  : '00',
    'ENABLE_HOUR_END'      : '00',
    'ENABLE_MINUTE_END'    : '00',
    'SID'                  : sid,
    'TOP_DATE'             : TOP_DATE,
    'LOGIN_INFO'           : login_info
}

# Reserve Action
res = session.post(reserve_url, data=change_param)
print('reserve_status:'+str(res.status_code))
#print(res.text)

# Change Select Action
res = session.post(change_url, data=change_param)
print('select_status:'+str(res.status_code))
#print(res.text)

# Change Commit Action
res = session.post(ret_change_url, data=ret_param)
print('change_status:'+str(res.status_code))
#print(res.text)

# Logout
res = session.post(logout_url, data=logout_param)

# Output Logout Result
print('logout_status:'+str(res.status_code))
#print(res.text)

