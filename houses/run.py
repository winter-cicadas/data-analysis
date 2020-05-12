import pandas as pd
import matplotlib.pyplot as plt

from analysis_function import *
from spider.main_spider import get_spiders
from spider.mysql_helper import get_connect

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def main():
    """
    主函数，程序入口, 主要为数据分析相关的代码
    :return: None
    """
    # 爬取数据存入数据库，第一次运行本程序时需要下面这一句，之后就直接注释掉即可
    get_spiders()
    # 连接数据库，读取数据
    connect = get_connect()
    house_info = pd.read_sql('select * from houseinfo', connect)

    # 数据清洗
    # 保留原数据
    data = house_info.copy()
    # 拆除title字段，得到location、apartment、size三个字段
    data['location'] = data.title.str.split(' ', expand=True)[0]
    data['apartment'] = data.title.str.split(' ', expand=True)[1]
    data.apartment.replace(r'房间', '室', regex=True, inplace=True)
    data['size'] = data.title.str.split(' ', expand=True)[2].apply(lambda x: x[:-2] if x else np.NaN)
    # 拆除address字段，得到direction和renovation两个字段
    data['direction'] = data.address.str.split('|', expand=True)[0]
    data['renovation'] = data.address.str.split('|', expand=True)[1]
    data.drop('address', axis=1, inplace=True)
    # flood，得到floor、total_floors、build_time、building_type四个字段
    data['floor'] = data.flood.apply(get_flood)
    data['total_floors'] = data.flood.apply(get_total_floors)
    data['build_time'] = data.flood.apply(get_build_time)
    data['building_type'] = data.flood.apply(get_building_type)
    data.drop('flood', axis=1, inplace=True)
    # 拆除deal_cycle字段，得到original_price和close_period字段
    data['original_price'] = data.deal_cycle.apply(get_original_price)
    data['close_period'] = data.deal_cycle.apply(get_close_period)
    data.drop('deal_cycle', axis=1, inplace=True)
    # 异常数据处理（单价异常）
    # 删除无价格数据行
    data = data[data.price > 0]
    # 房屋信息数据替换
    data.deal_house_info.replace('', '无', inplace=True)
    # 房屋建造时间空值填充
    data.build_time.fillna(method='pad', axis=0, inplace=True)
    # 建筑类型空值填充
    data.building_type.fillna(method='pad', axis=0, inplace=True)
    # 挂牌价格填充
    data.original_price.fillna(value=data.total_price, inplace=True)
    # 判断是否为车位，分离车位和非车位数据
    data['is_parking_lot'] = data.title.apply(lambda x: True if x.find('车位') != -1 else False)
    data.drop('title', axis=1, inplace=True)
    data_parking_lot = data[data['is_parking_lot'] == True]
    data_parking_lot = data_parking_lot[['location', 'price', 'total_price']]
    data_house = data[data['is_parking_lot'] == False]
    data_house.drop(['is_parking_lot', 'id'], axis=1, inplace=True)
    # 修改数据类型
    data_house.total_floors = data_house.total_floors.astype(np.int)
    data_house.build_time = data_house.build_time.astype(np.int)
    data_house.original_price = data_house.original_price.astype(np.float)
    data_house.close_period = data_house.close_period.astype(np.int)
    data_house['size'] = data_house['size'].astype(np.float)
    # 单位造成的误会
    data_house['total_price'] = data_house.total_price.apply(lambda x: x * 10000)
    data_house['original_price'] = data_house.original_price.apply(lambda x: x * 10000)
    data_parking_lot['total_price'] = data_parking_lot.total_price.apply(lambda x: x * 10000)
    # 重建索引
    data_house = data_house.reset_index(drop=True)
    data_parking_lot = data_parking_lot.reset_index(drop=True)
    # 将清洗后的数据导出为excel
    data_house.to_excel('./result_data/houses.xlsx')
    data_parking_lot.to_excel('./result_data/parking_lot.xlsx')

    # 数据分析及可视化
    # 户型数量可视化
    apartment = data_house.apartment.value_counts()
    plt.figure(1)
    plt.bar(apartment.index, apartment)
    plt.plot(apartment.index, apartment, 'r-*')
    for x, y in zip(apartment.index, apartment):
        plt.text(x, y, f'{y}')
    plt.xlabel('户型')
    plt.xticks(rotation=45)
    plt.ylabel('数量')
    plt.title('成交户型的数量')
    plt.savefig('./result_data/成交户型的数量.png')
    plt.show()

    # 房源优势数据可视化
    explode = [0.05, 0.01, 0.01, 0.01]
    label = np.array(data_house.deal_house_info.value_counts().index)
    plt.figure(2)
    plt.title('房源优势数据可视化')
    plt.pie(data_house.deal_house_info.value_counts(), explode=explode, labels=label, shadow=True)
    plt.savefig('./result_data/房源优势数据可视化.png')
    plt.show()

    # 房源位置售出数量可视化
    result = data_house.location.value_counts()
    result.sort_values(ascending=True, inplace=False)
    result = result[:30]
    plt.figure(3)
    plt.bar(result.index, result)
    plt.xlabel('售出数量')
    plt.xticks(rotation=85)
    plt.ylabel('房源位置')
    plt.title('房源售出数量与位置的关系图')
    plt.savefig('./result_data/房源售出数量与位置的关系.png')
    plt.show()

    # 房价和面积对比
    plt.figure(4)
    plt.scatter(data_house['size'], data_house['price'])
    plt.title('房价-面积关系图')
    plt.xlabel('房面积')
    plt.ylabel('单价')
    plt.savefig('./result_data/房价-面积关系.png')
    plt.show()

    # 最贵房价小区
    plt.figure(5)
    area = data_house.groupby('location').price.mean().sort_values(ascending=False)[:50]
    plt.bar(area.index, area)
    plt.title('房价最贵小区TOP50')
    plt.xticks(rotation=85)
    plt.xlabel('小区')
    plt.ylabel('房价')
    plt.savefig('./result_data/房价最贵小区TOP50.png')
    plt.show()

    # 装修程度和楼层高低对售卖数量的影响
    result = data_house.pivot_table(index=['floor'], columns=['renovation'], values=['total_price'], aggfunc=len)
    df = pd.DataFrame(result)
    renovation_percent = pd.DataFrame(dict(df.sum()/df.sum().sum()), index=['百分比'])
    df['百分比'] = df.sum(axis=1) / df.sum(axis=1).sum()
    df['百分比'] = df['百分比'].apply(lambda x: '%.2f%%' % (x * 100))
    df = pd.concat([df, renovation_percent])
    df.loc['百分比'] = df.loc['百分比'].apply(lambda x: '%.2f%%' % (x * 100))
    df.replace('nan%', '', inplace=True)
    df.to_excel('./result_data/装修程度和楼层高低透视表.xlsx')


if __name__ == '__main__':
    main()
