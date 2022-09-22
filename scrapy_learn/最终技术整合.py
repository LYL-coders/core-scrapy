


import urllib3

from selenium import webdriver



#
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("http://www.zhihu.com/explore")
# logo = browser.find_element_by_css_selector('PageBottomFooter')
# print(logo)
# print(logo.text)
#
#
# /html/body/div[1]/div/main/div[2]/div[4]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/span[1]/div/div/a/img
# //*[@id="collection"]

#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# input = browser.find_element_by_css_selector('.zu-top-add-question')
# print(input.id)
# print(input.location)
# print(input.tag_name)
# print(input.size)

# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get("http://www.zhihu.com/explore")
# element = browser.find_element_by_xpath('//*[@id="collection"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/span[1]/div/div/a/img')
# # print(element.get_attribute('outerHTML'))
# print(element.get_attribute('innerHTML'))
# print(element.get_attribute('textContent'))
# browser.close()
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import urllib.request
import datetime
import threading
import time

class save_to_database():
    def __init__(self,src_list):
        self.threads = []
        self.src_list = src_list
        self.load_image_pre()
    def load_image_pre(self):

        self.No = 0
        self.No = self.No + 1
        self.no = str(self.No)
        while len(self.no) < 6:
            self.no = "0" + self.no
        print(self.no)
        for src1 in self.src_list:
            # src1 = urllib.request(src1)
            # p = src1.rfind(".")
            p = src1.rfind("/")
            # mFile = self.no + src1[p:]   #编号+文件类型（png,jpg...)
            mFile = src1[p+1:]
            src2 = 0   #预留
            if src1 or src2:
                T = threading.Thread(target=self.download, args=(src1, src2, mFile))
                T.setDaemon(False)
                # setDaemon(True)因为没有了被守护者，守护线程也就没有工作可做了，也就没有继续运行程序的必要了。
                # 将线程转换为守护线程可以通过调用Thread对象的setDaemon(true)方法来实现。
                T.start()

                self.threads.append(T)  # 线程池
                global threads_list
                threads_list = self.threads


    def download(self, src1, src2, mFile):
        data = None
        if src1:
            try:
                req = urllib.request.Request(src1, headers=MySpider.headers)
                resp = urllib.request.urlopen(req, timeout=400)
                data = resp.read()
            except:
                pass
        if not data and src2:
            try:
                req = urllib.request.Request(src2, headers=MySpider.headers)
                resp = urllib.request.urlopen(req, timeout=400)
                data = resp.read()
            except:
                pass
        if data:
            # fobj = open(MySpider.imagePath + "\\" + mFile, "wb")
            fobj = open('downloads_img' + "\\" + mFile + ".jpg", "wb")
            fobj.write(data)
            fobj.close()
            print("download   ", mFile)


class MySpider:
    def __init__(self,url,key):
        self.url = url
        self.key = key  #搜索预备
        self.image_src_list = []
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)  # 加载网页url
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
    imagePath = "download"

    def startUp(self):
        # Initializing Chrome browser
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
# ========================================================================  爬虫核心代码

        time.sleep(3)  # 等待资源加载
        # 获取页面初始高度
        js = "return action=document.body.scrollHeight"
        height = self.browser.execute_script(js)
        # 将滚动条调整至页面底部  绕过懒加载！！！
        kk = 0.1
        for o in range(10):
            time.sleep(0.2)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight*%s*%o)' % (kk, o))
        # ==========================================================================================牛客的XPATH
        # time.sleep(3)
        # element = browser.find_element_by_xpath('//html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/a/div[1]')
        element = self.browser.find_elements_by_class_name("my-avatar")  # 个人头像
        # element = browser.find_elements_by_class_name('my-img')  #公司头像
        # =============================================================================================
        # html = browser.page_source
        # print(html)
        # print(element)
        # print(element.get_attribute('outerHTML'))    #获取当前标签的完整 html
        # print(element.get_attribute('innerHTML'))    #会获取标签之间的完整 html
        # print(element.get_attribute('textContent'))  # 会获取标签之间的文本内容


        for i in element:
            if i.get_attribute('outerHTML'):
                print(i.get_attribute('outerHTML'))
                # print(i.get_attribute('src'))  #图片绝对URL网络地址
                self.image_src_list.append(i.get_attribute('src'))
            else:
                print(i.get_attribute("data-lazy-img"))  # 不同网站，懒加载属性不同


        try:
            # browser.find_element_by_xpath("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[21]/div/button[1]")
            nextPage = self.browser.find_element_by_xpath("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[21]/div/button[2]")
            nextPage.click()
            self.startUp()
        except:
            self.browser.close()
            pass
        # browser.close()  #关闭，否则会堵塞堆积进程
        # 此时完成资源的爬取与载人步骤
    def executeSpider(self):
        starttime = datetime.datetime.now()
        print("Spider starting......")
        self.startUp()
        save_to_database(self.image_src_list)
        for t in threads_list:
            t.join()   # t.join()方法阻塞调用此方法的线程(calling thread)进入 TIMED_WAITING 状态，直到线程t完成，此线程再继续
                        # 如在main线程调用t.join(),则会阻塞main线程直到t线程执行完。
        print("Spider completed......")
        endtime = datetime.datetime.now()
        elapsed = (endtime - starttime).seconds
        print("Total ", elapsed, " seconds elapsed")



if __name__ == '__main__':
    # fobj = open('downloads', "w")
    #
    # fobj.close()
    url = "https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&search=python"
    key = '0'
    spider = MySpider(url,key)
    spider.executeSpider()


    # def test_execute3(self):
    #     js = 'var q=document.getElementById("kw");q.style.border="2px solid red"'
    #     self.driver.execute_script(js)  # 把百度搜索边框变为红色
    #     sleep(2)
    #
    #
    # def test_execute4(self):
    #     # 滚动条滚动
    #     self.driver.find_element_by_id('kw').send_keys('留白')
    #     self.driver.find_element_by_id('su').click()

    # document.getElementById("toolBarBox").innerText; 网页conselo

    # from selenium import webdriver
    #
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.get("https://www.cnblogs.com/yoyoketang/")
    #
    # # 第一种：如果想拿到javaScript执行的返回值，需要在js脚本前加上return
    # # js_blog = 'return document.getElementById("blog_nav_sitehome").innerText;'
    #
    # # 第二种：jquery也适用
    # js_blog = "return $('#blog_nav_sitehome')[0];"
    #
    # blog = driver.execute_script(js_blog)
    # print(blog)

# https://blog.csdn.net/qq_32189701/article/details/100176577  #find_element_by_xpath()使用的几种方法
# https://jishuin.proginn.com/p/763bfbd618c3  # 如何使用selenium获取网页里的图片
# 使用jquery选择器通过data-id属性获得到div标签，然后获取css样式里的background-image，selenium可以执行javascript代码，这样就获取到了图片的真实url。