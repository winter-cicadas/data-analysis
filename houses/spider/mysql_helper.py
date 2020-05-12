import pymysql


def get_connect():
    """
    连接mysql数据库
    :return: 一个连接对象
    """
    host = 'localhost'
    user = 'root'
    password = '123456'
    database = 'houses'
    port = 3306
    conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
    return conn


def insert_data(datas: list, connect):
    """
    根据输入的连接对象和数据插入数据
    :param datas: 需要插入的数据列表
    :param connect: 数据库连接对象
    :return: None
    """
    cursor = connect.cursor()
    sql = 'INSERT INTO houseinfo ' \
          '(title, address, total_price, flood, price, deal_house_info, deal_cycle)' \
          'VALUES' \
          '(%s, %s, %s, %s, %s, %s, %s)'
    for data in datas:
        values = (data['title'], data['address'], data['total_price'], data['flood'], data['price'],
                  data['deal_house_info'], '/'.join(data['deal_cycle']))
        cursor.execute(sql, values)
        connect.commit()
    cursor.close()


def close_db(connect):
    """
    关闭一个数据库连接
    :param connect: 一个数据库连接对象
    :return: None
    """
    connect.close()
