#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'


class Message(object):
    TID =''       #消息的type ID
    len_ = 0      #消息内容的长度
    data = ''     #消息的内容
    echo = ''     #回传给发送客户的消息

    def __init__(self, tid, **kwargs):
        self.TID = tid 
        self.data  = kwargs.get('data', '')
        self.echo = kwargs.get('echo', '')

    def eq(self, tid):
        return tid == self.TID

    def set_data(self, data):
        self.data = data

    def set_echo(self, echo):
        self.echo = echo

    def __str__(self):
        return self.data








