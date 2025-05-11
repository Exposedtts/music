# -*- coding: utf-8 -*-

import pandas as pd
from  sqlalchemy import  create_engine

con = create_engine('mysql+pymysql://root:5632@localhost:3306/music')
da = pd.read_sql('select * from 歌单',con=con)
db = pd.read_sql('select * from 网易云歌曲数据',con=con)
dc = pd.read_sql('select * from 英文专辑',con=con)
dd = pd.read_sql('select * from 用户评论',con=con)
#获取一列的全部数据
def typeList(sk,type):
    type = sk[type].values
    type = list(map(lambda x: x.split(','), type))
    typeList = []
    for i in type:
        for j in i:
            typeList.append(j)

    return typeList
# print(typeList(df,'书名'))