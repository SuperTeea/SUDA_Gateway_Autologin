# 自动注销脚本 (注销完之后应该会卡一段时间，不太懂)
import selenium
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import selenium.webdriver

import time
import sys

gateway = r"http://10.9.1.3/" # 苏大默认网关

# print(sys.platform)
ret = 1
cnt = 0
max_retry = 5
while ret:
    driver = selenium.webdriver.Firefox() if sys.platform.startswith('linux') else selenium.webdriver.Edge()
    try:
        driver.get(gateway)
        
        # 如果还没登录 就退出 (通过看title判断)
        if driver.title != "注销页":
            print("还未登录!")
            quit(2)
        
        logout = driver.find_element(By.XPATH, r'//input[@class="edit_lobo_cell" and @name="logout"]')
        logout.click()
        time.sleep(1)   # 不 sleep 这一两秒好像就会导致无法正常登出
        confirm = driver.find_element(By.XPATH, r'//input[@class="boxy-btn1" and @value="确认"]')
        confirm.click()
        time.sleep(1)
        if driver.title == "注销页":
            cnt += 1
            if cnt >= max_retry:
                break
        else:
            ret = 0
    finally:
        driver.quit()
quit(ret)
