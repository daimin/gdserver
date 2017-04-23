// protocol
package game

import (
	"gdserver/sc"
)

var DEFAULT *sc.Message = sc.NewMessage(0x0000)
var VERSION *sc.Message = sc.NewMessage(0x0001)
var HEARTBEAT *sc.Message = sc.NewMessage(0x0002)
var LOGIN *sc.Message = NewMessage(0x0003)
var RANDOM_CHAT *sc.Message = sc.NewMessage(0x0004)
var FIND_CHAT *sc.Message = sc.NewMessage(0x0005)
var SEND_CONT *sc.Message = sc.NewMessage(0x0006)
var RECV_CONT *sc.Message = sc.NewMessage(0x0007)
var OVER_CHAT *sc.Message = sc.NewMessage(0x0008)
var LOGOUT *sc.Message = sc.NewMessage(0x0009)
var OK *sc.Message = DEFAULT

// 大于等于0x8000用于错误表示
var ERR_NONE *sc.Message = sc.NewMessage(0x8000)
var ERR_VERSION *sc.Message = sc.NewMessage(0x8001, 0, "错误的版本")
var ERR_NOT_LOGIN *sc.Message = sc.NewMessage(0x8002, 0, "你还没有登录")
var ERR_LOGIN_FAIL *sc.Message = sc.NewMessage(0x8003, 0, "登录失败")
var ERR_RANDOM_FIND *sc.Message = sc.NewMessage(0x8004)
var ERR_FIND_CHAT *sc.Message = sc.NewMessage(0x8005)
var ERR_NO_SUPPORT *sc.Message = sc.NewMessage(0x8006, 0, "不支持的协议")
var ERR_SEND_CONT *sc.Message = sc.NewMessage(0x8007, 0, "发送消息失败")
