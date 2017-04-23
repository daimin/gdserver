// loginsev
package game

import (
	_ "fmt"
	"gdserver/comm"
	"gdserver/sc"
)

type LoginSev struct {
	sc.Server
}

func NewLoginSev(host string, port int) *Server {
	clients := make([]*Client, 0)
	logger := &comm.LogHandler{"login"}
	return &LoginSev{clients, host, port, logger}
}
