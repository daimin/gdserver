// main
package main

import (
	"bufio"
	"fmt"
	"gdserver/comm"
	"gdserver/sc"
	"os"
	"strconv"
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
	fmt.Println("Start Game Server ... ")
	Help(nil)
	r := bufio.NewReader(os.Stdin)
	b, _, _ := r.ReadLine()
	line := string(b)

	host := comm.LoadConfig().ServerConfig.Host
	port := comm.LoadConfig().ServerConfig.Port
	args := strings.Split(line, " ")
	if len(args) > 1 {
		host = args[0]
		port, _ = strconv.Atoi(args[1])
	} else if len(args) == 1 {
		host = args[0]
	}
	//	lastId := db.Insert("INSERT INTO userinfo(username, departname, created) values(?,?,?)", "min", "技术部", "2015-07-21")
	//	fmt.Printf("last id = %d\n", lastId)
	sc.Listen(host, port)

}
