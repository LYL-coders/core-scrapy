from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver#导入库
browser = webdriver.Chrome()#声明浏览器
url = 'https://www.139ys.com'
browser.get(url)#打开浏览器预设网址
print(browser.page_source)#打印网页源代码
elements = browser.find_elements(By.XPATH("/html/body/div[2]/div/div[1]/div/div[2]/ul/li"))
for i in elements:
    

browser.close()#关闭浏览器