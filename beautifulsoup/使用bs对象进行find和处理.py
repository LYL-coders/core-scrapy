import requests
from bs4 import BeautifulSoup
import re

headers = {'user-agent':
             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/79.0.3945.79 Safari/537.36'}

url = "https://new.qq.com/omn/20210305/20210305A09CF900.html"

# res_news =requests.request(url=url,headers=headers)
# res_news =requests.Request(url=url,headers=headers)
res_news = requests.get(url=url,headers=headers)
html_news = res_news.text

bs = BeautifulSoup(html_news,'html.parser')
print(bs.prettify())
title = bs.find('h1').text
content= bs.find('div',class_='content-article').text #注意参数带下划线
content_str = "".join(re.findall('[0-9\u4e00-\u9fa5]', content))

for i in range(n):
    print("Now we are crawling the {0}th page".format(i+1))
    res_news = requests.get(url,params=params,headers=headers)
    res_news.
    params['pn'] += 10
# ————————————————
# 版权声明：本文为CSDN博主「Ares_Drw」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/Ares_WangZiquan/article/details/114405146
