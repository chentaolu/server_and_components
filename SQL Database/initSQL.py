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
sql = 'DROP TABLE IF EXISTS `Race_Record`'
cur.execute(sql)
sql = 'DROP TABLE IF EXISTS `Game_Data`'
cur.execute(sql)

sql = 'CREATE TABLE `Game_Data` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`money` int(11) DEFAULT NULL,' + \
    '`name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,' + \
    ' PRIMARY KEY (`id`)' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'
cur.execute(sql)

sql = 'CREATE TABLE `Race_Record` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`playerId` int(11) DEFAULT NULL,' + \
    '`map` int(11) DEFAULT NULL,' + \
    '`time` time(4) DEFAULT NULL,' + \
    ' PRIMARY KEY (`id`), ' + \
    ' CONSTRAINT `GD_RR_playerId` FOREIGN KEY (`playerId`) REFERENCES `Game_Data` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'

cur.execute(sql)
cur.close()
