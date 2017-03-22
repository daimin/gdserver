// protocol
package cg

DEFAULT         = NewMessage(0x0000)
VERSION         = NewMessage(0x0001)
HEARTBEAT       = NewMessage(0x0002)
LOGIN           = NewMessage(0x0003)
RANDOM_CHAT     = NewMessage(0x0004)
FIND_CHAT       = NewMessage(0x0005)
SEND_CONT       = NewMessage(0x0006)
RECV_CONT       = NewMessage(0x0007)
OVER_CHAT       = NewMessage(0x0008)
LOGOUT          = NewMessage(0x0009)
OK              = DEFAULT

// 大于等于0x8000用于错误表示
ERR_NONE            = NewMessage(0x8000)
ERR_VERSION         = NewMessage(0x8001, data=u'错误的版本')
ERR_NOT_LOGIN       = NewMessage(0x8002, data=u'你还没有登录')
ERR_LOGIN_FAIL      = NewMessage(0x8003, data=u'登录失败')
ERR_RANDOM_FIND     = NewMessage(0x8004)
ERR_FIND_CHAT       = NewMessage(0x8005)
ERR_NO_SUPPORT      = NewMessage(0x8006, data=u'不支持的协议')
ERR_SEND_CONT       = NewMessage(0x8007, data=u'发送消息失败')