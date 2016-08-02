#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'


class Message(object):
    type_ = 0
    len_ = 0
    data = ''
    self_data = ''
    label = ''

    def __init__(self, type_, **kwargs):
        self.type_ = type_
        self.data = kwargs.get('data', '')
        self.label = kwargs.get('label', '')

    def eq(self, type_):
        return type_ == self.type_

    def set_data(self, data, self_data=''):
        self.data = data
        self.self_data = self_data








