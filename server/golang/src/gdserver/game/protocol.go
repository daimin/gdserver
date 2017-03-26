// protocol
package cg

var DEFAULT *Message = NewMessage(0x0000)
var VERSION *Message = NewMessage(0x0001)
var HEARTBEAT *Message = NewMessage(0x0002)
var LOGIN *Message = NewMessage(0x0003)
var RANDOM_CHAT *Message = NewMessage(0x0004)
var FIND_CHAT *Message = NewMessage(0x0005)
var SEND_CONT *Message = NewMessage(0x0006)
var RECV_CONT *Message = NewMessage(0x0007)
var OVER_CHAT *Message = NewMessage(0x0008)
var LOGOUT *Message = NewMessage(0x0009)
var OK *Message = DEFAULT

// 大于等于0x8000用于错误表示
var ERR_NONE *Message = NewMessage(0x8000)
var ERR_VERSION *Message = NewMessage(0x8001, 0, "错误的版本")
var ERR_NOT_LOGIN *Message = NewMessage(0x8002, 0, "你还没有登录")
var ERR_LOGIN_FAIL *Message = NewMessage(0x8003, 0, "登录失败")
var ERR_RANDOM_FIND *Message = NewMessage(0x8004)
var ERR_FIND_CHAT *Message = NewMessage(0x8005)
var ERR_NO_SUPPORT *Message = NewMessage(0x8006, 0, "不支持的协议")
var ERR_SEND_CONT *Message = NewMessage(0x8007, 0, "发送消息失败")
