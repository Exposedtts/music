# 从当前目录下的 utils 模块导入所有内容
from .utils import *
# 导入 collections 模块中的 Counter 类，用于统计元素出现的次数
from collections import Counter
# 导入 jieba 库，用于中文分词
import jieba

# 歌单类型图
def gdlxt():
    # 将从数据中提取的不同标签列表合并
    leix = typeList(da, '标签1') + typeList(da, '标签2') + typeList(da, '标签3')
    # 初始化一个空字典，用于存储每种类型及其出现的次数
    typeObj = {}
    # 遍历合并后的类型列表
    for i in leix:
        # 如果该类型不在字典中
        if typeObj.get(i, -1) == -1:
            # 则将该类型添加到字典中，并将其出现次数初始化为 1
            typeObj[i] = 1
        else:
            # 否则，将该类型的出现次数加 1
            typeObj[i] = typeObj[i] + 1
    # 初始化一个空列表，用于存储符合 ECharts 数据格式的类型数据
    typeEcharDate = []
    # 遍历字典中的键值对
    for key, value in typeObj.items():
        # 将键值对转换为 ECharts 所需的字典格式，并添加到列表中
        typeEcharDate.append(
            {
                'value': value,
                'name': key
            }
        )
    # 返回 ECharts 数据列表
    return typeEcharDate


# gdlxt()

# 歌单播放量排行榜
def gdbflphb():
    # 从数据中提取播放次数列表
    bfl = typeList(da, '播放次数')
    # 将播放次数列表中的元素从字符串类型转换为整数类型
    bfl = [int(i) for i in bfl]
    # 从数据中提取歌单名称列表
    gedan = typeList(da, '名称')
    # 创建一个字典，将歌单名称作为键，播放次数作为值
    zzrqbshuj = {gedan[i]: bfl[i] for i in range(0, len(bfl) - 1)}
    # 使用 Counter 对字典进行统计，并按值从大到小排序
    c = Counter(zzrqbshuj).most_common()
    # 初始化两个空列表，分别用于存储前十的歌单名称和播放数量
    mzi = []
    bofcshu = []
    # 遍历排序后的结果，取前十个元素
    for i in range(0, 10):
        # 将歌单名称添加到列表中
        mzi.append(c[i + 2][0])
        # 将播放数量添加到列表中
        bofcshu.append(c[i + 2][1])
    # 返回前十的歌单名称和播放数量列表
    return mzi, bofcshu


# gdbflphb()

# 歌单收藏排行榜
def gendanscphb():
    # 从数据中提取收藏量列表
    bfl = typeList(da, '收藏量')
    # 将收藏量列表中的元素从字符串类型转换为整数类型
    bfl = [int(i) for i in bfl]
    # 从数据中提取歌单名称列表
    gedan = typeList(da, '名称')
    # 创建一个字典，将歌单名称作为键，收藏量作为值
    zzrqbshuj = {gedan[i]: bfl[i] for i in range(0, len(bfl) - 1)}
    # 使用 Counter 对字典进行统计，并按值从大到小排序
    c = Counter(zzrqbshuj).most_common()

    # 初始化一个空列表，用于存储符合特定格式的收藏数据
    gedanshouc = []
    # 遍历排序后的结果
    for word_pair in c:
        # 初始化一个空字典
        word_pair_dict = {}
        # 将元组转换为列表
        word_pair_list = list(word_pair)
        # 将列表元素添加到字典中
        word_pair_dict[word_pair_list[0]] = word_pair_list[1]
        # 将收藏数据转换为特定的字典格式，并添加到列表中
        gedanshouc.append(
            {
                'value': word_pair_list[1],
                'name': word_pair_list[0]
            }
        )
    # 打印前十个收藏数据（可注释掉，仅用于调试）
    # print(gedanshouc[:10])
    # 返回前十个收藏数据列表
    return gedanshouc[:10]


# gendanscphb()

# 各年发布英文专辑数量
def gnfbywzjsl():
    # 从数据中提取专辑数量列表
    yinwen = typeList(dc, '专辑数量')
    # 将专辑数量列表中的元素从字符串类型转换为整数类型
    yinwen = [int(i) for i in yinwen]
    # 以下代码由于加载太慢，已手动统计结果并赋值给 nianf
    # 创建一个字典，统计年份相同的个数
    # a = {}
    # for i in yinwen:
    #     a[i] = yinwen.count(i)
    # 手动统计的各年专辑数量
    nianf = {2004: 5104, 2005: 4991, 2006: 4931, 2007: 5004, 2008: 4960, 2009: 4901, 2010: 5083, 2011: 4938, 2012: 4948,
             2013: 5041, 2014: 5001, 2015: 4961, 2016: 4989, 2017: 5116, 2018: 4959, 2019: 5149, 2020: 5005, 2021: 4988,
             2022: 5086, 2023: 5123, 2024: 5180}
    # 将所有年份提取出来，存储在列表中
    nian = list(nianf.keys())
    # 将所有专辑数量提取出来，存储在列表中
    yfshuliang = list(nianf.values())
    # 返回年份列表和专辑数量列表
    return nian, yfshuliang


