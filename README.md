# 豆瓣电影 Top250 爬虫

一个用于爬取豆瓣电影 Top250 数据的 Python 爬虫项目，支持保存到 CSV 文件和 MySQL 数据库。

## 功能特性

- 爬取豆瓣电影 Top250 的电影信息（名称、评分、评价人数、简介）
- 支持数据保存到 CSV 文件
- 支持数据保存到 MySQL 数据库
- 使用 `fake-useragent` 动态生成随机 User-Agent，降低被反爬的风险
- 完整的请求头模拟，更接近真实浏览器访问

## 环境要求

- Python 3.6+
- MySQL 5.7+

## 安装步骤

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd Practical-case
```

### 2. 安装依赖

```bash
pip install requests beautifulsoup4 pymysql fake-useragent
```

### 3. 配置数据库

创建 `config.py` 文件（该文件已在 `.gitignore` 中，不会被提交）：

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的密码',
    'database': 'douban_spider',
    'charset': 'utf8mb4'
}
```

### 4. 创建数据库和表

在 MySQL 中执行：

```sql
CREATE DATABASE IF NOT EXISTS douban_spider DEFAULT CHARSET utf8mb4;

USE douban_spider;

CREATE TABLE IF NOT EXISTS movies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    rating VARCHAR(10),
    people VARCHAR(20),
    quote VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 使用方法

```bash
python Spider_douban.py
```

运行后会：
1. 爬取豆瓣电影 Top250 数据
2. 保存到 `douban_movies.csv` 文件
3. 保存到 MySQL 数据库的 `movies` 表

## 项目结构

```
Practical case/
├── Spider_douban.py    # 主爬虫程序
├── config.py           # 配置文件（需自行创建，包含数据库密码）
├── README.md           # 项目说明
└── .gitignore          # Git 忽略文件
```

## 技术要点

| 技术点 | 说明 |
|--------|------|
| requests | 发送 HTTP 请求 |
| BeautifulSoup | 解析 HTML 页面 |
| pymysql | 连接 MySQL 数据库 |
| fake-useragent | 动态生成随机 User-Agent |

## 注意事项

- 请遵守网站的 robots.txt 协议
- 爬取间隔设置为 2 秒，避免对服务器造成压力
- 本项目仅供学习交流使用

## License

MIT
