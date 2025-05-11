import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time
import random

# 定义一些常用的User - Agent列表
USER_AGENTS = [
    'https://u6.y.qq.com/cgi-bin/musics.fcg?_=1744526615199&sign=zzceec4bcfk8qhwmdyer4is7svoeb6py9opwkba04f6b2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]


class MusicCrawler:
    def __init__(self):
        # 随机选择一个User - Agent
        self.headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'https://y.qq.com'
        }

    def _get_response(self, url, params):
        max_retries = 3  # 最大重试次数
        for retry in range(max_retries):
            try:
                # 每次请求前随机选择一个User - Agent
                self.headers['User-Agent'] = random.choice(USER_AGENTS)
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()  # 检查响应状态码
                return response
            except requests.RequestException as e:
                print(f"请求出错，第 {retry + 1} 次重试: {e}")
                # 每次重试前等待随机时间
                time.sleep(random.uniform(1, 3))
        print("达到最大重试次数，请求失败。")
        return None

    def crawl_qq_music(self):
        """爬取QQ音乐信息"""
        url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg"
        params = {
            'topid': '26',  # 热歌榜
            'format': 'json',
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'platform': 'yqq.json'
        }
        response = self._get_response(url, params)
        if response is None:
            return []
        data = response.json()
        songs = []
        if 'songlist' in data:
            for song in data['songlist']:
                song_data = song['data']
                song_info = {
                    '歌名': song_data.get('songname', ''),
                    '歌手': song_data.get('singer', [{'name': ''}])[0].get('name', ''),
                    '专辑': song_data.get('albumname', ''),
                    '时长': str(song_data.get('interval', 0)) + '秒',
                    '爬取时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                songs.append(song_info)
                print(f"已获取歌曲: {song_info['歌名']} - {song_info['歌手']}")
        # 每次爬取完一个网站的信息后，等待随机时间
        time.sleep(random.uniform(1, 3))
        return songs

    def crawl_netease_music(self):
        """爬取网易云音乐信息"""
        url = "https://music.163.com/api/playlist/detail"
        params = {
            "id": "3778678",  # 热歌榜ID
            "offset": 0,
            "total": True,
            "limit": 100
        }
        response = self._get_response(url, params)
        if response is None:
            return []
        data = response.json()
        songs = []
        if 'result' in data and 'tracks' in data['result']:
            for song in data['result']['tracks']:
                song_info = {
                    '歌名': song.get('name', ''),
                    '歌手': song.get('artists', [{'name': ''}])[0]['name'],
                    '专辑': song.get('album', {}).get('name', ''),
                    '时长': str(song.get('duration', 0) // 1000) + '秒',
                    '爬取时间': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                songs.append(song_info)
                print(f"已获取歌曲: {song_info['歌名']} - {song_info['歌手']}")
        # 每次爬取完一个网站的信息后，等待随机时间
        time.sleep(random.uniform(1, 3))
        return songs

    def save_to_csv(self, songs, filename):
        """保存数据到CSV文件"""
        if songs:
            df = pd.DataFrame(songs)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"数据已保存到 {filename}")
            print(f"共获取 {len(songs)} 首歌曲")
        else:
            print("没有数据可保存")


def main():
    crawler = MusicCrawler()
    print("开始爬取QQ音乐...")
    qq_songs = crawler.crawl_qq_music()
    crawler.save_to_csv(qq_songs, 'qq_music_songs.csv')

    print("\n开始爬取网易云音乐...")
    netease_songs = crawler.crawl_netease_music()
    crawler.save_to_csv(netease_songs, 'netease_music_songs.csv')


if __name__ == "__main__":
    main()
