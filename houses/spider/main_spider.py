import time

from spider.components import get_html, parse_page
from spider.mysql_helper import get_connect, insert_data


def get_spider(page, db):
    """
    爬取一页网页并解析，将解析的数据写入数据库中
    :param page: 要爬取的当前网页页数
    :param db: 解析好的数据需要存进的数据库
    :return: None
    """
    url = f'https://cd.lianjia.com/chengjiao/pg{page}/'
    html = get_html(url)
    if html == 'status code error':
        print(html)
    information = parse_page(html)
    insert_data(information, db)


def get_spiders():
    """
    爬取所有的网页命令
    :return: None
    """
    db = get_connect()
    for page in range(1, 101):
        get_spider(page, db)
        print(f'======{page}=========')
        time.sleep(3)
    db.close()
