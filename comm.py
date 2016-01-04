#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

__author__ = 'daimin'

import struct
import protocol
import message
import msgpack
import random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import conf
import copy
import hashlib
import logging

def pack_data(type_, data):
    data = str(data)
    data = msgpack_pack(aes_encode(conf.AES_KEY, data))
    return struct.pack("!HH", type_, len(data)) + data

def struct_unpack(data):
    return struct.unpack_from("!HH", data[:4])

def unpack_data(data):
        return aes_decode(conf.AES_KEY, msgpack_unpack(data))


def msgpack_pack(data):
    return msgpack.packb(data)


def msgpack_unpack(data):
    return msgpack.unpackb(data)

def aes_encode(key, data):
    obj = AES.new(key, AES.MODE_CBC, b'0000000000000000')
    length = 16
    count = len(data)
    if count < length:
        add = (length-count)
        #\0 backspace
        data = data + ('\0' * add)
    elif count > length:
        add = (length-(count % length))
        data = data + ('\0' * add)

    return b2a_hex(obj.encrypt(data))

def aes_decode(key, data):
    cryptor = AES.new(key, AES.MODE_CBC, b'0000000000000000')
    plain_text  = cryptor.decrypt(a2b_hex(data))
    return plain_text.rstrip('\0')

def create_nonce_str(length=16):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    str_ = ''
    for i in xrange(length):
        rpos = random.randint(0, len(chars) - 1)
        str_ = '%s%s' % (str_, chars[rpos : rpos + 1])
    return str_

def get_protocols():
    protos = {}
    lis = dir(protocol)
    for li in lis:
        m = getattr(protocol, li)
        if isinstance(m, message.Message):
            m.label = li
            protos[m.type_] = m

    return protos


def copy_protocol(name):
    m = getattr(protocol, name)
    if isinstance(m, message.Message):
        return copy.deepcopy(m)
    return None


def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def md5(src, t='lower'):
    src = "{}-{}".format(conf.MD5_SALT, src)
    if t is 'lower':
        return hashlib.md5(src).hexdigest().lower()
    else:
        return hashlib.md5(src).hexdigest().upper()

verbose = 0

def print_exception(e):
    global verbose
    logging.error(e)
    if verbose > 0:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    etext = aes_encode(conf.AES_KEY, """密码学中又称Rijndael加密法，是美国联邦政府采用的一种区块加密标准。这个标准用来替代原先的DES，已经被多方分析且广为全世界所使用。经过五年的甄选流程，高级加密标准由美国国家标准与技术研究院（NIST）于2001年11月26日发布于FIPS PUB 197，并在2002年5月26日成为有效的标准。2006年，高级加密标准已然成为对称密钥加密中最流行的算法之一。
    AES只是个基本算法，实现AES有若干模式。其中的CBC模式因为其安全性而被TLS（就
    是https的加密标准）和IPSec（win采用的）作为技术标准。简单地说，CBC使用密码和salt
    （起扰乱作用）按固定算法（md5）产生key和iv。然后用key和iv（初始向量'""")
    
    print(etext)
    print(aes_decode(conf.AES_KEY, etext))