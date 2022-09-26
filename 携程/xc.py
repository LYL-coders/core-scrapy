from selenium import webdriver

import time

from selenium.webdriver.common.action_chains import ActionChains

# driver = webdriver.Chrome("C:/Users/Administrator/PycharmProjects/untitled/chromedriver.exe")
driver = webdriver.Chrome()
driver.implicitly_wait(30)

driver.get("https://www.ctrip.com/?sid=155952&allianceid=4897&ouid=index")

driver.maximize_window()

# 点击登录

driver.find_element_by_css_selector("#nav-bar-set-login > a > span").click()

# 登录账号

account =123

driver.find_element_by_id('nloginname').send_keys(account)

# 登录密码

password ="***"

driver.find_element_by_id('npwd').send_keys(password)

# 拖动滑块

slider = driver.find_element_by_css_selector("#sliderddnormal > div.cpt-drop-box > div.cpt-drop-btn")

# print(slider.size['width'])    方便理解，打印出来40px

# print(slider.size['height'])   打印出来40px

slider_area = driver.find_element_by_css_selector("#sliderddnormal > div.cpt-drop-box > div.cpt-bg-bar")

# print(slider_area.size['width'])  打印出来288px

# print(slider_area.size['height'])  打印出来40px

ActionChains(driver).drag_and_drop_by_offset(slider,slider_area.size['width'],slider.size['height']).perform()

time.sleep(3)

# 作者：蕊rui儿
# 链接：https://www.jianshu.com/p/954eeb0face9
# 来源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。