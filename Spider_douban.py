import requests
from bs4 import BeautifulSoup
import time
import csv



def get_movie_info(url):
    """
    获取单个页面的电影信息

    参数说明：
    url: 要爬取的页面网址

    返回值：
    movie_list: 包含电影信息的列表
    """

    # 步骤1: 设置请求头，模拟浏览器访问
    # 为什么要设置请求头？
    # 因为网站会检查访问者是不是真实的浏览器，如果不设置，可能会被拒绝访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        # 步骤2: 发送GET请求
        # timeout=10 表示如果10秒内没响应就放弃
        print(f"正在请求: {url}")
        response = requests.get(url, headers=headers, timeout=10)

        # 步骤3: 检查请求是否成功
        # 状态码200表示成功
        if response.status_code == 200:
            print("请求成功！")

            # 步骤4: 使用BeautifulSoup解析HTML
            # 'html.parser' 是Python内置的解析器
            soup = BeautifulSoup(response.text, 'html.parser')

            # 步骤5: 查找所有电影条目
            # 电影列表在 ol.grid_view 容器内的 li 标签中
            grid = soup.find('ol', class_='grid_view')
            movie_items = grid.find_all('li') if grid else []

            movie_list = []

            # 步骤6: 遍历每个电影，提取信息
            for item in movie_items:
                try:
                    # 提取电影标题
                    # find()方法找到第一个匹配的标签
                    title_tag = item.find('span', class_='title')
                    if title_tag:
                        title = title_tag.text
                    else:
                        continue

                    # 提取评分
                    rating_tag = item.find('span', class_='rating_num')
                    rating = rating_tag.text if rating_tag else '暂无评分'

                    # 提取评价人数
                    people_tag = item.find('div', class_='star')
                    if people_tag:
                        people_text = people_tag.find_all('span')[-1].text
                        # 提取数字，例如从"(123456人评价)"中提取"123456"
                        people = people_text.strip('人评价').strip('()')
                    else:
                        people = '0'

                    # 提取电影简介（一句话描述）
                    inq_tag = item.find('span', class_='inq')
                    inq = inq_tag.text if inq_tag else '暂无简介'

                    # 将提取的信息组成字典
                    movie_info = {
                        '电影名称': title,
                        '评分': rating,
                        '评价人数': people,
                        '简介': inq
                    }

                    movie_list.append(movie_info)
                    print(f"已提取: {title} - 评分: {rating}")

                except Exception as e:
                    print(f"提取某个电影信息时出错: {e}")
                    continue

            return movie_list

        else:
            print(f"请求失败，状态码: {response.status_code}")
            return []

    except Exception as e:
        print(f"发生错误: {e}")
        return []


def save_to_csv(data, filename='douban_movies.csv'):
    """
    将数据保存到CSV文件

    参数说明：
    data: 电影信息列表
    filename: 保存的文件名
    """
    if not data:
        print("没有数据可保存")
        return

    # 使用with语句打开文件，会自动关闭文件
    # newline='' 防止Windows系统出现空行
    # encoding='utf-8-sig' 让Excel能正确显示中文
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        # 创建CSV写入器
        writer = csv.DictWriter(f, fieldnames=['电影名称', '评分', '评价人数', '简介'])

        # 写入表头
        writer.writeheader()

        # 写入所有数据
        writer.writerows(data)

    print(f"数据已保存到 {filename}")


def main():
    """
    主函数：控制爬虫的执行流程
    """
    print("=" * 50)
    print("豆瓣电影Top250爬虫 - 学习版")
    print("=" * 50)

    # 存储所有电影信息
    all_movies = []

    # 豆瓣Top250分为10页，每页25部电影
    # 我们只爬取前2页（50部电影）作为学习示例
    # URL规律: start=0是第1页，start=25是第2页，以此类推
    for page in range(2):  # 爬取2页
        start = page * 25
        url = f'https://movie.douban.com/top250?start={start}'

        print(f"\n正在爬取第 {page + 1} 页...")

        # 获取当前页的电影信息
        movies = get_movie_info(url)

        # 添加到总列表
        all_movies.extend(movies)

        # 重要：休息2秒，避免请求太频繁被封IP
        # 这是爬虫礼仪，也是保护自己的方式
        print("休息2秒...")
        time.sleep(2)

    # 保存数据
    print(f"\n共爬取 {len(all_movies)} 部电影")
    save_to_csv(all_movies)

    # 打印前5部电影作为预览
    print("\n前5部电影预览:")
    for i, movie in enumerate(all_movies[:5], 1):
        print(f"{i}. {movie['电影名称']} - {movie['评分']}分")

    print("\n爬取完成！")


# 程序入口
# 这个判断确保只有直接运行这个文件时才会执行main()
# 如果被其他文件导入，则不会自动执行
if __name__ == '__main__':
    main()