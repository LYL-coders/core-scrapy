from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
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
# for i in s:
#     print(i)
/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]
/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]/a/div[1]/img
/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]/div[1]/a[2]/img
/html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]/div[1]/a[2]/img
lis = self.driver.find_elements_by_xpath("//html/body/section/main/div/div[3]/div[3]/div[1]/div/div[2]/div/div[2]")
/html/body/div[2]/div[3]/div[1]/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div/a/div/img
