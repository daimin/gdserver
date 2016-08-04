#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'


class Message(object):
    type_=''
    len_ = 0
    data = ''
    echo = ''
    label = ''

    def __init__(self, type_, **kwargs):
        self.type_= type_ 
        self.data  = kwargs.get('data', '')
        self.echo = kwargs.get('echo', '')
        self.label = kwargs.get('label', '')

    def eq(self, type_):
        return type_ == self.type_

    def set_data(self, data):
        self.data = data

    def set_echo(self, echo):
        self.echo = echo  








