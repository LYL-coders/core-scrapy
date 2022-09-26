from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# =======================================使用bs4进行html分析，通过正则拿到工资，该方案只作为个人测试学习，实际本项目用selenium去抓取工资
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome = webdriver.Chrome(chrome_options=chrome_options)
# chrome.get("https://www.lagou.com/wn/jobs?cl=false&fromSearch=true&kd=python")
# chrome.get('http://search.dangdang.com/?key=Python&act=input')
chrome.get('https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&search=python')
html=chrome.page_source
soup=BeautifulSoup(html,"lxml")
soupp=soup.prettify()
print(soup.prettify())
# hMsg=soup.find("span").text
# print('hMsg',hMsg)
# jMsg=soup.find("span",attrs={"id":"jMsg"}).text
# print(jMsg)
# sMsg=soup.find("span",attrs={"id":"sMsg"}).text
# print(sMsg)
import re
# s="I am testing search function"
s=soupp
# reg=r"[A-Za-z]+\b"
# reg ='span*/span'
# reg = '(?<=span)*?(?=/span)'
# m=re.search(reg,s)
# reg =
m=re.findall(r'<span>[\s\S]*?</span>', s)
n=[]
for i in m:
    # n.append(i.split('\n'))
    print(i.split('\n')[1].strip())
# m = re.findall(r'<span.........',s)
print(m)
print(n)
# while m!=None:
#  start=m.start()
#  end=m.end()
#  print(s[start:end])
#  s=s[end:]
#  m=re.search(reg,s)
