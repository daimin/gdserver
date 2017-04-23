// cryto
package comm

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	_ "errors"
	_ "fmt"
)

type AesEncrypt struct {
}

var aesEncryptObj *AesEncrypt

func PKCS5Padding(ciphertext []byte, blockSize int) []byte {
	padding := blockSize - len(ciphertext)%blockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(ciphertext, padtext...)
}

func PKCS5UnPadding(origData []byte) []byte {
	length := len(origData)
	if length == 0 {
		return origData
	}
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
	blockMode := cipher.NewCBCEncrypter(block, make([]byte, block.BlockSize()))
	crypted := make([]byte, len(origData))
	// 根据CryptBlocks方法的说明，如下方式初始化crypted也可以
	// crypted := origData
	blockMode.CryptBlocks(crypted, origData)
	return base64.StdEncoding.EncodeToString(crypted), nil
}

//解密字符串
func (this *AesEncrypt) Decrypt(srcStr string) (strDesc string, err error) {

	crypted, err := base64.StdEncoding.DecodeString(srcStr)
	CheckErr(err)
	key := this.getKey()
	block, err := aes.NewCipher(key)
	if err != nil {
		return "", err
	}

	blockMode := cipher.NewCBCDecrypter(block, make([]byte, block.BlockSize()))
	origData := make([]byte, len(crypted))
	blockMode.CryptBlocks(origData, crypted)
	origData = PKCS5UnPadding(origData)
	return string(origData), nil
}

func GetAesEncrypt() *AesEncrypt {
	if aesEncryptObj == nil {
		aesEncryptObj = &AesEncrypt{}
	}
	return aesEncryptObj
}
