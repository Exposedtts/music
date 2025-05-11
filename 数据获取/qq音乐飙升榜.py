import  requests
from bs4 import BeautifulSoup
import time
import random
import sys
import re
from tqdm import tqdm
from lxml import etree

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3'
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0'
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'
    'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
    'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0'
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0'
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0'
    'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0'
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0'
    'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0'
    'Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0'
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1'
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1'
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0'
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0'
]

headers = {
    'User-Agent':random.choice(USER_AGENTS),
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }

# QQ音乐飙升榜
def QQ_muc_up():
    # 请求访问
    url = 'https://y.qq.com/n/ryqq/toplist/62'
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    # print(res)
    html = etree.HTML(res.text)
    # print(html)
    # 创建保存文件
    # 创建文件
    file = open("QQ_muc_up.csv", "a")
    file.write(
        "QQ_muc_pop" + "," + "QQ_muc_up" + "," + "QQ_muc_name" + "," + "QQ_muc_singer" + "," + "QQ_muc_time" + '\n')
    file = file.close()
    # 排名QQ_muc_pop、飙升指数QQ_muc_up、歌名QQ_muc_name、歌手QQ_muc_singer、歌曲时间QQ_muc_time
    pop = 1
    for i in range(1,21):
        QQ_muc_pop = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[1]/text()".format(pop))
        for item in QQ_muc_pop:
            QQ_muc_pop = item
        QQ_muc_up = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[2]/text()".format(pop))
        for item in QQ_muc_up:
            QQ_muc_up = item.strip('%')
            QQ_muc_up = int(QQ_muc_up)
        QQ_muc_name = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()".format(pop))
        for item in QQ_muc_name:
            QQ_muc_name = item
        QQ_muc_singer = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()".format(pop))
        for item in QQ_muc_singer:
            QQ_muc_singer = item
        QQ_muc_time = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[5]/text()".format(pop))
        for item in  QQ_muc_time:
            QQ_muc_time = item
        pop += 1
        # 保存数据
        with open('QQ_muc_up.csv', "a", encoding='utf-8') as file1:
            file1.writelines(QQ_muc_pop + "," + str(QQ_muc_up) + "," + QQ_muc_name + "," + QQ_muc_singer + "," + QQ_muc_time + '\n')
        print('歌名：',QQ_muc_name,'\n','排名：',QQ_muc_pop,'\n','飙升指数：',QQ_muc_up,'\n','歌手名：',QQ_muc_singer,'\n','时长',QQ_muc_time)

#QQ音乐流行榜
def QQ_muc_fasion():
    # 请求访问
    url = 'https://y.qq.com/n/ryqq/toplist/4'
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    # print(res)
    html = etree.HTML(res.text)
    # print(html)
    # 创建保存文件
    # 创建文件
    file = open("QQ_muc_fasion.csv", "a")
    file.write(
        "QQ_muc_pop" + "," + "QQ_muc_up" + "," + "QQ_muc_name" + "," + "QQ_muc_singer" + "," + "QQ_muc_time" + '\n')
    file = file.close()
    # 排名QQ_muc_pop、飙升指数QQ_muc_up、歌名QQ_muc_name、歌手QQ_muc_singer、歌曲时间QQ_muc_time
    pop = 1
    for i in range(1,21):
        QQ_muc_pop = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[1]/text()".format(pop))
        for item in QQ_muc_pop:
            QQ_muc_pop = item
        QQ_muc_up = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[2]/text()".format(pop))
        for item in QQ_muc_up:
            QQ_muc_up = item.strip('%')
            QQ_muc_up = int(QQ_muc_up)
        QQ_muc_name = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[3]/span/a[2]/text()".format(pop))
        for item in QQ_muc_name:
            QQ_muc_name = item
        QQ_muc_singer = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[4]/a/text()".format(pop))
        for item in QQ_muc_singer:
            QQ_muc_singer = item
        QQ_muc_time = html.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li[{}]/div/div[5]/text()".format(pop))
        for item in  QQ_muc_time:
            QQ_muc_time = item
        pop += 1
        # 保存数据
        with open('QQ_muc_fasion.csv', "a", encoding='utf-8') as file1:
            file1.writelines(
                QQ_muc_pop + "," + str(QQ_muc_up) + "," + QQ_muc_name + "," + QQ_muc_singer + "," + QQ_muc_time + '\n')
        print('歌名：',QQ_muc_name,'\n','排名：',QQ_muc_pop,'\n','飙升指数：',QQ_muc_up,'\n','歌手名：',QQ_muc_singer,'\n','时长',QQ_muc_time)

if __name__ == '__main__':
    print('-------------------start----------------------')
    print('正在爬取QQ音乐飙升榜单')
    QQ_muc_up()
    print('-------------------分界线----------------------')
    print('正在爬取QQ音乐流行榜单')
    QQ_muc_fasion()
    print('--------------------end------------------------')