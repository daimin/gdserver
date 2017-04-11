// conf
package conf

type Database struct {
	Type   string
	Host   string
	Port   int
	DbName string
	User   string
	Pwd    string
}

type Server struct {
	Host     string
	Port     int
	CrytoKey string
}

type Conf struct {
	Dbconfig     *Database
	ServerConfig *Server
}
