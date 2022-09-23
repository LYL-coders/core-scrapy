import sqlite3
import threading
import time



from selenium import webdriver
import urllib.request

class MySpider_DOU:
    def __init__(self,URL,SEARCH_KEY):
        self.browser = webdriver.Chrome()
        self.browser.get(URL+SEARCH_KEY)
        self.page_num = 0
        self.image_url = []
        self.title_text = []
        self.meta_abstract = []

        self.startUp()

    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}
    def startUp(self):
        time.sleep(2)


        element =self.browser.find_elements_by_class_name('cover')
        element2 = self.browser.find_elements_by_class_name('title-text')
        element3 = self.browser.find_elements_by_class_name('meta.abstract')
        for i in element:
            try:
                self.image_url.append(i.get_attribute('src'))
            except:
                print('nan1')
                self.image_url.append("nan")

        for i in element2:
            try:
                print(i.get_attribute('textContent'))
                self.title_text.append(i.get_attribute('textContent'))
            except:
                print('nan2')
                self.title_text.append("nan")
        for i in element3:
            try:
                print(i.get_attribute('textContent'))
                self.meta_abstract.append(i.get_attribute('textContent'))
            except:
                print('nan3')
                self.meta_abstract.append("nan")
        try:

            nextPage = self.browser.find_element_by_class_name('next')  #没有s  才能提取web中的a标签 进行click操作

            nextPage.click()
            time.sleep(1)
            self.page_num += 1
            if self.page_num>=5:  #爬前5页
                self.browser.close()
                self.do_data()
                return 0
            self.startUp()

        except Exception as e:
            print(e)
            # self.browser.close()
            pass

    def do_data(self):
        print('self.image_url:::',len(self.image_url))
        print('self.title_text',len(self.title_text))
        print('self.meta_abstract',len(self.meta_abstract))
        a = Data_Load(self.image_url,self.title_text,self.meta_abstract)
        for t in threads_list:
            t.join()
        a.to_sql()
        print("数据库保存成功！！")


class Data_Load():
    def __init__(self,image_url,title_text,meta_abstract):
        self.image_url = image_url
        self.title_text = title_text
        self.meta_abstract = meta_abstract
        self.threads = []
        self.BOOK_IMAGE = []

        self.t_info()

    def to_sql(self):
        # Initializing database

        try:
            self.con = sqlite3.connect("douban.db")
            self.cursor = self.con.cursor()
            try:
                #  如果有表就删除
                self.cursor.execute("drop table douban.db")
            except:
                pass
            try:
                #  建立新的表
                sql = "create   table   douban   (id varchar(256)   primary   key,title_text  varchar(256),photo  longblob,meta_abstract  varchar(1024))"
                self.cursor.execute(sql)
            except:
                pass
        except Exception as err:

            print(err)
        # =============================================================数据库保存
        print('self.BOOK_IMAGE',len(self.BOOK_IMAGE))
        for id in range(len(self.image_url)):
            self.insertDB(id, self.title_text[id+1], self.BOOK_IMAGE[id], self.meta_abstract[id+2])
        self.closeUp()

    def closeUp(self):
        try:
            self.con.commit()
            self.con.close()
            # self.driver.close()
        except Exception as err:
            print(err)

    def insertDB(self, id, title_text, photo, meta_abstract):

        try:
            sql = "insert into douban (id,title_text,photo,meta_abstract) values (?,?,?,?)"
            self.cursor.execute(sql, (id, title_text, photo, meta_abstract))
        except Exception as err:
            print(err)



    def t_info(self):


        for src1 in self.image_url:

            p = src1.rfind("/")
            mFile = src1[p+1:]
            if src1:
                T = threading.Thread(target=self.download, args=(src1, mFile))
                T.setDaemon(False)
                T.start()
                self.threads.append(T)
                print(T)
                global threads_list
                threads_list = self.threads


    def download(self, src1, mFile):
        data = None
        if src1:
            try:
                req = urllib.request.Request(src1, headers=MySpider_DOU.headers)
                resp = urllib.request.urlopen(req, timeout=10)
                data = resp.read()
                self.BOOK_IMAGE.append(data)
            except:
                data=''
                pass

        try:
            if data:

                fobj = open(PATH_INFO + "\\" + mFile, "wb")
                fobj.write(data)
                fobj.close()
                print("已下载：   ", mFile)
        except Exception as E:
            print(E)
def initialize_data_form_input():
    PATH_INFO = 'download_IMG'
    URL_INFO = 'https://search.douban.com/book/subject_search?search_text='
    SEARCH_KEY = 'PYTHON'
    return PATH_INFO,URL_INFO,SEARCH_KEY

if __name__ == '__main__':
    PATH_INFO, URL_INFO, SEARCH_KEY = initialize_data_form_input()
    a = MySpider_DOU(URL_INFO,SEARCH_KEY)

