import time
from selenium import webdriver
import urllib.request
import datetime
import threading
import time


url = "https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&search=python"
browser = webdriver.Chrome()
browser.get(url)  # 加载网页url  更新了爬下一页的功能。所以放在这里
time.sleep(3)  # 等待资源加载

try:
    # nextPage = browser.find_element_by_xpath("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]")
    # nextPage.click()
    # time.sleep(3)
    # 获取当前窗口句柄（窗口A）
    handle = browser.current_window_handle

    # 打开一个新的窗口
    # btn0_list = browser.find_elements_by_xpath('/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]')
    btn0_list = browser.find_elements_by_class_name('job-message-boxs')

    time.sleep(3)
    print(len(btn0_list))
    for btn0 in btn0_list:
        # 获取当前所有窗口句柄（窗口A、B）
        btn0.click()
        time.sleep(4)
        handles = browser.window_handles

        # 对窗口进行遍历
        for newhandle in handles:
            # 筛选新打开的窗口B
            if newhandle != handle:
                # 切换到新打开的窗口B
                browser.switch_to.window(newhandle)
            else:
                browser.switch_to.window(handles[1])
                # 在新打开的窗口B中操作
        print('在新打开的窗口B中操作')
        # element = browser.find_element_by_class_name('ptb-2.pre-line')
        element  = browser.find_element_by_class_name('job-detail-infos.tw-flex-auto')
        # element = browser.find_element_by_xpath('/html/body/section/main/div/div/div[2]/div[1]/div[2]/div/div[6]')

        print(element.text)
        # 关闭当前窗口B

        browser.close()

        # 切换回窗口A
        print('切换回窗口A')

        browser.switch_to.window(handles[0])

            # browser.close()
except Exception as E:
    print(E)
    browser.close()
time.sleep(1)
browser.close()
"""

1.关闭浏览器全部标签页

driver.quit()

2.关闭当前标签页（从标签页A打开新的标签页B，关闭标签页A）

driver.close()

3.关闭当前标签页（从标签页A打开新的标签页B，关闭标签页B）

可利用浏览器自带的快捷方式对打开的标签进行关闭

Firefox自身的快捷键分别为：

Ctrl+t 新建tab

Ctrl+w 关闭tab

 Ctrl+Tab /Ctrl+Page_Up      定位当前标签页的下一个标签页

 Ctrl+Shift+Tab/Ctrl+Page_Down   定位当前标签页的前一个标签页

 Ctrl+[数字键1-8] 定位所有标签页中最前的第[1-8]个

 Ctrl+数字键9      定位最后一个标签页

注：如果是在一些Linux发行版系统中,比如Ubuntu,需要将Ctrl键换成Alt键

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

#新建标签页

ActionChains(browser).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()

# 关闭标签页

ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()

4.标签页切换

from selenium import webdriver


browser=webdriver.Firefox()

browser.get('xxxxx')

# 获取当前窗口句柄（窗口A）

handle = browser.current_window_handle

# 打开一个新的窗口

browser.find_element_by_id('xx').click()

# 获取当前所有窗口句柄（窗口A、B）

handles = browser.window_handles

# 对窗口进行遍历

for newhandle in handles:

    # 筛选新打开的窗口B

    if newhandle!=handle:

# 切换到新打开的窗口B

browser.switch_to_window(newhandle)

# 在新打开的窗口B中操作

browser.find_element_by_id('xx').click()

# 关闭当前窗口B

browser.close()

#切换回窗口A

browser.switch_to_window(handles[0]) 

# ————————————————
# 版权声明：本文为CSDN博主「爱唱歌de小青蛙」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/xm_csdn/article/details/53395900

"""