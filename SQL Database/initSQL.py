# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 16:49:06 2021

@author: owner
"""
import  pymysql 

conn = pymysql.connect(
    host = '127.0.0.1', user = 'root', passwd = 'root', db = 'fly_in_nature'
    )
cur  =  conn.cursor ()

sql = 'DROP TABLE IF EXISTS `Purchase_Record`'
cur.execute(sql)
sql = 'DROP TABLE IF EXISTS `Broom`'
cur.execute(sql)
sql = 'DROP TABLE IF EXISTS `Race_Record`'
cur.execute(sql)
sql = 'DROP TABLE IF EXISTS `Game_Data`'
cur.execute(sql)
sql = 'DROP TABLE IF EXISTS `Map`'
cur.execute(sql)




sql = 'CREATE TABLE `Game_Data` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`money` int(11) DEFAULT NULL,' + \
    '`name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,' + \
    ' PRIMARY KEY (`id`)' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'
cur.execute(sql)

Sql = "INSERT INTO fly_in_nature.game_data (`money`, `name`) VALUES (10000, 'testPlayer')"
cur.execute(Sql)
conn.commit()

sql = 'CREATE TABLE `Map` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`name` char(45) COLLATE utf8_unicode_ci DEFAULT NULL,' + \
    ' PRIMARY KEY (`id`)' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'
cur.execute(sql)

Sql = "INSERT INTO fly_in_nature.Map (`name`) VALUES ('finger')"
cur.execute(Sql)
conn.commit()

Sql = "INSERT INTO fly_in_nature.Map (`name`) VALUES ('herry_potter')"
cur.execute(Sql)
conn.commit()


sql = 'CREATE TABLE `Race_Record` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`playerId` int(11) DEFAULT NULL,' + \
    '`mapId` int(11) DEFAULT NULL,' + \
    '`time` time(2) DEFAULT NULL,' + \
    ' PRIMARY KEY (`id`), ' + \
    ' CONSTRAINT `GD_RR_playerId` FOREIGN KEY (`playerId`) REFERENCES `Game_Data` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION, ' + \
    ' CONSTRAINT `M_RR_playerId` FOREIGN KEY (`mapId`) REFERENCES `Map` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION ' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'

cur.execute(sql)

sql = 'CREATE TABLE `Broom` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL, ' + \
    '`speed` int(11) DEFAULT NULL, ' + \
    '`price` int(11) DEFAULT NULL, ' + \
    ' PRIMARY KEY (`id`)' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'

cur.execute(sql)

Sql = "INSERT INTO fly_in_nature.Broom (`name`, `speed`, `price`) VALUES ('originBroom', 16000, 0)"
cur.execute(Sql)
conn.commit()

Sql = "INSERT INTO fly_in_nature.Broom (`name`, `speed`, `price`) VALUES ('magicBroom', 18000, 1000)"
cur.execute(Sql)
conn.commit()


sql = 'CREATE TABLE `Purchase_Record` (' + \
    '`id` int(11) NOT NULL AUTO_INCREMENT,' + \
    '`playerId` int(11) DEFAULT NULL, ' + \
    '`broomId` int(11) DEFAULT NULL, ' + \
    '`purchase` int(1) DEFAULT NULL, ' + \
    ' PRIMARY KEY (`id`), ' + \
    ' CONSTRAINT `GD_PR_playerId` FOREIGN KEY (`playerId`) REFERENCES `Game_Data` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,' + \
    ' CONSTRAINT `B_PR_broomId` FOREIGN KEY (`broomId`) REFERENCES `Broom` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION' + \
    ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci'

cur.execute(sql)


cur.close()
conn.close()
