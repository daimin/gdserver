// comm
package comm

func CheckErr(err error) {
	if err != nil {
		panic(err)
	}
}
