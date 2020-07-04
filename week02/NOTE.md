###### 架构介绍
* 引擎（Enfine）
* 调度器（Scheduler）
* 下载器（Downloader）
* 爬虫（Spiders）
* 项目管道（Item Pipeline）
* 下载器中间件（Downloader Middlewares）
* 爬虫中间件（Spider MIddlewares）
###### 数据流程
* Engine 首先打开一个网站及处理该网站的 Spider 并向该 Spider 请求第一个要爬取的 URL
* Engine 从 Spider 获取第一个要爬取的 URL 并通过 Schedule 以 Request 的形式调度
* Engine 向 Schedule 请求下一个要爬取的 URL
* Schedule 返回下一个要爬取的 URL 给 Engine 将 URL 通过 Downloader Middlewares 转发给 Downloader 下载
* 一旦页面下载完毕 Downloader 生成该页面的 Request 并将其通过 Downloader Middlewares 发送给 Engine
* Engine 从 Downloader 中接收到 Response 并将其通过 Spider Middlewares 发送给 Spider 处理
* Spider 处理 Response 并返回提取到的 Item及新的 Request 给 Engine
* Engine 将 Spider 返回的 Item 给 Item Pipeline 将新的 Request 给 Schedule
* 重复以上步骤直到 Schedule 中没有更多的 Request 关闭 Engine 爬虫结束
###### 项目实践
* 创建项目：scrapy startproject tutorial
1. 项目模块文件：tutorial/
1.1 爬取处理文件：spiders/
1.2 爬取数据结构：items.py
1.3 爬取的中间件：middlewares.py
1.3 定义数据管道：pipelines.py
1.4 项目配置文件：settings.py
2. 部署配置文件：scrapy.cfg
* 制作爬虫 -> Spider
1. 两件事情
1.1 定义爬取网页的动作
1.2 分析爬取下来的网页
2. 运行流程
2.1 以初始的 URL 初始化 Request 并设置回调函数
2.2 当 Request 成功请求并返回 Response 生成并作为参数传给该回调函数
2.3 在回调函数内分析返回的网页内容
2.4 如果返回的是字典或 Item 对象将返回结果保存到文件
2.5 如果返回的是链接 构造 Request 并设置新的回调函数等待后续调度
2.6 重复以上步骤直到完成站点的爬取 
3. Selector 的用法
3.1 直接使用
3.2 Scrapy shell：scrapy shell https://...
3.3 XPath 选择器
3.4 CSS 选择器
3.5 正则匹配
4. Spider 类分析
```
cd tutorial
scrapy genspider quotes quotes.toscrape.com
```
```
import scrapy


class QuotesSpider(scrapy.Spider):
    # 每个项目唯一名称
    name = 'quotes'
    # 允许爬取的域名（可选配置）
    allowed_domains = ['quotes.toscrape.com']
    # 起始 URL 列表：没有实现 start_request() 方法时默认开始抓取
    start_urls = ['http://quotes.toscrape.com/']

    # 解析返回的响应、提取数据或进一步生成要处理的请求
    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = TutorialItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        # 通过 CSS 选择器获取下一个页面的链接
        next = response.css('.pager .next a::attr("href")').extract_first()
        # 调用 urljoin() 方法将相对 URL 构造成绝对 URL
        url = response.urljoin(next)
        # 通过 url 和 callback 回调函数构造一个新的请求
        yield scrapy.Request(url=url, callback=self.parse)
```
* 提取信息 -> Item
```
import scrapy


class TutorialItem(scrapy.Item):
    collection = table = 'quotes'
    
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```
* 存储信息
1. 运行时存储 -> Feed Exports
1.1 scrapy crawl quotes -o quotes.json/jl/jsonlines
1.2 scrapy crawl quotes -o quotes.csv
1.3 scrapy crawl quotes -o quotes.xml
1.4 scrapy crawl quotes -o quotes.pickle
1.5 scrapy crawl quotes -o quotes.marshal
1.6 scrapy crawl quotes -o ftp://user:pass@ftp.example.com/..
2. 使用数据管道 -> Item Pipelines
2.1 清理 HTML 数据
2.2 验证爬取数据及检查爬取字段
2.3 查重并丢弃重复内容
2.4 将爬取结果保存到数据库等
```
from scrapy.exceptions import DropItem


class TutorialPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')
```
```
import pymongo


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 获取 settings.py 中的配置
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
```
```
import pymysql


class MysqlPipeline(object):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.databse = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MUSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host,
                                  self.user,
                                  self.password,
                                  self.databse,
                                  charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
```
```
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, res, item, info):
        images_paths = [x['path'] for ok, x in res if ok]
        if not images_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'])
```
```
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'tutorial.pipelines.TutorialPipeline': 300,
    'tutorial.pipelines.MongoPipeline': 301,
    'tutorial.pipelines.MysqlPipeline': 302,
    'tutorial.pipelines.ImagePipeline': 303
}

IMAGES_STORE = './images'

MAX_PAGE = 50

MONGO_URI = 'xxx.xxx'
MONGO_DB = 'tutorial'

MYSQL_HOST = 'xxx.xxx'
MYSQL_DATABASE = 'xxx'
MYSQL_USER = 'xxx'
MYSQL_PASSWORD = 'xxx'
MYSQL_PORT = 3306
```
* 中间件 -> Middlewares
1. Downloader Middleware：异常处理 & 应对反爬虫
1.1 from_crawler(cls, crawler)：创建中间件并（必须）返回中间件对象
1.1 process_request(request, spider)：优先级高先调用
1.2 process_response(request, response, spider)：优先级高后调用
1.3 process_exception(request, exception, spider)：异常时调用
```
from scrapy import signals
from scrapy.exceptions import NotConfigured

from urllib.parse import urlparse
from collections import defaultdict
import random


class RandomHttpProxyMiddleware:
    def __init__(self, auth_encoding='utf-8', proxy_list=None):
        self.user_agent = [
            'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1'
        ]
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
        return cls(auth_encoding, http_proxy_list)

    def process_request(self, request, scheme):
        request.meta['proxy'] = random.choice(self.proxies[scheme])
        request.headers['User-Agent'] = random.choice(self.user_agent)

    def process_response(self, request, response, spider):
        response.status = 201
        return response
```
```
DOWNLOADER_MIDDLEWARES = {
    'maoyan.middlewares.MaoyanDownloaderMiddleware': 543,
    'maoyan.middlewares.RandomHttpProxyMiddleware': 400
}

HTTP_PROXY_LIST = [
    'http://52.179.231.206:80',
    'http://95.0.194.241.9090',
]
```
2. Spider Middleware：必要情况下用来方便数据的处理
2.1 process_spider_input(response, spider)
2.2 process_spider_output(response, result, spider)
2.3 process_spider_exception(response, exception, spider)
2.4 process_start_requests(start_requests, spider)
###### 高级功能
* Scrapy 对接 Selenium
* Scrapy 对接 Splash
* Scrapy 通用爬虫
* Scrapyrt 的使用
* Scrapy 对接 Docker