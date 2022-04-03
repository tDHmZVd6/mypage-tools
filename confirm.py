import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Target URL
login_url    = "https://mypage-web.*************.com/MyPage/login_check.asp"
logout_url   = "https://mypage-web.*************.com/MyPage/logout.asp"
confirm_url  = "https://mypage-web.*************.com/MyPage/confirm/confirm.asp"
workinfo_url = "https://mypage-web.*************.com/MyPage/confirm/workshop_info.asp"
menu_url     = "https://mypage-web.*************.com/MyPage/menu.asp"
reserve_url  = "https://mypage-web.*************.com/MyPage/reserve/reserve.asp"
change_url   = "https://mypage-web.*************.com/MyPage/reserve/change_reserve.asp"
ret_change_url = "https://mypage-web.*************.com/MyPage/reserve/ret_change_reserve.asp"

# Read Login Info
f = open('./login_info', 'r')
USER = f.readline().replace('\n', '')
PASS = f.readline().replace('\n', '')
f.close()

# Login Parameter
login_param = {
    'UID': USER,
    'PW' : PASS
}

# Logout Parameter
logout_param = {
    'SID': USER
}

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

'''
# Basic Parameter
basic_param = {
    'SID'        : '=?ISO-2022-JP?B?NDA3ODA=?=',
    'CONF_MODE'  : '=?ISO-2022-JP?B?Mg==?=',
    'MENU_MODE'  : '=?ISO-2022-JP?B?MQ==?=',
    'LOGIN_INFO' : login_info
}
#print(basic_param)
'''

# Set Menu URL
url = confirm_url + '?SID=' + sid + '&CONF_MODE==?ISO-2022-JP?B?Mg==?=&MENU_MODE==?ISO-2022-JP?B?MA==?=&LOGIN_INFO=' + login_info
res = session.get(url)
#print(url)
#print('status:'+str(res.status_code))
#print(res.text)

# Get Parameters(from web page source)
index = res.text.find('PRO_ID')
pro_id = res.text[index + 14 : index + 40]
index = res.text.find('DATE')
date = res.text[index + 12 : index + 22]
index = res.text.find('ST_DATE" ')
st_date = res.text[index + 16 : index + 58]
index = res.text.find('MENU_MODE" ')
menu_mode = res.text[index + 18 : index + 40]
index = res.text.find('BID')
bid = res.text[index + 11 : index + 12]
index = res.text.find('BASE_ID')
base_id = res.text[index + 16 : index + 38]

print(date)

# Encode Date
#st_date_encoded = base64.b64encode(st_date.encode()).decode()

# Workinfo Parameter
workinfo_param = {
    'CONF_BTN'   : '\x8A\x6D\x94\x46',
    'SID'        : sid,
    'PRO_ID'     : pro_id,
    'DATE'       : date,
    'ST_DATE'    : st_date,
    'MENU_MODE'  : menu_mode,
    'BID'        : bid,
    'LOGIN_INFO' : login_info,
    'BASE_ID'    : base_id
}
#print(workinfo_param)

# Work Infomation Page
#res = session.get(confirm_url, data=basic_param)
#print('workinfo_status:'+str(res.status_code))
#print(res.text)

# Confirm Action
res = session.post(workinfo_url, data=workinfo_param)
print('confirm_status:'+str(res.status_code))
#print(res.text)

# Logout
res = session.post(logout_url, data=logout_param)
#print('logout_status:'+str(res.status_code))
#print(res.text)

# Wait
#print('Press Any Key')
#input()
