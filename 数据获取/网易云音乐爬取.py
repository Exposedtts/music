import os
import re
import json
import requests
from lxml import etree
import csv


def get_song_info(url=None):
    if url is None:
        url = 'https://music.163.com/#/playlist?id=2384642500'

    url = url.replace('/#', '').replace('https', 'http')
    out_link = 'http://music.163.com/song/media/outer/url?id='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    res = requests.get(url=url, headers=headers).text
    tree = etree.HTML(res)
    song_list = tree.xpath('//ul[@class="f-hide"]/li/a')
    artist_name_tree = tree.xpath('//h2[@id="artist-name"]/text()')
    artist_name = str(artist_name_tree[0]) if artist_name_tree else None
    song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
    song_list_name = str(song_list_name_tree[0]) if song_list_name_tree else None

    song_data_table = []

    for i, s in enumerate(song_list):
        href = str(s.xpath('./@href')[0])
        song_id = href.split('=')[-1]
        src = out_link + song_id
        title = str(s.xpath('./text()')[0])

        try:
            lyric = get_song_lyric(song_id)
        except:
            lyric = "未获取到歌词"

        song_info = {
            "歌曲名称": title,
            "歌曲ID": song_id,
            "歌曲链接": src,
            "歌手或歌单名称": artist_name if artist_name else song_list_name,
            "歌词": lyric
        }

        song_data_table.append(song_info)

    return song_data_table


def get_song_lyric(song_id):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
    }
    res = requests.get(url=url, headers=headers).text
    json_obj = json.loads(res)
    lyric = json_obj['lrc']['lyric']
    reg = re.compile(r'\[.*\]')
    lrc_text = re.sub(reg, '', lyric).strip()

    return lrc_text


def save_to_csv(data, filename='音乐数据.csv'):
    headers = ["歌曲名称", "歌曲ID", "歌曲链接", "歌手或歌单名称", "歌词"]
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    music_list = 'https://music.163.com/#/artist?id=8325'
    song_info_table = get_song_info(music_list)
    save_to_csv(song_info_table)
    print("数据已保存到音乐数据.csv")
