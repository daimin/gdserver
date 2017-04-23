// net
package sc

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"gdserver/comm"
	"io"
	"net"
	_ "os"
)

type Server struct {
	clients []*Client
	host    string
	port    int
	logger  *comm.LogHandler
}

func (this *Server) Listen() {
	listen, err := net.ListenTCP("tcp", &net.TCPAddr{net.ParseIP(this.host), this.port, ""})
	comm.CheckErr(err)
	if err != nil {
		fmt.Println("监听端口失败:", err.Error())
		return
	}

	fmt.Println("已初始化连接，等待客户端连接...")

	this.ServeForever(listen)
}

func (this *Server) read(conn *net.TCPConn, size int) ([]byte, bool) {
	buf := make([]byte, size)
	len_, err := conn.Read(buf)
	if err != nil {
		if err == io.EOF {
			fmt.Println("客户断开连接:", err.Error())
			return nil, false
		}
		fmt.Println("读取客户端数据错误:", err.Error())
		return nil, false
	}

	if len_ != size {
		fmt.Println("数据长度读取错误:", err.Error())
		return nil, false
	}

	return buf, true
}

//获取包头部
func (this *Server) getHead(conn *net.TCPConn) (uint16, bool) {
	readData, ret := this.read(conn, 2)
	if ret == false {
		return 0, ret
	}
	buf := bytes.NewReader(readData)
	var type_ uint16
	err := binary.Read(buf, binary.BigEndian, &type_)
	comm.CheckErr(err)
	return type_, ret
}

func (this *Server) ServeForever(listen *net.TCPListener) {
	defer listen.Close()
	for {
		conn, err := listen.AcceptTCP()
		if err != nil {
			this.logger.LogErr(fmt.Sprintf("接受客户端连接异常:%s", err.Error()))
			continue
		}
		this.logger.LogMsg(fmt.Sprintf("客户端连接来自:", conn.RemoteAddr().String()))
		defer conn.Close()
		session := make(chan string, 0)
		this.clients = append(this.clients, &Client{session, conn})
		go func(sess chan string) {
			for {

				type_, ret1 := this.getHead(conn)
				if !ret1 {
					break
				}

				this.logger.LogMsg(fmt.Sprintf("Protocol type = %d", type_))

				dataSize, ret2 := this.getHead(conn)
				if !ret2 {
					break
				}
				this.logger.LogMsg(fmt.Sprintf("Content size = %d", dataSize))
				cont, ret3 := this.read(conn, int(dataSize))
				if !ret3 {
					break
				}
				this.logger.LogMsg(fmt.Sprintf("Content = %s", cont))
				decryptCont, err := comm.GetAesEncrypt().Decrypt(string(cont))
				comm.CheckErr(err)
				fmt.Println(string(decryptCont))
				msg, _ := json.Marshal(NewMessage(type_, dataSize, string(decryptCont)))
				sess <- string(msg)
			}

		}(session)
	}
}
