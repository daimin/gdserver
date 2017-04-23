// comm
package comm

import (
	"os"
	"path/filepath"
	"strings"

	"gdserver/conf"

	"strconv"

	"github.com/go-ini/ini"
)

var iniConf *conf.Conf = nil

func CheckErr(err error) {
	if err != nil {

		panic(err)
	}
}

func IfReturn(condition bool, trueVal, falseVal interface{}) interface{} {
	if condition {
		return trueVal
	}
	return falseVal
}

func getCurrentDirectory() string {
	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	CheckErr(err)
	return strings.Replace(dir, "\\", "/", -1)
}

func getValue(key *ini.Key, err error) string {
	CheckErr(err)
	return key.Value()
}

func atoI(val string) int {
	intval, err := strconv.Atoi(val)
	CheckErr(err)
	return intval
}

func LoadConfig() *conf.Conf {
	if iniConf != nil {
		return iniConf
	}
	rootPath := getCurrentDirectory()
	cfg, err := ini.InsensitiveLoad(rootPath + "/conf/conf.ini")
	CheckErr(err)
	inidbSection, err := cfg.GetSection("database")
	CheckErr(err)
	dbconf := &conf.Database{
		getValue(inidbSection.GetKey("TYPE")),
		getValue(inidbSection.GetKey("HOST")),
		atoI(getValue(inidbSection.GetKey("PORT"))),
		getValue(inidbSection.GetKey("DBNAME")),
		getValue(inidbSection.GetKey("USER")),
		getValue(inidbSection.GetKey("PWD"))}
	iniServerSection, err := cfg.GetSection("server")
	CheckErr(err)
	serverConf := &conf.Server{getValue(iniServerSection.GetKey("HOST")),
		atoI(getValue(iniServerSection.GetKey("PORT"))),
		getValue(iniServerSection.GetKey("CRYTO_KEY")),
		atoI(getValue(iniServerSection.GetKey("DEBUG"))) > 0}
	iniConf = &conf.Conf{dbconf, serverConf}
	return iniConf
}

/**
 * 判断文件是否存在  存在返回 true 不存在返回false
 */
func checkFileIsExist(filename string) bool {
	var exist = true
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		exist = false
	}
	return exist
}

//var cfg, err = ini.InsensitiveLoad("filename")
