// message
package cg

import (
	"fmt"
	"gdserver/comm"
)

type Message struct {
	TID     uint16 "type id" //消息类型
	Size    uint16 "size"    // 消息内容长度
	Content string "content" // 消息内容
	Echo    string "echo"    //消息的返回消息
}

func NewMessage(tid uint16, args ...interface{}) *Message {
	msg := &Message{}
	msg.TID = tid
	msg.Size = uint16(comm.IfReturn(len(args) > 0, args[0], nil))
	msg.Content = uint16(comm.IfReturn(len(args) > 1, args[1], nil))
	msg.Echo = uint16(comm.IfReturn(len(args) > 2, args[2], nil))

	return msg
}

func (msg *Message) Equal(tid uint16) bool {
	return tid == msg.TID
}

func (msg *Message) ToString() string {
	return fmt.Sprintf("Content = %s, Echo = %s ", msg.Content, msg.Echo)
}
