// net
package sc

import (
	_ "bytes"
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
			buf := make([]byte, 128)
			for {
				len_, err := conn.Read(buf)
				if err != nil {
					if err == io.EOF {
						fmt.Println("客户断开连接:", err.Error())
						break
					}
					fmt.Println("读取客户端数据错误:", err.Error())
					break
				}

				indata := string(buf[0:len_])
				fmt.Println("客户端发来数据:", indata)
				if indata == "q" {
					fmt.Println("客户端主动断开连接")
					conn.Close()
					break
				}

				conn.Write([]byte{'f', 'i', 'n', 'i', 's', 'h'})
			}

		}()
	}
}
