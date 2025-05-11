# 导入 requests 库，用于发送 HTTP 请求，获取网页内容
import requests
# 导入 BeautifulSoup 类，用于解析 HTML 或 XML 文档
from bs4 import BeautifulSoup
# 导入 time 模块，用于添加时间延迟，避免对目标网站造成过大压力
import time

# 设置请求头，模拟浏览器访问，避免被网站识别为爬虫而拒绝访问
# 这里的 "xxx" 应替换为真实的用户代理字符串，示例中给出一个常见的 Chrome 浏览器的 User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 定义一个函数，用于从指定 URL 获取酷狗音乐排行榜的歌曲信息
def get_info(url):
    try:
        # 通过请求头和 url 链接，发送 HTTP 请求，获取整体网页页面信息
        # 使用 requests 库的 get 方法发送请求，传入 url 和请求头
        web_data = requests.get(url, headers=headers)
        # 检查请求的响应状态码，如果状态码不是 200（表示请求成功），则抛出异常
        web_data.raise_for_status()

        # 对返回的结果进行解析，使用 'lxml' 解析器来解析 HTML 内容
        # 创建 BeautifulSoup 对象，传入网页内容和解析器类型
        soup = BeautifulSoup(web_data.text, 'lxml')

        # 找到具体的相同的数据的内容位置和内容
        # 使用 CSS 选择器找到所有歌曲的排名信息
        ranks = soup.select('span.pc_temp_num')
        # 使用 CSS 选择器找到所有歌曲的标题和歌手信息
        titles = soup.select('div.pc_temp_songlist > ul > li > a')
        # 使用 CSS 选择器找到所有歌曲的时长信息
        times = soup.select('span.pc_temp_tips_r > span')

        # 提取具体的文字内容
        # 使用 zip 函数同时遍历排名、标题和时长信息
        for rank, title, song_time in zip(ranks, titles, times):
            # 分割标题信息，获取歌手和歌曲名称
            singer, song = title.get_text().split('-', 1)
            # 创建一个字典，存储每条歌曲的详细信息
            data = {
                'rank': rank.get_text().strip(),  # 排名信息，去除前后空格
                'singer': singer.strip(),  # 歌手信息，去除前后空格
                'song': song.strip(),  # 歌曲名称，去除前后空格
                'time': song_time.get_text().strip()  # 歌曲时长，去除前后空格
            }
            # 打印每条歌曲的详细信息
            print(data)
    except requests.RequestException as e:
        # 若请求过程中出现异常，打印错误信息
        print(f"请求出错: {e}")
    except ValueError:
        # 若在分割标题信息时出现异常，打印错误信息
        print(f"解析标题信息出错，URL: {url}")

# 程序入口，当脚本作为主程序运行时执行以下代码
if __name__ == '__main__':
    # 生成要爬取的网页 URL 列表
    # 使用列表推导式生成从 1 到 2 的 URL 列表，用于访问酷狗音乐排行榜的不同页面
    urls = ['https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(i) for i in range(1, 2)]
    # 遍历 URL 列表，对每个 URL 调用 get_info 函数进行数据提取
    for url in urls:
        get_info(url)
        # 每次请求后暂停 1 秒，避免对目标网站造成过大压力，降低被反爬机制拦截的风险
        time.sleep(1)