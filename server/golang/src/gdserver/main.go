// main
package main

import (
	"fmt"
	"gdserver/comm"
	"gdserver/sc"
	"strings"
)

func Help(args []string) int {
	fmt.Println("Commands:<host> <port>")
	return 0
}

/**
 * 这里返回的是一个map，map的键是string，值是函数
 */
func GetCommandHandlers() map[string]func(args []string) int {
	return map[string]func([]string) int{
		"help": Help,
		"h":    Help,
	}
}

func main() {
	host := strings.TrimSpace(comm.LoadConfig().ServerConfig.Host)
	port := comm.LoadConfig().ServerConfig.Port

	fmt.Println(fmt.Sprintf("Start Game Server in [%s:%d] ... ", host, port))

	//	lastId := db.Insert("INSERT INTO userinfo(username, departname, created) values(?,?,?)", "min", "技术部", "2015-07-21")
	//	fmt.Printf("last id = %d\n", lastId)
	sc.Listen(host, port)
	//	enstr, _ := comm.GetAesEncrypt().Encrypt("1")
	//	fmt.Println(enstr)
	//	destr, _ := comm.GetAesEncrypt().Decrypt(enstr)
	//	fmt.Println(destr)

}
