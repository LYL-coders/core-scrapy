# 基本功能的实现介绍：

## （1） 爬取外网 

本次我尝试爬取了牛客网的职位信息。

> 该网站URL如下：
>
> https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&page=1&search=python

这里以python岗位为例子,其网页显示如下：

![image-20220925161225205](./readme.assets\image-20220925161225205-16640935613541.png)

## （2） 有对应的设计文档和源码，并能运行 



本工程文件结构如下：

![image-20220925161528718](.\readme.assets\image-20220925161528718.png)



运行效果如下：

![image-20220925232955150](.\readme.assets\image-20220925232955150.png)



## （3） 应当使用到数据库存储（sqlite3，mysql，...） 



本工程使用了sqlite3作为数据库，数据库显示效果如下:

![image-20220925190901236](.\readme.assets\image-20220925190901236.png)

数据库中的img列，保存的是二进制图片数据，从数据库中读取img和job_detail_infos结果如下：  （运行  数据库读写测试.py  生成）

![image-20220925162749193](.\readme.assets\image-20220925162749193.png)



公司头像如下：

![image-20220925162231068](.\readme.assets\image-20220925162231068.png)

HR头像保存如下：

![image-20220925162537092](.\readme.assets\image-20220925162537092.png)

## （4） 应当跨网页抓取（纵向读取链接）

详情页的显示内容如下：

> 本次工程将红框中的所有文本提取了出来。
>
> 就是数据库中job_detail_infos列中的内容。

![image-20220925163030219](.\readme.assets\image-20220925163030219.png)



# 环境介绍

本工程环境介绍：

主体为selenium框架：

- Window 系统 
- PyCharm 工程    
- Anaconda 虚拟环境

必要库：

- selenium  3.141.0
- beautifulsoup4  4.11.1
- urllib.request  1.26.12
- sqlite3  3.39.2





![image-20220925164525694](.\readme.assets\image-20220925164525694.png)

本工程文件结构内容介绍：

![image-20220925161528718](.\readme.assets\image-20220925161528718.png)



1.**最终技术整合_主运行程序.py**  是本工程的主程序，执行爬取，与数据库保存操作。

2.**数据库读写测试.py**  读取数据库数据生成对应文件，直观显示 ---将结果保存到read文件夹下。

3.**beautiful_selenium.py**  查看网页内容。

4.数据库名：**niuke_info.db**

5.**详情页跳转增加效率版.py**     详情页跳转设计批量化执行，该部分函数，已经整合到了主运行程序中。



# 需求分析

​		使用selenium框架，模拟chorme浏览器对牛客网进行访问，爬取相关职位信息，分析岗位情况。

主页面的信息，对于职位的描述并不充分，所以还需要点击跳转进入详情页，

对以下信息（岗位名称，公司照片，详情页职位描述信息，岗位工资，工作地区，要求学历，要求经验，相关标签）进行爬取。

![image-20220925191125503](.\readme.assets\image-20220925191125503.png)



![image-20220925171953745](.\readme.assets\image-20220925171953745.png)

有了数据以后就可以对其进行数据预处理，然后将重要数据筛选出来形成图表

![image-20220925203733022](.\readme.assets\image-20220925203733022.png)





# 技术选型和爬虫分析

分析完要爬什么数据后，剩下就是要解决怎么爬的问题了。

​		根据我多次的测试，有些网站存在javascript ,css 资源，它不能直接用beautifulsoup 爬取html,然后通过正则表达式提取出来，需要使用selenium才能提取对应的元素内容。其次，很多网站具有懒加载的机制，即资源异步加载，只加载窗口能看到部分的资源，其他部分的内容不会进行加载处理。因此就更有必要使用selenium作为爬虫框架，去模拟网页浏览过程。

以上就是我选用selenium作为爬虫框架的原因。

### 技术选型

| Window 系统             | 作用                              | 要点             |
| ----------------------- | --------------------------------- | ---------------- |
| PyCharm 工程编辑        | python编程语言                    |                  |
| Anaconda 虚拟环境       | 虚拟环境包管理                    |                  |
| selenium  3.141.0       | 模拟用户浏览过程                  | Chorme浏览器驱动 |
| beautifulsoup4  4.11.1  | 生成页面HTML结构                  |                  |
| urllib.request  1.26.12 | 发送 get  post 请求，下载对应资源 |                  |
| sqlite3  3.39.2         | 数据的保存                        | sqlite数据库     |

​		

### 爬虫设计与爬取分析逻辑

​		爬虫逻辑为：打开主页，等待3s，对窗口页进行滚动，到底部后再回到顶部，绕过懒加载，所有资源加载完毕，根据class_name抓取对应主页元素，然后读取页面含点击event的元素,形成点击列表，为了提升爬取速度，按照10个一组进行详情页打开操作，爬取详情页信息。当主页信息都读完后，调用下一页的按钮点击事件，进入下一页，然后迭代爬虫函数，再次执行直到最后一页。此间信息都保存在内存中，爬虫函数执行结束后，程序加载sqlite数据库函数，将内存中的信息保存到数据库niuke_info.db中,进行持久化保存。

