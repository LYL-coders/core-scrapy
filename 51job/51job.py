

"""
from selenium import webdriver
url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
      #https://search.51job.com/list/000000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
browser = webdriver.Chrome()
browser.get(url)
# element = browser.find_element_by_xpath('//*[@id="collection"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/span[1]/div/div/a/img')
element = browser.find_elements_by_class_name('jname.at')
element2 = browser.find_elements_by_class_name('sal')
# print(element.get_attribute('outerHTML'))
# print(element.get_attribute('innerHTML'))
for i in element:
    print(i.get_attribute('textContent'))
for i in element2:
    print(i.get_attribute('textContent'))
btn = browser.find_element_by_class_name('e_icons')
btn.click()
browser.close()
"""


"""

from selenium import webdriver
# 导入selenium中鼠标库
from selenium.webdriver import ActionChains
import time
driver = webdriver.Chrome()
driver.get("https://www.jq22.com/yanshi23642")
# 页面最大化
driver.maximize_window()
# 跳转到iframe中
driver.switch_to.frame('iframe')
# 在输入框中输入内容
driver.find_element_by_name('title').send_keys('123456')
# 通过CSS定位滑动点坐标
# slider = driver.find_element_by_css_selector('div.slider-btn.layui-icon.layui-icon-next')
slider = driver.find_element_by_xpath('//*[@id="sliderVerify16639506198763018582"]/div[3]')
# slider = driver.find_element_by_class_name('div.slider-btn.layui-icon.layui-icon-next')
# slider = driver.find_element_by_css_selector('slider-btn.layui-icon.layui-icon-ok-circle.slider-btn-success')
#slider-btn.layui-icon.layui-icon-ok-circle.slider-btn-success
print(slider)
time.sleep(3)
slider[0].click()

print(slider.location)
action = ActionChains(driver)
# 长按鼠标
action.drag_and_drop_by_offset(slider,268, 0)
# 偏移量（F12中查看）
print('偏移')
# action.move_by_offset(268, 0)
# 释放鼠标
# action.release()
# 执行以上操作
action.perform()
"""

"""
from selenium import webdriver
# 导入selenium中鼠标库
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
driver.get("https://www.jq22.com/yanshi23642")
# 页面最大化
driver.maximize_window()
# 跳转到iframe中
driver.switch_to.frame('iframe')
# 在输入框中输入内容
driver.find_element_by_name('title').send_keys('123456')
# 通过CSS定位滑动点坐标
slider = driver.find_element_by_css_selector('#sliderVerify16639514411974573265 > div.slider-btn.layui-icon.layui-icon-next')
time.sleep(5)
action = ActionChains(driver)
# 长按鼠标
action.click_and_hold(slider)
# 偏移量（F12中查看）
action.move_by_offset(268, 0)
# 释放鼠标
action.release()
# 执行以上操作
action.perform()
time.sleep(1)
# 元素属性
locator = (By.CLASS_NAME,'layui-layer-content')
# 通过显示等待进行定位元素
WebDriverWait(driver, 20,0.5).until(EC.presence_of_element_located(locator))
# 获取元素属性值
text = driver.find_element_by_class_name('layui-layer-content').text
print(text)
assert text == '滑块验证通过'
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver
url = 'https://www.jq22.com/yanshi23642'
browser = webdriver.Chrome()
browser.get(url)

browser.maximize_window()
# 跳转到iframe中
browser.switch_to.frame('iframe')
# 在输入框中输入内容
browser.find_element_by_name('title').send_keys('123456')
# 通过CSS定位滑动点坐标
# slider = browser.find_element_by_css_selector('#sliderVerify16639514411974573265>div.slider-btn.layui-icon.layui-icon-next')
slider = browser.find_element_by_class_name('slider-btn.layui-icon.layui-icon-next')
slider2 = browser.find_element_by_class_name('slider-bg.layui-bg-green')
# browser.execute_script("document.getElementByCss('#sliderVerify16639539363803137174 > div.slider-btn.layui-icon.layui-icon-next').style.left = '50px';")
# browser.execute_script("document.getElementByClassName('slider-btn.layui-icon.layui-icon-next').style.left = '50px';")
# slider.setAttribute('left', '100px')
browser.execute_script("arguments[0].setAttribute('style', 'left: 2680px;transition: left 2s;')", slider)
browser.execute_script("arguments[0].setAttribute('class', 'slider-btn.layui-icon.layui-icon-ok-circle.slider-btn-success')", slider)
browser.execute_script("arguments[0].setAttribute('style', 'width: 2680px;transition: width 2s;')", slider2)
# slider = browser.find_element_by_css_selector('#slider')
# slider = browser.find_element(By.CSS_SELECTOR, '#slider')
# time.sleep(5)
# action = ActionChains(browser)
# # 长按鼠标
# action.click_and_hold(slider)
# # 偏移量（F12中查看）
# action.move_by_offset(268, 0)
# # 释放鼠标
# action.release()
# # 执行以上操作
# action.perform()