# gnfbywzjsl()

# 专辑销量类型评分榜
def zjxlpfb():
    # 从数据中提取专辑类型列表
    leix = typeList(dc, '专辑类型')
    # 从数据中提取专辑销量列表
    xiaoliang = typeList(dc, '专辑销量')
    # 将专辑销量列表中的元素从字符串类型转换为整数类型
    xiaoliang = [int(i) for i in xiaoliang]
    # 从数据中提取滚石网站评分列表
    gunshi = typeList(dc, '滚石网站评分')
    # 从数据中提取全球音乐电视台评分列表
    quanqyy = typeList(dc, '全球音乐电视台评分')
    # 从数据中提取音乐达人评分列表
    yydarpf = typeList(dc, '音乐达人评分')
    # 创建一个字典，将专辑类型作为键，销量和评分作为值
    zzrqbshuj = {leix[i]: (xiaoliang[i], gunshi[i], quanqyy[i], yydarpf[i]) for i in range(0, len(xiaoliang) - 1)}
    # 使用 Counter 对字典进行统计，并按值从大到小排序
    c = Counter(zzrqbshuj).most_common()
    # 初始化四个空列表，分别用于存储专辑类型、滚石网站评分、全球音乐电视台评分和音乐达人评分
    leixin = []
    gpf = []
    qpf = []
    ypf = []
    # 遍历排序后的结果，取前十个元素
    for i in range(0, 10):
        # 将专辑类型添加到列表中
        leixin.append(c[i][0])
        # 将滚石网站评分添加到列表中
        gpf.append(c[i][1][1])
        # 将全球音乐电视台评分添加到列表中
        qpf.append(c[i][1][2])
        # 将音乐达人评分添加到列表中
        ypf.append(c[i][1][3])
    # 返回专辑类型和三种评分列表
    return leixin, gpf, qpf, ypf


# zjxlpfb()

# 将列表转换成文档
# def baocuntex():
#     text1 = typeList(db, '歌手')
#     f = open("歌手.txt", "w")
#     f.writelines(text1)
#     f.close()
# baocuntex()

# 歌名词云图
def gmcyt():
    # 打开歌名文本文件，以只读模式，使用 UTF-8 编码
    t = open("..\\词云图\\歌名.txt", "r", encoding='utf-8')
    # 读取文件内容
    txt = t.read()  # 2.全职法师   加载txt文本
    # 使用 jieba 对文本进行分词，返回可迭代的数据
    words = jieba.cut(txt)  # 返回可迭代的数据
    # 打开停用词文件，以只读模式，使用 UTF-8 编码
    stop = open("../词云图/stopwords.txt", "r", encoding='utf-8').read()  # 加载停用词表

    # 初始化一个空字典，用于存储词语及其出现的次数
    counts = {}  # 创建列表

    # 遍历分词结果
    for word in words:
        # 如果词语不在停用词表中
        if word not in stop:  # 去除停用词
            # 如果词语长度为 1
            if len(word) == 1:
                # 则跳过该词语
                continue  # 如果字长为1则去除
            else:
                # 否则，将该词语的出现次数加 1
                counts[word] = counts.get(word, 0) + 1  # 字长不为1且不是停用词的词，频率加1
    # 将字典转换为列表
    items = list(counts.items())  # 转换为列表
    # 初始化两个空列表，分别用于存储词语和词频
    pingci = []
    shuliang = []
    # 对词频进行降序排序
    items.sort(key=lambda x: x[1], reverse=True)  # 对词频进行降序排序
    # 遍历排序后的结果，取前 200 个元素
    for i in range(200):  # 输出频率最高的前200个词
        # 将词语添加到列表中
        pingci.append(items[i][0])
        # 将词频添加到列表中
        shuliang.append(items[i][1])
    # 创建一个字典，将词语作为键，词频作为值
    zzrqbshuj = {pingci[i]: shuliang[i] for i in range(0, len(shuliang) - 1)}
    # 初始化一个空列表，用于存储符合词云图数据格式的词语数据
    ciyuntutu = []
    # 遍历字典中的键值对
    for key, value in zzrqbshuj.items():
        # 将键值对转换为词云图所需的字典格式，并添加到列表中
        ciyuntutu.append(
            {
                'value': value,
                'name': key
            }
        )
    # 打印词云图数据（可注释掉，仅用于调试）
    # print(ciyuntutu)
    # 返回词云图数据列表
    # return ciyuntutu


