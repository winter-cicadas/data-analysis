"""
用于字段清洗阶段中的函数
"""

import re

import numpy as np


def get_flood(item):
    """
    获取楼层高低信息
    :param item: 字段
    :return: 楼层高低
    """
    floors = ['高楼层', '中楼层', '低楼层', '地下室']
    for floor in floors:
        if floor in item:
            return floor


def get_total_floors(item):
    """
    获取楼层数
    :param item: 字段
    :return: 楼层数
    """
    result = re.findall(r'.*?\(共(\d*)层\).*?', item)
    return result[0] if result else np.NaN


def get_build_time(item):
    """
    获取建造时间
    :param item: 字段
    :return: 建造时间
    """
    result = re.findall(r'.*?(\d{4})年建.*?', item)
    return result[0] if result else np.NaN


def get_building_type(item):
    """
    获取楼型
    :param item: 字段
    :return: 楼型
    """
    buildings = ['塔楼', '板塔结合', '板楼', '平房']
    for building in buildings:
        if building in item:
            return building
    else:
        return np.NaN


def get_original_price(item):
    """
    获取挂牌价格
    :param item: 字段
    :return: 挂牌价
    """
    result = re.findall(r'挂牌(\d*)万', item)
    return result[0] if result else np.NaN


def get_close_period(item):
    """
    获取签约周期
    :param item:
    :return:
    """
    result = re.findall(r'成交周期(\d*)天', item)
    return result[0] if result else np.NaN
