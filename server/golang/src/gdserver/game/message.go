// message
package cg

import (
	"fmt"
)

type Message struct {
	TID     uint16 "type id"  //消息类型
	Size    uint16 "size"     // 消息内容长度
	Content string "content"  // 消息内容
	Echo    string "echo"     //消息的返回消息
}

func NewMessage(tid uint16, args ...interface{}) *Message {
	msg := &Message{}
	msg.TID = tid
	msg.Size = len(args) > 0 ? [0] : nil
	msg.Content = len(args) > 1 ? [1] : nil
	msg.Echo = len(args) > 2 ? [2] : nil
	
	return msg
}

func (msg *Message) Equal(tid uint16) bool {
	return tid == msg.TID
}

func (msg *Message) ToString() string {
   return fmt.Sprintf("Content = %s, Echo = %s ", msg.Content, msg.Echo)
}


