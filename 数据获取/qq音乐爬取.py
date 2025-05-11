import asyncio
import aiohttp
import re
import csv


async def fetch(session, url, headers):
    """
    异步获取网页内容
    :param session: aiohttp 会话对象
    :param url: 要请求的网页 URL
    :param headers: 请求头信息
    :return: 网页内容
    """
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def process_page(session, page_num, base_url, headers):
    """
    处理单页数据，提取歌曲信息
    :param session: aiohttp 会话对象
    :param page_num: 当前页码
    :param base_url: 基础 URL
    :param headers: 请求头信息
    :return: 该页的歌曲信息列表
    """
    page_url = base_url.format(page_num)
    res = await fetch(session, page_url, headers)
    # 这里需要根据实际 QQ 音乐页面结构调整正则表达式来提取信息
    song_names = re.findall(r'<span class="songname">(.*?)</span>', res)
    singers = re.findall(r'<span class="singername">(.*?)</span>', res)
    albums = re.findall(r'<span class="albumname">(.*?)</span>', res)
    durations = re.findall(r'<span class="interval">(.*?)</span>', res)

    song_data = []
    for song_name, singer, album, duration in zip(song_names, singers, albums, durations):
        song_info = {
            "歌曲名称": song_name,
            "歌手": singer,
            "专辑": album,
            "时长": duration
        }
        song_data.append(song_info)
        await asyncio.sleep(1)  # 设置请求间隔时间为 1 秒
    return song_data


async def main():
    """
    主函数，协调异步任务
    :return: 所有页面的歌曲信息列表
    """
    # 假设这是 QQ 音乐排行榜的分页 URL 模板，实际需要根据真实情况调整
    base_url = 'https://y.qq.com/n/yqq/toplist/4.html?ADTAG=myqq&from=myqq&channel=10007100&page={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        # 假设爬取前 5 页，可根据需要调整
        for page_num in range(1, 6):
            task = asyncio.create_task(process_page(session, page_num, base_url, headers))
            tasks.append(task)

        all_song_data = []
        for task in tasks:
            page_song_data = await task
            all_song_data.extend(page_song_data)

    return all_song_data


def save_to_csv(data, filename='qq_music_data.csv'):
    """
    将歌曲信息保存到 CSV 文件
    :param data: 歌曲信息列表
    :param filename: 保存的 CSV 文件名
    """
    headers = ["歌曲名称", "歌手", "专辑", "时长"]
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    song_info_table = loop.run_until_complete(main())
    save_to_csv(song_info_table)
    print("数据已保存到 qq_music_data.csv")

