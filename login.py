# 直接用 GET 方法的登入 SUDA
import requests
import toml
import socket
import base64

VENDOR_DIC = {
    '中国电信' : r'%40ctc',
    '校园网' : '',
    '中国移动' : r'%40zgyd',
    '中国联通' : r'%40cucc'
    }

def getIP():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    return None

def connect(ip : str, data : dict) -> str:
    print(f"IP : {ip}")
    vendor = VENDOR_DIC.get(data.get('vendor','114514'),'114514')
    if vendor == '114514':
        print('运营商不正确')
        quit(1)
    gateway = data.get('gateway','114514')
    if gateway == '114514':
        print('网关未找到')
        quit(1)
    account = data.get('account','114514')
    if account == '114514':
        print('账号未找到')
        quit(1)
    pswd = data.get('pswd','114514')
    if pswd == '114514':
        print('密码未找到')
        quit(1)

    print('连接中....')
    response = requests.get(f'http://{gateway}/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2Cb%2C{account}{vendor}&user_password={pswd}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=10253')
    return response.text

def proc(response : str):
    resp_dic = eval(response[7:-1]) # 删去 dr1003()
    msg : str = resp_dic['msg']
    # print(msg)
    if '\\' in msg or '成功' in msg:
        print(eval(r"'" + msg + r"'"))
    elif msg:
        print(base64.b64decode(msg.encode('ascii')).decode())
    else:
        print('已经登录')

if __name__ == '__main__':
    data = toml.load('data.toml')
    proc(connect(getIP(),data))
    