import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析网页
import pandas as pd  # 存取csv
from time import sleep  # 等待时间

music_name = []  # 专辑名称
music_url = []  # 专辑链接
music_star = []  # 专辑评分
music_star_people = []  # 评分人数
music_singer = []  # 歌手
music_pub_date = []  # 发行日期
music_type = []  # 类型
music_media = []  # 介质
music_style = []  # 曲风


def get_music_info(url, headers):
	"""
	获取豆瓣音乐详情数据
	:param url: 爬取地址
	:param headers: 爬取请求头
	:return: None
	"""
	res = requests.get(url, headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')
	for music in soup.select('.item'):
		name = music.select('.pl2 a')[0].text.replace('\n', '').replace('                ', ' ').strip()  # 专辑名称
		music_name.append(name)
		url = music.select('.pl2 a')[0]['href']  # 专辑链接
		music_url.append(url)
		try:
			star = music.select('.rating_nums')[0].text  # 电影评分
		except:
			star = ''
		music_star.append(star)
		star_people = music.select('.pl')[1].text  # 评分人数
		star_people = star_people.strip().replace(' ', '').replace('人评价', '').replace('(\n', '').replace('\n)',
		                                                                                                 '')  # 数据清洗
		music_star_people.append(star_people)
		music_infos = music.select('.pl')[0].text.strip()  # 歌手、发行日期、类型、介质、曲风
		# print('music_infos is:')
		# print(music_infos)
		if name == '浮躁' or name == '3颗猫饼干 三颗猫饼干 / Three Cat Cookies':
			singer = music_infos.split(' / ')[0]
			music_singer.append(singer)
			pub_date = music_infos.split(' / ')[1]
			music_pub_date.append(pub_date)
			type = None
			music_type.append(type)
			media = music_infos.split(' / ')[2]
			music_media.append(media)
			style = music_infos.split(' / ')[3]
			music_style.append(style)
		elif name == '陪我歌唱 苏打绿台北小巨蛋演唱会Live Cd:陪我歌唱':
			singer = music_infos.split(' / ')[0]
			music_singer.append(singer)
			pub_date = music_infos.split(' / ')[1]
			music_pub_date.append(pub_date)
			type = music_infos.split(' / ')[2]
			music_type.append(type)
			media = music_infos.split(' / ')[3]
			music_media.append(media)
			style = None
			music_style.append(style)
		else:
			singer = music_infos.split(' / ')[0]
			music_singer.append(singer)
			pub_date = music_infos.split(' / ')[1]
			music_pub_date.append(pub_date)
			type = music_infos.split(' / ')[2]
			music_type.append(type)
			media = music_infos.split(' / ')[3]
			music_media.append(media)
			style = music_infos.split(' / ')[4]
			music_style.append(style)


def save_to_csv(csv_name):
	"""
	数据保存到csv
	:return: None
	"""
	df = pd.DataFrame()  # 初始化一个DataFrame对象
	df['专辑名称'] = music_name
	df['专辑链接'] = music_url
	df['专辑评分'] = music_star
	df['评分人数'] = music_star_people
	df['歌手'] = music_singer
	df['发行日期'] = music_pub_date
	df['类型'] = music_type
	df['介质'] = music_media
	df['曲风'] = music_style
	df.to_csv(csv_name, encoding='utf_8_sig')  # 将数据保存到csv文件


if __name__ == "__main__":
	# 定义一个请求头(防止反爬)
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	# 开始爬取豆瓣数据
	for i in range(10):  # 爬取共10页，每页25条数据
		page_url = 'https://music.douban.com/top250?start={}'.format(str(i * 25))
		print('开始爬取第{}页，地址是:{}'.format(str(i + 1), page_url))
		get_music_info(page_url, headers)
		sleep(1)  # 等待1秒(防止反爬)
	# 保存到csv文件（第456页只有24首，所以总数量是247）
	save_to_csv(csv_name="musicDouban250.csv")