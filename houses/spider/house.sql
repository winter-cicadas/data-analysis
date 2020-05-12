# 本文件为准备存储爬虫爬取的数据的数据库操作，包括创建书库、数据表

# 创建数据库houses
CREATE DATABASE houses;

# 切换数据库到houses
USE houses;


# 创建存储数据的表格
CREATE TABLE IF NOT EXISTS houseinfo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(30) NOT NULL,
    address VARCHAR(20) NOT NULL,
    total_price FLOAT NOT NULL,
    flood VARCHAR(30) NOT NULL,
    price INT NOT NULL,
    deal_house_info VARCHAR(20),
    deal_cycle VARCHAR(30) not null
) ENGINE=innodb DEFAULT CHARSET=utf8;
