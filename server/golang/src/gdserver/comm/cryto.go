// cryto
package comm

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	_ "fmt"
)

type AesEncrypt struct {
}

func PKCS5Padding(ciphertext []byte, blockSize int) []byte {
	padding := blockSize - len(ciphertext)%blockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(ciphertext, padtext...)
}

func PKCS5UnPadding(origData []byte) []byte {
	length := len(origData)
	// 去掉最后一个字节 unpadding 次
	unpadding := int(origData[length-1])
	return origData[:(length - unpadding)]
}

func (this *AesEncrypt) getKey() []byte {
	strKey := LoadConfig().ServerConfig.CrytoKey
	keyLen := len(strKey)
	if keyLen < 16 {
		panic("res key 长度不能小于16")
	}
	arrKey := []byte(strKey)
	if keyLen >= 32 {
		//取前32个字节
		return arrKey[:32]
	}
	if keyLen >= 24 {
		//取前24个字节
		return arrKey[:24]
	}
	//取前16个字节
	return arrKey[:16]
}

//加密字符串
func (this *AesEncrypt) Encrypt(strMesg string) (string, error) {
	key := this.getKey()
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}
	origData := []byte(strMesg)
	origData = PKCS5Padding(origData, block.BlockSize())
	blockMode := cipher.NewCBCEncrypter(block, make([]byte, len(key)))
	crypted := make([]byte, len(origData))
	// 根据CryptBlocks方法的说明，如下方式初始化crypted也可以
	// crypted := origData
	blockMode.CryptBlocks(crypted, origData)
	return base64.StdEncoding.EncodeToString(crypted), nil
}

//解密字符串
func (this *AesEncrypt) Decrypt(src []byte) (strDesc string, err error) {

	crypted := make([]byte, len(src))

	size, err := base64.StdEncoding.Decode(crypted, src)
	CheckErr(err)
	if size == 0 {
		return "", nil
	}
	key := this.getKey()
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}
	blockMode := cipher.NewCBCDecrypter(block, make([]byte, len(key)))
	origData := make([]byte, len(crypted))
	blockMode.CryptBlocks(origData, crypted)
	origData = PKCS5UnPadding(origData)
	return string(origData), nil
}
