// log
package comm

import (
	"fmt"
	"log"
	"os"
	"time"
)

type LogHandler struct {
	name      string
	msgLogger *log.Logger
	errLogger *log.Logger
}

func NewLogHandler(name string) *LogHandler {
	_msglogger := log.New(createlLogFile(name, "msg"), "", log.LstdFlags|log.Llongfile)
	_errlogger := log.New(createlLogFile(name, "err"), "", log.LstdFlags|log.Llongfile)
	return &LogHandler{name, _msglogger, _errlogger}
}

func createlLogFile(name string, type_ string) *os.File {
	var file *os.File = nil
	var err error
	filepath := fmt.Sprintf("%s/logs/%s-%s.%s.log", name, type_, getCurrentDirectory(), time.Now().Format("2006010215"))

	if checkFileIsExist(filepath) {
		file, err = os.OpenFile(filepath, os.O_APPEND, 0666) //打开文件
		CheckErr(err)
	} else {
		file, err = os.Create(filepath)
		CheckErr(err)
	}
	return file
}

func (this *LogHandler) LogMsg(message string) {
	if LoadConfig().ServerConfig.Debug {
		fmt.Println(message)
	}
	this.msgLogger.Println(message)
}

func (this *LogHandler) LogErr(message string) {
	if LoadConfig().ServerConfig.Debug {
		fmt.Println(message)
	}

	this.errLogger.Println(message)
}
