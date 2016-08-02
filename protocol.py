# coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'

from message import Message
import copy
import sys

DEFAULT         = Message(0x0000)
VERSION         = Message(0x0001)
S2C_VERSION     = Message(0x1001)
HEARTBEAT       = Message(0x0002)
LOGIN           = Message(0x0003)
RANDOM_CHAT     = Message(0x0004)
FIND_CHAT       = Message(0x0005)
SEND_CONT       = Message(0x0006)
RECV_CONT       = Message(0x0007)
OVER_CHAT       = Message(0x0008)
LOGOUT          = Message(0x0009)

# 大于等于0x8000用于错误表示
ERR_NONE            = Message(0x8000)
ERR_VERSION         = Message(0x8001, data='错误的版本')
ERR_LOGIN           = Message(0x8002)
ERR_RANDOM_FIND     = Message(0x8003)
ERR_FIND_CHAT       = Message(0x8004)
ERR_NO_SUPPORT      = Message(0x8005, label='ERR_NO_SUPPORT', data=u'不支持的协议')


def get_protocol(name):
    m = getattr(sys.modules['__main__'], name)
    if isinstance(m, Message):
        return copy.deepcopy(m)
    return None



