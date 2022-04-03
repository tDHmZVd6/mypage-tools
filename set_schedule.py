import numpy
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import pandas
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Target URL
login_url   = "https://mypage-web.*************.com/MyPage/login_check.asp"
logout_url  = "https://mypage-web.*************.com/MyPage/logout.asp"
menu_url    = "https://mypage-web.*************.com/MyPage/menu.asp"
reserve_url = "https://mypage-web.*************.com/MyPage/reserve/reserve.asp"
change_url  = "https://mypage-web.*************.com/MyPage/reserve/change_reserve.asp"
ret_change_url  = "https://mypage-web.*************.com/MyPage/reserve/ret_change_reserve.asp"

# Read Login Info
f = open('./login_info', 'r')
user = f.readline().replace('\n', '')
pw = f.readline().replace('\n', '')
f.close()

# Login Data
login_param = {
    'UID': user,
    'PW' : pw
}

# Logout Data
logout_param = {
    'SID': user
}

# Get Date
today = datetime.datetime.today()
print(today)

# Set Today
top_date = today.strftime('%Y/%m/%d')
#print(top_date)

# Get First Day of Next Month
start_date = today + relativedelta(months=1, day=1)
print('start_date: ' + str(start_date))
#print(start_date.strftime('%Y/%m/%d 0:00:00'))

# Get End Date of Month
end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
print('end_date: ' + str(end_date))

# Set List of Days
date_index = pandas.date_range(start_date, end_date, freq='D')
all_days = date_index.to_series().dt.strftime('%Y/%m/%d 0:00:00').values
#print(all_days)

# Set Saturday Disable
date_index = pandas.date_range(start_date, end_date, freq='W-SAT')
sat_days = date_index.to_series().dt.strftime('%Y/%m/%d 0:00:00').values
#print(sat_days)

# Set Sunday Disable
date_index = pandas.date_range(start_date, end_date, freq='W-SUN')
sun_days = date_index.to_series().dt.strftime('%Y/%m/%d 0:00:00').values
#print(sun_days)

disable_days = numpy.concatenate([sun_days, sat_days])

print('disable_days:')
print(disable_days)

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


# ENABLE ACTION
# Reserve Data
reserve_param = {
    'SID'        : sid,
    'TOP_DATE'   : top_date,
    'DATE_FLG'   : 'True',
    'BTN'        : '1',
    'LOGIN_INFO' : login_info
}

# Change Data
change_param = {
    'CHK_RSV'    : all_days,
    'BTN'        : '1',
    'SID'        : sid,
    'TOP_DATE'   : top_date,
    'DATE_FLG'   : 'True',
    'LOGIN_INFO' : login_info
}

# Ret Change Data
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
    'TOP_DATE'             : top_date,
    'LOGIN_INFO'           : login_info
}

# Reserve Action
res = session.post(reserve_url, data=change_param)
#print('enable_reserve_status:'+str(res.status_code))

# Change Select Action
res = session.post(change_url, data=change_param)
#print('enable_select_status:'+str(res.status_code))

# Change Commit Action
res = session.post(ret_change_url, data=ret_param)
#print('enable_change_status:'+str(res.status_code))


# DISABLE ACTION
# Change Data
change_param = {
    'CHK_RSV'    : disable_days,
    'BTN'        : '1',
    'SID'        : sid,
    'TOP_DATE'   : top_date,
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
    'TOP_DATE'             : top_date,
    'LOGIN_INFO'           : login_info
}

# Reserve Action
res = session.post(reserve_url, data=change_param)
print('disable_reserve_status:'+str(res.status_code))
#print(res.text)

# Change Select Action
res = session.post(change_url, data=change_param)
print('disable_select_status:'+str(res.status_code))
#print(res.text)

# Change Commit Action
res = session.post(ret_change_url, data=ret_param)
print('disable_change_status:'+str(res.status_code))
#print(res.text)


# Logout
res = session.post(logout_url, data=logout_param)

# Output Logout Result
print('logout_status:'+str(res.status_code))
#print(res.text)

print('')
