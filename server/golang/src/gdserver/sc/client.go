package sc

import (
	_ "encoding/json"
	"net"
)

type Client struct {
	sess chan string
	conn *net.TCPConn
}

func NewClient(sess chan string, conn *net.TCPConn) *Client {
	return &Client{sess, conn}
}
