// net
package sc

import (
	"bytes"
	_ "bytes"
	"encoding/binary"
	"fmt"
	"gdserver/comm"
	"io"
	"net"
	_ "os"
)

func Listen(host string, port int) {
	listen, err := net.ListenTCP("tcp", &net.TCPAddr{net.ParseIP(host), port, ""})
	comm.CheckErr(err)
	if err != nil {
		fmt.Println("监听端口失败:", err.Error())
		return
	}

	fmt.Println("已初始化连接，等待客户端连接...")

	NetServer(listen)
}

func read(conn *net.TCPConn, size int) ([]byte, bool) {
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

func getHead(conn *net.TCPConn) (uint16, bool) {
	readData, ret := read(conn, 2)
	if ret == false {
		return 0, ret
	}
	buf := bytes.NewReader(readData)
	var type_ uint16
	err := binary.Read(buf, binary.BigEndian, &type_)
	comm.CheckErr(err)
	return type_, ret
}

func NetServer(listen *net.TCPListener) {
	defer listen.Close()
	for {
		conn, err := listen.AcceptTCP()
		if err != nil {
			fmt.Println("接受客户端连接异常:", err.Error())
			continue
		}
		fmt.Println("客户端连接来自:", conn.RemoteAddr().String())
		defer conn.Close()
		go func() {
			for {

				_, ret1 := getHead(conn)
				if !ret1 {
					break
				}
				dataSize, ret2 := getHead(conn)
				if !ret2 {
					break
				}

				cont, ret3 := read(conn, int(dataSize))
				if !ret3 {
					break
				}

				fmt.Println(string(cont))

			}

		}()
	}
}