流程图如下：

<img src=".\readme.assets\image-20220925230955929.png" alt="image-20220925230955929" style="zoom:80%;" />

### 爬虫基本架构selenium

```python
from selenium import webdriver
browser = webdriver.Chrome()
browser.get("http://www.zhihu.com/explore")
 element = browser.find_element_by_xpath('//*[@id="collection"]/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/span[1]/div/div/a/img')
# print(element.get_attribute('outerHTML'))
print(element.get_attribute('innerHTML'))
print(element.get_attribute('textContent'))
browser.close()
```



### 主页面的元素抓取操作

​		使用浏览器F12，分析器分析要爬取的元素的class name,最开始我是用Xpath进行元素选择，但是一层层的div并不直观，非常丑，所以选用了find_elements_by_class_name  、find_element_by_class_name  进行元素选择

比如在爬（工作地区，要求学历，要求经验，相关标签）这个部分的时候，直接复制html页面中的

class = flex-row-wrap tw-items-center tw-h-[21px] tw-leading-[21px] tw-overflow-hidden  是提取不到它的真实class name的，根据经验把其中的空格换成 '.'

class = flex-row-wrap.tw-items-center.tw-h-[21px] tw-leading-[21px].tw-overflow-hidden    尝试后还是无法提取到，这个时候我注意到它后面的tw属性，显然是css的相关属性，于是突发奇想把所有tw-的属性全部删掉，变成  class = flex-row-wrap   再次尝试，成功得到了对应的元素！再get 文本属性，此div中包含的所有文本就拿到手了。代码如下：

```python
base_message_list = browser.find_elements_by_class_name('flex-row-wrap')
for i in base_message_list:
      print(i.get_attribute('textContent'))
```

![image-20220925175126586](.\readme.assets\image-20220925175126586.png)

部分爬取结果如图：

![image-20220925232617937](.\readme.assets\image-20220925232617937.png)

其他元素的提取方法如下：

```python
# 公司头像集
element = self.browser.find_elements_by_class_name('my-img')
# ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
# 工作地区集
# work_space_list = self.browser.find_elements_by_class_name( 'job-info-item.tw-truncate.max-w-15.tw-flex-none')

# ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
# 多分支信息提取(工作地区,经验,学历,[tags])  北京 本科 3-5年 软件工程Python人工智能
base_message_list = self.browser.find_elements_by_class_name('flex-row-wrap')

# ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
try:
    # title = self.browser.find_element_by_xpath
    # ("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]/div[1]/span[1]").text
    # ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
    # 岗位名称集
    title = self.browser.find_elements_by_class_name('job-name')
    # 一定注意fing_element没有s,就只有一个返回值，xpath同理
    print(title)
    # ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
    # 薪水集
    salarys_list = self.browser.find_elements_by_class_name('job-salary.tw-flex-shrink-0')
    print('salarys_list=======', len(salarys_list))
    # ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
```

### 爬取详情页，元素抓取操作

当主页面的元素都提取完后，就要开始把详情页中的内容抓出来了,刚开始想法是 遍历job-message-boxs，其作为一个可被点击箱体（有event属性），对其一个个点击,进入详情页爬取数据后再关掉详情页，回到主页面。

![image-20220925234812059](.\readme.assets\image-20220925234812059.png)

```python
 # 岗位详细描述box
btn0_list = self.browser.find_elements_by_class_name('job-message-boxs')


```

![image-20220926000019830](.\readme.assets\image-20220926000019830.png)

#### 详情页的批量点击操作

显然一个个打开再关闭非常耗时，加上详情页的爬取后，竟然比只爬主页面多花了5倍的时间

所以有了详情页跳转增加效率版.py，打开不再是一个个打开，而是10个一组，进行打开爬取操作，如有不够的，就单次打开。

经过如下改进后原先760s才能结束，现在150s左右就能完成爬取和数据库保存工作。

核心代码：

```
# 获取当前窗口句柄（窗口A）
handle = self.browser.current_window_handle
# 切换到新打开的窗口B
self.browser.switch_to.window(newhandle)
```



```python
# 获取当前窗口句柄（窗口A）
    handle = self.browser.current_window_handle

    # 打开一个新的窗口
    # btn0_list = browser.find_elements_by_xpath
    # ('/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/a[1]')
    # ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
    # 岗位详细描述
    btn0_list = self.browser.find_elements_by_class_name('job-message-boxs')
    # ------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>
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

        # element = browser.find_element_by_xpath
        # ('/html/body/section/main/div/div/div[2]/div[1]/div[2]/div/div[6]')
        print(element.text)
        # 打印详情页内容
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
```



### 主页面跳转至下一页操作

只爬当前页，能得到的数据明显是不够的，这个时候就需要进行模拟翻页操作，之前一直是通过修改url  start /page  相关的参数，进行页面跳转的，但有些网站参数非常难以拿到或看到，根据之前的详情页点击event的经验,我也右键检查了下一页按钮btn 发现它也有点击event ，那接下来就简单了，拿到它对应的webelement  进行点击操作，直到点不了下一页后，就结束当前爬虫程序。

