package db

import (
	"database/sql"
	_ "fmt"

	"gdserver/comm"

	_ "github.com/mattn/go-sqlite3" //【import _ 包路径】只是引用该包，仅仅是为了调用init()函数，所以无法通过包名来调用包中的其他函数。
)

var conn *sql.DB = nil

func Conn() *sql.DB {
	if conn == nil {
		var err error
		conn, err = sql.Open("sqlite3", "./foo.s3db")
		comm.CheckErr(err)
	}

	return conn
}

func init() { //init函数初始化该模块
	Conn()
}

func Close() {
	if conn != nil {
		conn.Close()
	}
}

func Insert(fmtsql string, args ...interface{}) int64 {
	stmt, err := conn.Prepare(fmtsql)
	comm.CheckErr(err)
	ret, err := stmt.Exec(args...)

	comm.CheckErr(err)
	id, err := ret.LastInsertId()
	comm.CheckErr(err)
	return id
}

func Update(fmtsql string, args ...interface{}) int64 {
	stmt, err := conn.Prepare(fmtsql)
	comm.CheckErr(err)
	ret, err := stmt.Exec(args...)

	comm.CheckErr(err)
	id, err := ret.LastInsertId()
	comm.CheckErr(err)
	return id
}
