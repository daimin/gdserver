// main
package main

import (
	_ "fmt"
	_ "gdserver/db"
	"gdserver/sc"
)

func main() {
	//	lastId := db.Insert("INSERT INTO userinfo(username, departname, created) values(?,?,?)", "min", "技术部", "2015-07-21")
	//	fmt.Printf("last id = %d\n", lastId)
	sc.Listen("127.0.0.1", 14395)
}