```python
# =======================================翻页逻辑=========================================================
try:
    # browser.find_element_by_xpath("/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[21]/div/button[1]")
    nextPage = self.browser.find_element_by_xpath(
        "/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[21]/div/button[2]")
    nextPage.click()
    # ============================控制爬取页数
    # self.page_num +=1
    # if self.page_num==2:
    #     self.browser.close()
    #     return 0
    # ==============================
    self.startUp()
except:
    self.browser.close()
    pass

# 此时完成资源的爬取与载人步骤
```

![image-20220926002028810](.\readme.assets\image-20220926002028810.png)



### 爬虫数据内存管理部分items设计

每个类型数据都先存为列表

```python
class MySpider:
    def __init__(self, url, key, save_path):
        self.save_path = save_path
        self.url = url
        self.key = key  # 搜索预备
        self.page_num = 0   # 页面爬取数量设定
        # =====================item部分
        self.image_src_list = []
        self.title_text_list = []
        self.salarys_text_list = []
        self.job_detail_infos_list = []
        self.base_message_list = []
        # ========================

        self.browser = webdriver.Chrome()
        self.browser.get(self.url + self.key)  # 加载网页url  更新了爬下一页的功能。所以放在这里

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre)"
                      " Gecko/2008072421 Minefield/3.0.2pre"}
```

将爬取的数据存入列表中，一一对应

```python
# ========================================================================== WebElement文本提取与显示
for i in title:
    # f = open(self.save_path + 'title.txt', 'a')
    # f.write(i.get_attribute('textContent') + '\n')
    self.title_text_list.append(i.get_attribute('textContent'))
    # print(type(i.get_attribute('textContent')))

for salary in salarys_list:
    if type(salary.get_attribute('textContent')) == str and salary.get_attribute('textContent') != '':
        self.salarys_text_list.append(salary.get_attribute('textContent'))
        print("salary:::", salary.get_attribute('textContent'))
    else:
        self.salarys_text_list.append('')

for i in base_message_list:
    if type(i.get_attribute('textContent')) == str and i.get_attribute('textContent') != '':
        self.base_message_list.append(i.get_attribute('textContent'))
        print("base_message_list:::", i.get_attribute('textContent'))
    else:
        self.base_message_list.append('')

# 将图片URL地址，形成序列，为下载做准备
for i in element:
    if i.get_attribute('outerHTML'):
        print(i.get_attribute('outerHTML'))
        # print(i.get_attribute('src'))  #图片绝对URL网络地址
        self.image_src_list.append(i.get_attribute('src'))
```

### 下载资源的线程管理设计

​		做这一步，本质上就是为了让下载好的资源可以按照原先的src输入顺序排好队列，如果不做线程阻塞这步，有的线程下的快，有的慢，就会导致和原先的src请求顺序不同，队伍顺序一乱，张三就会戴上李四的帽子，爬的数据就不可靠了。

```python
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
        mFile = src1[p + 1:]
        src2 = 0  # 预留
        if src1 or src2:
            T = threading.Thread(target=self.download, args=(src1, src2, mFile))
            T.setDaemon(False)
            # setDaemon(True)因为没有了被守护者，守护线程也就没有工作可做了，也就没有继续运行程序的必要了。
            # 将线程转换为守护线程可以通过调用Thread对象的setDaemon(true)方法来实现。
            T.start()

            self.threads.append(T)  # 线程池
            global threads_list
            threads_list = self.threads

def download(self, src1, src2, mFile):  # 需要进一步通过src,url加载的，运行下载函数线程，如图片，文本不需要下载
    data = None
    if src1:
        try:
            req = urllib.request.Request(src1, headers=MySpider.headers)
            resp = urllib.request.urlopen(req, timeout=3)
            data = resp.read()
            self.user_image_list.append(data)
        except:
            data = '0'
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
```

```python
# ============================线程开启==========================================

for t in threads_list:
    print("%s线程状态转换完成" % t)
    t.join()  # t.join()方法阻塞调用此方法的线程(calling thread)进入 TIMED_WAITING 状态，直到线程t完成，此线程再继续
    # 如在main线程调用t.join(),则会阻塞main线程直到t线程执行完。
print("下载完毕")
# time.sleep(3)
# ============================线程结束==========================================
```



### 数据库的使用

#### 将内存中的爬取数据保存到数据库

爬虫数据不多，刚好够且不需要联网故使用sqlite，增删改查速度都还很快。

```python
try:
    #  建立新的表
    sql = "create   table   niuke_info_list   (id varchar(256)   primary   key," \
          "title_name  " \
          "varchar(256)," \
          "img  longblob," \
          "job_detail_infos  varchar(4096)," \
          "salary  varchar(256)," \
          "base_message varchar(32))"
    self.cursor.execute(sql)
except:
    pass
```

提取内容到sqlite3 数据库中

![image-20220925234212389](.\readme.assets\image-20220925234212389.png)

![image-20220926004504928](.\readme.assets\image-20220926004504928.png)