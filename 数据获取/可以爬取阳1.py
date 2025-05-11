import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time

class MusicCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://y.qq.com',
            'sec - ch - ua':'"Microsoft Edge"; v = "135", "Not-A.Brand";  v = "8", "Chromium"; v = "135"',
            'path':'/cgi-bin/musics.fcg?_=1744861442383&sign=zzcf305b9afjtun6kdzcemxlj0nsdda8fgla8bf4fa777'

        }

    def crawl_qq_music(self):
        """爬取QQ音乐信息"""
        try:
            # 使用QQ音乐新版API
            url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg"
            params = {
                'topid': '26',  # 热歌榜
                'format': 'json',
                'inCharset': 'utf-8',
                'outCharset': 'utf-8',
                'platform': 'yqq.json'
            }
            
            response = requests.get(url, params=params, headers=self.headers)
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
            
            return songs
            
        except Exception as e:
            print(f"爬取QQ音乐时出错: {str(e)}")
            return []

    def crawl_netease_music(self):
        """爬取网易云音乐信息"""
        try:
            # 使用网易云音乐热歌榜API
            url = "https://music.163.com/api/playlist/detail"
            params = {
                "id": "3778678",  # 热歌榜ID
                "offset": 0,
                "total": True,
                "limit": 100
            }
            
            response = requests.get(url, params=params, headers=self.headers)
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
            
            return songs
            
        except Exception as e:
            print(f"爬取网易云音乐时出错: {str(e)}")
            return []

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
    
    # 爬取QQ音乐
    print("开始爬取QQ音乐...")
    qq_songs = crawler.crawl_qq_music()
    crawler.save_to_csv(qq_songs, 'qq_music_songs.csv')
    
    # 等待一下，避免请求过快
    time.sleep(2)
    
    # 爬取网易云音乐
    print("\n开始爬取网易云音乐...")
    netease_songs = crawler.crawl_netease_music()
    crawler.save_to_csv(netease_songs, 'netease_music_songs.csv')

if __name__ == "__main__":
    main() 