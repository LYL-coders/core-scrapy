import os
import re
import time
import json
import base64
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def load_url(url):
    # 创建chrome浏览器驱动
    driver = webdriver.Chrome()
    # 打开你的访问地址
    driver.get(url)
    # 获取页面初始高度
    js = "return action=document.body.scrollHeight"
    height = driver.execute_script(js)
    # 将滚动条调整至页面底部
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3)
    # 定义初始时间戳（秒）
    t1 = int(time.time())
    # 定义循环标识，用于终止while循环
    status = True
    # 重试次数
    num = 0
    while status:
        # 获取当前时间戳（秒）
        t2 = int(time.time())
        # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
        if t2 - t1 < 30:
            new_height = driver.execute_script(js)
            if new_height > height:
                time.sleep(1)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                # 重置初始页面高度
                height = new_height
                # 重置初始时间戳，重新计时
                t1 = int(time.time())
        elif num < 3:  # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
            time.sleep(3)
            num = num + 1
        else:  # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
            print("滚动条已经处于页面最下方！")
            status = False
            # 滚动条调整至页面顶部
            driver.execute_script('window.scrollTo(0, 0)')
            break
    content = driver.page_source.encode('utf-8')
    driver.close()
    return content


def analysis_html(content, save_path):
    # 定义爬虫header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre"}  # 需修改，按照你的电脑chrome版本而定
    # 解析爬取的网页
    content = BeautifulSoup(content, 'lxml')
    # 查找图片的父标签
    res = content.find_all("img", class_='main_img img-hover')
    # 查找到图片标签，而且保存图片
    for i in range(len(res)):
        src = res[i].attrs["src"]
        try:
            # 分为两种情况：第一、网页上显示图片的base64编解码格式；第二、网页上显示图片的url
            if src.startswith('data'):
                data = src.split(',')[1]
                image_data = base64.b64decode(data)
                print("正在下载：第%s张图片" % str(i))
                with open(os.path.join(save_path,
                                       '{}.jpg'.format(str(i).zfill(4))), 'wb') as f:
                    f.write(image_data)
            else:
                data = requests.get(src, timeout=60, headers=headers)
                print("正在下载：第%s张图片" % str(i))
                with open(os.path.join(save_path, '{}.jpg'.format(str(i).zfill(4))), 'wb') as f:
                    f.write(data.content)
        except Exception as e:
            print("第%s张图片格式错误" % str(i))
            print("错误原因为: %s" % e)
    print("下载完毕")


if __name__ == "__main__":
    url = "https://www.nowcoder.com/jobs/fulltime/center?recruitType=3&search=python"
    save_path = './'
    content = load_url(url)
    analysis_html(content, save_path)

