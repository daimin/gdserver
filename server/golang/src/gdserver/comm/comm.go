// comm
package comm

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
