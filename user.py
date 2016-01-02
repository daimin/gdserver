#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'

import torndb
import conf

class User(object):
    tabname = 'c_user'

    id = ''
    name = ''
    passwd = ''
    sex = ''
    score = ''
    grade = ''
    phone = ''
    devid = ''
    country = ''
    city = ''

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', '')
        self.name = kwargs.get('name', '')
        self.passwd = kwargs.get('passwd', '')
        self.sex = kwargs.get('sex', 2) # 0 女，1 男，2未知
        self.score = kwargs.get('score', 0)
        self.grade = kwargs.get('grade', 1)
        self.phone = kwargs.get('phone', '')
        self.devid = kwargs.get('devid', '')
        self.country = kwargs.get('country', '')
        self.city = kwargs.get('city', '')
        self.ctime = kwargs.get('ctime', '')
        self.utime = kwargs.get('utime', '')
        self.ltime = kwargs.get('ltime', '')
        self.state = kwargs.get('state', 1)


        self._conn  = torndb.Connection(
                             host = "%s:%d" (conf.MYSQL_CONFIG['host'], conf.MYSQL_CONFIG['port']),
                             database = conf.MYSQL_CONFIG['db'],
                             user = conf.MYSQL_CONFIG['user'],
                             password = conf.MYSQL_CONFIG['passwd'],
            )

    def add(self):
        
        self.id = self._conn.insert("INSERT INTO `%s`(`name`, `passwd`, `sex`, `score`, `grade`, `phone`, `devid`,\
         `country`, `city`, `ctime`, `utime`, `ltime`, `state`) VALUES('%s', '%s', '%s', '%s', '%s', '%s',\
          '%s', '%s', '%s', '%s', '%s', '%s', '%')" % (self.tabname, self.name, self.passwd, self.sex,\
           self.score, self.grade, self.phone, self.devid, self.country, self.city, self.ctime, self.utime,\
           self.ltime, self.state))
        return self.id

    def update(self):
        return self._conn.update("UPDATE  `%s` SET `name`='%s', `passwd`='%s', `sex`='%s', `score`='%s', `grade`='%s',\
         `phone`='%s', `devid`='%s', `country`='%s', `city`='%s', `ctime`='%s', `utime`='%s', `ltime`='%s', `state`='%s'\
          WHERE `id`='%s'" % (self.tabname, self.name, self.passwd, self.sex,\
           self.score, self.grade, self.phone, self.devid, self.country, self.city, self.ctime, self.utime,\
           self.ltime, self.state, self.id))

    def get(self, id):
        





