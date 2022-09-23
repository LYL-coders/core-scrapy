import sqlite3

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

class Save_To_Database():
    def __init__(self,save_path,src_list,title_list,job_detail_infos_list):
        self.save_path = save_path
        self.threads = []
        # =======================需要通过链接下载的src,url (图片url_list)
        self.src_list = src_list
        # ===========================经过下载后取得的图片数据
        self.user_image_list = []
        # ===========================直接获取到不需要下载的文本数据
        self.title_list = title_list
        self.job_detail_infos_list = job_detail_infos_list
        # ===========================
        # self.push_self()
        self.load_information_pre()

    # def push_self(self):  # ====================== # 不同类中self的传递
        # MySpider.get_self(self)
    def save_data_to_sqlite(self):
        # Initializing database
        try:
            self.con = sqlite3.connect("niuke_info.db")
            self.cursor = self.con.cursor()
            try:
                #  如果有表就删除
                self.cursor.execute("drop table niuke_info.db")
            except:
                pass
            try:
                #  建立新的表
                sql = "create   table   niuke_info_list   (id varchar(256)   primary   key,title_name  varchar(256),img  longblob,job_detail_infos  varchar(4096))"
                self.cursor.execute(sql)
            except:
                pass
        except Exception as err:
            print(err)
        # =============================================================数据库保存
        for id in range(len(self.src_list)):
            self.insertDB(id,self.title_list[id],self.user_image_list[id],self.job_detail_infos_list[id])
        self.closeUp()
    def closeUp(self):
        try:
            self.con.commit()
            self.con.close()
            # self.driver.close()
        except Exception as err:
            print(err)

    def insertDB(self,id,title_name, img,job_d_i):

        try:
            sql = "insert into niuke_info_list (id,title_name,img,job_detail_infos) values (?,?,?,?)"
            self.cursor.execute(sql,(id,title_name, img,job_d_i))
        except Exception as err:
            print(err)

    # def showDB(self):
    #     try:
    #         con = sqlite3.connect("test.db")
    #         cursor = con.cursor()
    #         print("%-8s %-16s %-8s %-16s %s" % ("No", "Mark", "Price", "Image", "Note"))
    #         cursor.execute("select  mNo,mMark,mPrice,mFile,mNote from  phones  orderby mNo")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print("%-8s  %-16s %-8s  %-16s %s" % (row[0], row[1], row[2], row[3], row[4]))
    #         con.close()
    #     except Exception as err:
    #         print(err)
    def load_information_pre(self):

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


    def download(self, src1, src2, mFile):  #需要进一步通过src,url加载的，运行下载函数线程，如图片，文本不需要下载
        data = None
        if src1:
            try:
                req = urllib.request.Request(src1, headers=MySpider.headers)
                resp = urllib.request.urlopen(req, timeout=3)
                data = resp.read()
                self.user_image_list.append(data)
            except:
                data='0'
                pass
        # if not data and src2:
        #     try:
        #         req = urllib.request.Request(src2, headers=MySpider.headers)
        #         resp = urllib.request.urlopen(req, timeout=400)
        #         data = resp.read()
        #     except:
        #         pass
        # ==========================================================本地保存图片
        try:
            if data:
                # fobj = open(MySpider.imagePath + "\\" + mFile, "wb")
                fobj = open(self.save_path + "\\" + mFile + ".jpg", "wb")
                fobj.write(data)
                fobj.close()
                print("download   ", mFile)
        except Exception as E:
            print(E)



