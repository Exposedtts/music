# -*- coding:utf8 -*-
# python3.6
from urllib import request
import json
import pymysql
from datetime import datetime
import re

ROOT_URL = 'https://music.163.com/#/playlist?id=7050074027'
LIMIT_NUMS = 50  # 每页限制爬取数
DATABASE = ''  # 数据库名
TABLE = ''  # 数据库表名
# 数据表设计如下：
'''
id(int)             commentId(varchar) 
content(text)       likedCount(int) 
userId(varchar) time(datetime)
'''
PATTERN = re.compile(r'[\n\t\r\/]')  # 替换掉评论中的特殊字符以防插入数据库时报错


def getData(url):
    if not url:
        return None, None
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62',
        'Cookie': '_ntes_nnid=0e3ff42e3a972b16d05b643fc5c29aef,1666435082381; _ntes_nuid=0e3ff42e3a972b16d05b643fc5c29aef; __bid_n=1847927455736eee074207'
    }
    print('Crawling>>> ' + url)
    try:
        req = request.Request(url, headers=headers)
        content = request.urlopen(req).read().decode("utf-8")
        js = json.loads(content)
        total = int(js['total'])
        datas = []
        for c in js['comments']:
            data = dict()
            data['commentId'] = c['commentId']
            data['content'] = PATTERN.sub('', c['content'])
            data['time'] = datetime.fromtimestamp(c['time'] // 1000)
            data['likedCount'] = c['likedCount']
            data['userId'] = c['user']['userId']
            datas.append(data)
        return total, datas
    except Exception as e:
        print('Down err>>> ', e)
        pass


def saveData(data):
    if not data:
        return None
    conn = pymysql.connect(host='localhost', user='root', passwd='5632', db='music',
                           charset='utf8mb4')  # 注意字符集要设为utf8mb4，以支持存储评论中的emoji表情
    cursor = conn.cursor()
    sql = 'insert into ' + TABLE + ' (id,commentId,content,likedCount,time,userId) VALUES (%s,%s,%s,%s,%s,%s)'
    for d in data:
        try:
            cursor.execute('SELECT max(id) FROM ' + TABLE)
            id_ = cursor.fetchone()[0]
            cursor.execute(sql, (id_ + 1, d['commentId'], d['content'], d['likedCount'], d['time'], d['userId']))
            conn.commit()
        except Exception as e:
            print('mysql err>>> ', d['commentId'], e)
            pass

    cursor.close()
    conn.close()


if __name__ == '__main__':
    songId = input('歌曲ID：').strip()
    total, data = getData(ROOT_URL % (songId, LIMIT_NUMS, 0))
    saveData(data)
    if total:
        for i in range(1, total//EVERY_PAGE_NUMS + 1):
            _, data = getData(ROOT_URL % (songId, LIMIT_NUMS, i * (LIMIT_NUMS)))
            saveData(data)