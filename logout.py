# 用GET的方法登出网关
import requests
import toml
import socket

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

def unbind(ip : str, data : dict) -> str:
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

    print('解绑中....')
    response = requests.get(f'http://{gateway}/?c=Portal&a=unbind_mac&callback=dr1003&user_account={account}{vendor}&wlan_user_mac=000000000000&wlan_user_ip={ip}')
    return response.text

# 登出竟然不是用的自己的账号
def logout(ip : str, data : dict) -> str:
    print(f"IP : {ip}")
    gateway = data.get('gateway','114514')
    if gateway == '114514':
        print('网关未找到')
        quit(1)

    print('登出中....')
    response = requests.get(f'http://{gateway}/?c=Portal&a=logout&callback=dr1004&login_method=1&user_account=drcom&user_password=123&ac_logout=1&register_mode=1&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_vlan_id=1&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=')
    return response.text

def proc(response : str):
    resp_dic = eval(response[7:-1]) # 删去 dr1004()
    msg : str = resp_dic['msg']
    print(msg)

if __name__ == '__main__':
    data = toml.load('data.toml')
    proc(unbind(getIP(),data))
    proc(logout(getIP(),data))