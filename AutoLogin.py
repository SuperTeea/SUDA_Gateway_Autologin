# 需要selenium库
import selenium
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import selenium.webdriver

import tomllib
import os
import time
import sys

# 没有使用toml的默认配置
usr = 'your username'
pwd = 'your password'
vendor = '校园网'
gateway = r"http://10.9.1.3/" # 苏大默认网关

if os.path.exists(os.path.join(os.path.dirname(__file__),"login.toml")):
    with open(os.path.join(os.path.dirname(__file__),"login.toml"), 'rb') as f:
        data = tomllib.load(f)
        usr = data['usr']
        pwd = data['pwd']
        vendor = data.get("vendor",vendor)
else:
    print(f"使用默认的用户和密码, 如需要请在 {os.path.dirname(__file__)} 下创建login.toml,格式见README.md")

# 一般Edge / Firefox 大家电脑都有，如果想用其他的自己更换
driver = selenium.webdriver.Firefox() if sys.platform.startswith('linux') else selenium.webdriver.Edge()
try:
    driver.get(gateway)
    
    # 如果已经登录 就退出 (通过看title判断)
    if driver.title != "上网登录页":
        print("已经登录!")
        quit(2)

    # 找到运营商选框，并按填写的运营商选择
    sel = Select(driver.find_element(By.NAME, r"ISP_select"))
    sel.select_by_visible_text(vendor)

    # 勾选漫游免认证 (不需要就注释掉)
    driver.find_element(By.NAME, r"checkPerceive").click()

    # 输入用户名和密码 (不得不吐槽这个name的命名...)  直接 Name找会找错，这里直接Xpath了
    usrInput = driver.find_element(By.XPATH, r'//input[@class="edit_lobo_cell" and @name="DDDDD"]')
    pwdInput = driver.find_element(By.XPATH, r'//input[@class="edit_lobo_cell" and @name="upass"]')
    usrInput.send_keys(usr)
    pwdInput.send_keys(pwd)
    
    time.sleep(3)

    # 确认登录
    driver.find_element(By.XPATH, r'//input[@class="edit_lobo_cell" and @name="0MKKey"]').click()

    time.sleep(3)

    print(driver.title)
    if driver.title != "注销页":
        print("登录失败!")
        quit(1)
    else:
        print("登录成功!")
        quit(0)
    
finally:
    driver.quit()