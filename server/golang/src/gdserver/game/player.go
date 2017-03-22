// player
package cg

import (
	"fmt"
)

type Player struct {
	Id      int    "id"
	Name    string "name"
	Passwd  string "password"
	Sex     int    "sex"
	Score   int    "score"
	Level   int    "level"
	Tel     int    "telphone"
	Devid   string "device id"
	Country string "country"
	City    string "city"
	Room    int    "room"
	mq      chan *Message
}

func NewPlayer() *Player {
	m := make(chan *Message, 1024)
	player := &Player{"", 0, 0, 0, m}

	go func(p *Player) {
		for {
			msg := <-p.mq
			fmt.Println(p.Name, "received message:", msg.Content)
		}
	}(player)

	return player
}
