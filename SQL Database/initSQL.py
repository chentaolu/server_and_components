# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 16:49:06 2021

@author: owner
"""
import  pymysql 

conn = pymysql.connect(
    host = '127.0.0.1', user = 'root', passwd = 'root', db = 'sys'
    )
cur  =  conn.cursor () 
sql = 'DROP TABLE IF EXISTS `Game_Data`'
cur.execute(sql)

sql = 'CREATE TABLE `Game_Data` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`score` int(11) DEFAULT NULL,' + \
    '`name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,' + \
    ' PRIMARY KEY (`id`)' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'
cur.execute(sql)