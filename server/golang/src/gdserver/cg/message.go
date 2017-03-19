// message
package cg

import (
	"fmt"
)

type Message struct {
	From    string "from"
	To      string "to"
	Content string "content"
}

func main() {
	fmt.Println("Hello World!")
}