# gmcyt()

# 歌手词云图

# 小时时间段评论次数
def dzqsdpl():
    # 从数据中提取评论时间列表
    dianzan = typeList(dd, '评论时间')
    # 初始化一个空列表，用于存储小时信息
    xiaoshi = []
    # 遍历评论时间列表
    for i in range(0, len(dianzan)):
        # 提取评论时间中的小时信息，并添加到列表中
        xiaoshi.append(dianzan[i][0:2])
    # 将小时信息列表中的元素从字符串类型转换为整数类型
    xiaoshi = [int(i) for i in xiaoshi]
    # 使用 Counter 对小时信息进行统计，并按值从大到小排序
    c = Counter(xiaoshi).most_common()
    # 对统计结果按小时信息进行排序
    c = sorted(c)
    # 初始化一个空列表，用于存储符合特定格式的评论次数数据
    xiaoshipls = []
    # 遍历排序后的结果
    for word_pair in c:
        # 初始化一个空字典
        word_pair_dict = {}
        # 将元组转换为列表
        word_pair_list = list(word_pair)
        # 将列表元素添加到字典中
        word_pair_dict[word_pair_list[0]] = word_pair_list[1]
        # 将评论次数数据转换为特定的字典格式，并添加到列表中
        xiaoshipls.append(
            {
                'value': word_pair_list[1] * 10,
                'name': str(word_pair_list[0]) + '时'
            }
        )
    # 初始化一个空列表，用于存储评论次数
    plshu = []
    # 遍历排序后的结果，取前 23 个元素
    for i in range(0, 23):
        # 将评论次数添加到列表中
        plshu.append(c[i][1])
        # 将评论次数转换为整数类型，并乘以 10
        plshu[i] = int(plshu[i]) * 10

    # 返回评论次数数据列表和评论次数列表
    return xiaoshipls, plshu


# 歌曲时长分析
def gqscfx():
    # 从数据中提取歌曲时间列表
    shichang = typeList(db, '时间')
    # 初始化一个空列表，用于存储歌曲时长的分钟信息
    fenzhogn = []
    # 遍历歌曲时间列表
    for i in range(0, len(shichang)):
        # 提取歌曲时间中的分钟信息，并添加到列表中
        fenzhogn.append(shichang[i][0:1])
    # 将分钟信息列表中的元素从字符串类型转换为整数类型
    fenzhogn = [int(i) for i in fenzhogn]
    # 使用 Counter 对分钟信息进行统计，并按值从大到小排序
    c = Counter(fenzhogn).most_common()
    # 对统计结果按分钟信息进行排序
    c = sorted(c)
    # 初始化两个空列表，分别用于存储歌曲时长区间和歌曲数量
    shic = []
    shul = []
    # 遍历排序后的结果
    for i in range(0, len(c)):
        # 将歌曲时长区间添加到列表中
        shic.append(c[i][0])
        # 将歌曲时长区间转换为特定的字符串格式
        shic[i] = str(shic[i] + 1) + '分钟内'
        # 将歌曲数量添加到列表中
        shul.append(c[i][1])
    # 返回歌曲时长区间列表和歌曲数量列表
    return shic, shul


# gqscfx()

# 歌手词云图
def gscyt():
    # 从数据中提取歌手列表
    geshou = typeList(db, '歌手')
    # 使用 Counter 对歌手列表进行统计，并按值从大到小排序
    c = Counter(geshou).most_common()
    # 初始化一个空列表，用于存储歌手名称
    geshouccc = []
    # 遍历排序后的结果
    for i in range(0, len(c)):
        # 将歌手名称添加到列表中
        geshouccc.append(c[i][0])
    # 初始化一个空列表，用于存储符合词云图数据格式的歌手数据
    geshoucyuntu = []
    # 遍历排序后的结果
    for word_pair in c:
        # 初始化一个空字典
        word_pair_dict = {}
        # 将元组转换为列表
        word_pair_list = list(word_pair)
        # 将列表元素添加到字典中
        word_pair_dict[word_pair_list[0]] = word_pair_list[1]
        # 将歌手数据转换为词云图所需的字典格式，并添加到列表中
        geshoucyuntu.append(
            {
                'value': word_pair_list[1],
                'name': word_pair_list[0]
            }
        )
    # 返回前 32 个歌手数据列表
    return geshoucyuntu[:32]


# gscyt()