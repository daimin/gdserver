#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'

from message import Message


C2S_VERSION         = Message(0x0001)
S2C_VERSION         = Message(0x1001)
C2S_HEARTBEAT       = Message(0x0002)
S2C_HEARTBEAT       = Message(0x1002)
C2S_LOGIN           = Message(0x0003)
S2C_LOGIN           = Message(0x1003)
C2S_RANDOM_CHAT     = Message(0x0004)
S2C_RANDOM_CHAT     = Message(0x1004)
C2S_FIND_CHAT       = Message(0x0005)
S2C_FIND_CHAT       = Message(0x1005)
C2S_SEND_CONT       = Message(0x0006)
S2C_SEND_CONT       = Message(0x1006)
C2S_RECV_CONT       = Message(0x0007)
S2C_RECV_CONT       = Message(0x1007)
C2S_OVER_CHAT       = Message(0x0008)
S2C_OVER_CHAT       = Message(0x1008)
C2S_LOGOUT          = Message(0x0009)
S2C_LOGOUT          = Message(0x1009)

# 大于等于0x8000用于错误表示
ERR_NONE            = Message(0x8000)
ERR_VERSION         = Message(0x8001, data='错误的版本')
ERR_LOGIN           = Message(0x8002)
ERR_RANDOM_FIND     = Message(0x8003)
ERR_FIND_CHAT       = Message(0x8004)
ERR_NO_SUPPORT      = Message(0x8005, label='ERR_NO_SUPPORT', data=u'不支持的协议')