class MySpider:
    def __init__(self,url,key,save_path):
        self.save_path = save_path
        self.url = url
        self.key = key  #搜索预备
        # =====================item部分
        self.image_src_list = []
        self.title_text_list = []
        self.job_detail_infos_list = []
        # ========================

        self.browser = webdriver.Chrome()
        self.browser.get(self.url)  # 加载网页url  更新了爬下一页的功能。所以放在这里
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
    # imagePath = "download"
    # def get_self(self,Save_To_Database_self):  # ====================== # 不同类中self的传递
    #     self.SELF = Save_To_Database_self
    # def data_self_return(self):
    #     return self.SELF
    def startUp(self):



        # Initializing Chrome browser
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(chrome_options=chrome_options)
# ========================================================================  爬虫核心代码

        time.sleep(3)  # 等待资源充分加载 非常重要的一步！！
        # 获取页面初始高度
        js = "return action=document.body.scrollHeight"
        height = self.browser.execute_script(js)
        # 将滚动条调整至页面底部  绕过懒加载！！！
        kk = 0.1
        for o in range(10):
            time.sleep(0.2)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight*%s*%o)' % (kk, o))
        self.browser.execute_script('window.scrollTo(0,0)')   #返回开始位置，开始加载详情页
        # ==========================================================================================牛客的XPATH
        # time.sleep(3)
        # element = browser.find_element_by_xpath('//html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/a/div[1]')
        # element = self.browser.find_elements_by_class_name("my-avatar")  # 个人头像
        element =self.browser.find_elements_by_class_name('my-img')  #公司头像
        try:
            # title = self.browser.find_element_by_xpath("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]/div[1]/span[1]").text

            title = self.browser.find_elements_by_class_name('job-name')  #一定注意fing_element没有s,就只有一个返回值，xpath同理
            print(title)
        except:

            title = "0"
            print('title,title',title)
        # =============================================================================================
        # html = browser.page_source
        # print(html)
        # print(element)
        # print(element.get_attribute('outerHTML'))    #获取当前标签的完整 html
        # print(element.get_attribute('innerHTML'))    #会获取标签之间的完整 html
        # print(element.get_attribute('textContent'))  # 会获取标签之间的文本内容
        # ==========================================================================文本本地化保存
        for i in title:

            # f = open(self.save_path + 'title.txt', 'a')
            # f.write(i.get_attribute('textContent') + '\n')
            self.title_text_list.append(i.get_attribute('textContent'))

        #将图片URL地址，形成序列，为下载做准备
        for i in element:
            if i.get_attribute('outerHTML'):
                print(i.get_attribute('outerHTML'))
                # print(i.get_attribute('src'))  #图片绝对URL网络地址
                self.image_src_list.append(i.get_attribute('src'))


            else:
                print(i.get_attribute("data-lazy-img"))  # 不同网站，懒加载属性不同





        # ==================================================================================读取详情页信息
        try:
            # nextPage = browser.find_element_by_xpath("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]")
            # nextPage.click()
            # time.sleep(3)
            # 获取当前窗口句柄（窗口A）
            handle = self.browser.current_window_handle

            # 打开一个新的窗口
            # btn0_list = browser.find_elements_by_xpath('/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]')
            btn0_list = self.browser.find_elements_by_class_name('job-message-boxs')

            time.sleep(3)
            print(len(btn0_list))
            for i in range(len(btn0_list)):
                # 获取当前所有窗口句柄（窗口A、B）
                if i % 10 == 0 and i < (len(btn0_list) - (len(btn0_list) % 10)):
                    btn0_list[i].click()  # 0,5,10,15  0  6   12 18
                    btn0_list[i + 1].click()
                    btn0_list[i + 2].click()
                    btn0_list[i + 3].click()
                    btn0_list[i + 4].click()
                    btn0_list[i + 5].click()
                    btn0_list[i + 6].click()
                    btn0_list[i + 7].click()
                    btn0_list[i + 8].click()
                    btn0_list[i + 9].click()

                    time.sleep(3)
                elif i >= (len(btn0_list) - (len(btn0_list) % 10)):
                    btn0_list[i].click()
                else:
                    pass
                # time.sleep(3)
                handles = self.browser.window_handles

                # 对窗口进行遍历
                for newhandle in handles:
                    # 筛选新打开的窗口B
                    if newhandle != handle:
                        # 切换到新打开的窗口B
                        self.browser.switch_to.window(newhandle)
                    else:
                        self.browser.switch_to.window(handles[1])
                        # 在新打开的窗口B中操作
                print('在新打开的窗口B中操作')
                # element = self.browser.find_element_by_class_name('ptb-2.pre-line')
                element = self.browser.find_element_by_class_name('job-detail-infos.tw-flex-auto')

                # element = browser.find_element_by_xpath('/html/body/section/main/div/div/div[2]/div[1]/div[2]/div/div[6]')

                print(element.text)
                # 关闭当前窗口B
                self.job_detail_infos_list.append(element.text)

                self.browser.close()

                # 切换回窗口A
                print('切换回窗口A')

                self.browser.switch_to.window(handles[0])

                # browser.close()
        except Exception as E:
            print(E)
            self.browser.close()

        # ========================================================================================================


        # ======================================================================================================#翻页逻辑
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
        database = Save_To_Database(self.save_path,self.image_src_list,self.title_text_list,self.job_detail_infos_list)
        for t in threads_list:
            print("%s线程阻塞中"%t)
            t.join() # t.join()方法阻塞调用此方法的线程(calling thread)进入 TIMED_WAITING 状态，直到线程t完成，此线程再继续
                        # 如在main线程调用t.join(),则会阻塞main线程直到t线程执行完。
        # ===================调用数据库sqlite    # 运用技术难点：不同类中self的传递
        try:

            database.save_data_to_sqlite()

        except:
            print('数据库保存失败。。。。。。')
        print("Spider completed......")
        endtime = datetime.datetime.now()
        elapsed = (endtime - starttime).seconds
        print("Total ", elapsed, " seconds elapsed")



if __name__ == '__main__':
    save_path = 'download'
    url = "https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&search=python"  #牛客
    # url = 'https://www.yohobuy.com/product/51085171.html'
    # url = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&suggest=1.his.0.0&wq=&pvid=e664938aaddc4f59ad60f02c2adc77af' #京东
    #自动输入搜索框，自动人机验证等等
    key = '0'
    spider = MySpider(url,key,save_path)
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