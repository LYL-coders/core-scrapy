from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import threading
import sqlite3
import os
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# from selenium.webdriver.support.wait import WebDriverWait


class MySpider:
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
    # headers = {"User-Agent": "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666"}
    imagePath = "download"

    def startUp(self,url,key):
        # Initializing Chrome browser
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # Initializing variables
        self.threads = []
        self.No = 0
        self.imgNo=0


        # Initializing database
        try:
            self.con = sqlite3.connect("phones.db")
            self.cursor = self.con.cursor()
            try:
                #  如果有表就删除
                self.cursor.execute("drop table phones")
            except:
                pass
            try:
                #  建立新的表
                sql   =   "create   table   phones   (mNo  varchar(32)   primary   key,mMark varchar(256),mPrice varchar(32),mNote varchar(1024),mFile varchar(256))"
                self.cursor.execute(sql)
            except:
                pass
        except Exception as err:
            print(err)

        # Initializing images folder
        try:
            if not os.path.exists(MySpider.imagePath):
                os.mkdir(MySpider.imagePath)
            images = os.listdir(MySpider.imagePath)
            for img in images:
                s = os.path.join(MySpider.imagePath, img)
                os.remove(s)
        except Exception as err:
            print(err)

        # self.driver.get(url)
        # keyInput=self.driver.find_element_by_id("key")
        # keyInput.send_keys(key)
        # keyInput.send_keys(Keys.ENTER)
    #
    # def closeUp(self):
    #     try:
    #         self.con.commit()
    #         self.con.close()
    #         self.driver.close()
    #     except Exception as err:
    #         print(err);
    #
    # def insertDB(self, mNo, mMark, mPrice, mNote, mFile):
    #
    #     try:
    #         sql = "insert into phones (mNo,mMark,mPrice,mNote,mFile) values (?,?,?,?,?)"
    #         self.cursor.execute(sql, (mNo, mMark, mPrice, mNote, mFile))
    #     except Exception as err:
    #         print(err)
    #
    # def showDB(self):
    #     try:
    #         con=sqlite3.connect("phones.db")
    #         cursor=con.cursor()
    #         print("%-8s %-16s %-8s %-16s %s" % ("No", "Mark", "Price", "Image", "Note"))
    #         cursor.execute("select  mNo,mMark,mPrice,mFile,mNote from  phones  orderby mNo")
    #         rows = cursor.fetchall()
    #         for row in rows:
    #             print("%-8s  %-16s %-8s  %-16s %s"  %  (row[0],  row[1],  row[2],  row[3],row[4]))
    #         con.close()
    #     except Exception as err:
    #         print(err)

    def download(self, src1,src2,mFile):
        data=None
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
            fobj = open(MySpider.imagePath + "\\" + mFile, "wb")
            fobj.write(data)
            fobj.close()
            print("download ",mFile)

    def processSpider(self):
        try:
            self.driver.get(url)
            time.sleep(1)
            print(self.driver.current_url)

            lis = self.driver.find_elements_by_xpath("//html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]")
            # lis = self.driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div[1]/div[3]/div[1]/div/div/div/div[1]/div[2]")
            print('lis',lis[0].text)
            for li in lis:
                print(li.text)
                # src1 = li.find_element_by_xpath(".//div/div[1]/div/a/div/img").get_attribute("outerHTML")
                # src1 = li.find_element_by_xpath(".//div/div[1]/div/a/div/img").get_attribute("src")
                # print(src1)
            #
            #     try:
            #         print(WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]/a/div[1]/img"))).get_attribute("src"))
            #         src1 = li.find_element_by_xpath("./a/div[1]/img").get_attribute("outerHTML")

                #         for i in src1:
                #             print('src1', src1)
                #             src1 = urllib.request.get(src1)
                #             print('src1_request:', src1)
                #             p = src1.rfind(".")
                #             mFile = src1[p:]
                #             print(type(mFile))
                # except:
                #         src1 = ""
                # We find that the image is either in src or in data-lazy-img attribute
                try:
                    src1 = li.find_element_by_xpath(".//div/div[1]/div/a/div/img").get_attribute("src")
                    print(src1)
                except:
                    src1 = ""
                try:
                    src2 = li.find_element_by_xpath(".//div/div[1]/div/a/div/img").get_attribute("data-lazy-img")
                except:
                    src2 = ""
        #         try:
        #             price = li.find_element_by_xpath(".//div[@class='p-price']//i").text
        #         except:
        #             price = "0"
        #         print(src1)
                # print(src2)
        #
        #         self.No = self.No + 1
        #         no = str(self.No)


                if src1:
                    print('src1',src1)
                    src1 = urllib.request.urljoin(self.driver.current_url, src1)
                    print('src1_request:',src1)
                    p = src1.rfind(".")
                    mFile =src1[p:]
                    print(type(mFile))
                elif src2:
                    print('src2', src2)
                    src2 = urllib.request.urljoin(self.driver.current_url, src2)
                    p = src2.rfind(".")
                print(p)
                    # mFile = no + src2[p:]
                # if src1 or src2:
                #     T = threading.Thread(target=self.download, args=(src1, src2, mFile))
                #     T.setDaemon(False)
                #     T.start()
                #     self.threads.append(T)
                # else:
                #     mFile = ""
        #         self.insertDB(1, 1, 1, 1, mFile)

        #     try:
        #         self.driver.find_element_by_xpath("//span[@class='p-num']//a[@class='pn-next disabled']")
        #     except:
        #         nextPage = self.driver.find_element_by_xpath("//span[@class='p-num']//a[@class='pn-next']")
        #         nextPage.click()
        #         self.processSpider()
        except Exception as err:
            print(err)

    def executeSpider(self, url,key):
        starttime = datetime.datetime.now()
        print("Spider starting......")
        self.startUp(url,key)
        self.processSpider()
        # self.closeUp()
        for t in self.threads:
            t.join()
        print("Spider completed......")
        endtime = datetime.datetime.now()
        elapsed = (endtime - starttime).seconds
        print("Total ", elapsed, " seconds elapsed")

        self.driver.close()
url = "https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&search=python"
spider = MySpider()
while True:
    print("1.爬取")
    print("2.显示")
    print("3.退出")
    s=input("请选择(1,2,3):")
    if s=="1":
        spider.executeSpider(url,"平板电脑")
    # elif s=="2":
    #     # spider.showDB()
    # elif s=="3":
    #     break
