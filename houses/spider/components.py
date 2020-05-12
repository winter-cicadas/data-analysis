import requests
from lxml import etree


def get_html(url):
    """
    获取网页源代码
    :param url: 网页url
    :return: 如果状态码为200，返回正确的网页html代码，否则返回'status code error'
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return 'status code error'


def parse_page(html):
    """
    解析爬取到的网页html代码
    :param html: 需要分析的网页html
    :return: 返回一个带有本网页所有（二手房售卖）数据的列表，列表中没个元素是字典
    """
    etree_html = etree.HTML(html)
    houses = etree_html.xpath('//ul[@class="listContent"]/li')
    result = []
    for house in houses:
        info = house.xpath('./div[@class="info"]')[0]
        title = info.xpath('./div[@class="title"]/a/text()')[0]
        address = info.xpath('./div[@class="address"]/div[@class="houseInfo"]/text()')[0]
        total_price = info.xpath('./div[@class="address"]/div[@class="totalPrice"]/span/text()')
        total_price = total_price[0] if len(total_price) > 0 else 0
        flood = info.xpath('./div[@class="flood"]/div[@class="positionInfo"]/text()')[0]
        price = info.xpath('./div[@class="flood"]/div[@class="unitPrice"]/span/text()')
        price = price[0] if len(price) > 0 else 0
        deal_house_info = info.xpath('./div[@class="dealHouseInfo"]/span[@class="dealHouseTxt"]/span/text()')
        deal_house_info = deal_house_info[0] if len(deal_house_info) > 0 else ''
        deal_cycle = info.xpath('./div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span/text()')
        result.append({
            'title': title,
            'address': address,
            'total_price': total_price,
            'flood': flood,
            'price': price,
            'deal_house_info': deal_house_info,
            'deal_cycle': deal_cycle
        })
    return result

