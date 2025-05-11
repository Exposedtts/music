import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

try:
    # 读取数据文件
    df = pd.read_csv('音乐数据.csv')
except FileNotFoundError:
    print("未找到数据文件，请检查文件名和路径是否正确。")
else:
    # 数据清洗

    # 处理缺失值：删除发行日期缺失的记录
    df = df.dropna(subset=['发行日期'])

    # 处理重复值：通过歌名和歌手识别并删除重复记录
    df = df.drop_duplicates(subset=['歌名', '歌手'])

    # 处理错误数据：删除歌曲时长为负数的记录
    df = df[df['歌曲时长'] >= 0]

    # 数据预处理

    # 数据类型转换：将播放量从字符串转换为整数类型
    df['播放量'] = pd.to_numeric(df['播放量'], errors='coerce')
    df = df.dropna(subset=['播放量'])
    df['播放量'] = df['播放量'].astype(int)

    # 数据归一化：使用最小 - 最大归一化处理播放量和收藏量
    scaler = MinMaxScaler()
    df[['播放量', '收藏量']] = scaler.fit_transform(df[['播放量', '收藏量']])

    # 或者使用 Z - score 归一化
    # scaler = StandardScaler()
    # df[['播放量', '收藏量']] = scaler.fit_transform(df[['播放量', '收藏量']])

    # 将清洗和预处理后的数据保存为新文件
    df.to_csv('清洗预处理后的音乐数据.csv', index=False)
    print("数据清洗和预处理完成，处理后的数据已保存为 清洗预处理后的音乐数据.csv")
