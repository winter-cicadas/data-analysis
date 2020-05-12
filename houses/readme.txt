"""
author: yelin
website: https://yelin.site
qq: 2929947176
作者是个菜鸟，有问题或者有更好的建议请联系作者
"""

读者须知
#######请忽略程序运行后产生的警告信息#################

文件夹介绍：
result_data:本文件夹存储的是运行整个程序后产生的数据表和图
spider:本文件夹存储的是在链家官网爬取数据的代码，包括数据库的创建和数据存储

如果不想运行本程序，仅需根据程序结合result_data文件夹中的数据即可

如果需要运行本程序，需要一下几个步骤准备：：
1.创建一个python虚拟环境，并根据requirements.txt中的库安装，为提升下载速度，可加上镜像文件：
pip install -r requirements.txt -i https://pypi.douban.com/simple/
2.根据spider文件夹house.sql文件中的sql语句在本地创建数据库和数据表
3.修改spider文件夹mysql_helper.py文件get_connect方法中的连接数据库的参数
4.运行整个程序run.py即可
