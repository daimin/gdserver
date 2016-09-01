#coding:utf-8
__author__ = 'daimin'

import socket
import sys

from gevent import monkey

monkey.patch_socket()
import gevent
import select
from gdserver import comm
from gdserver import protocol
import time
import json

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Address Family: 可以永AF_INET, AF_INET6(用于Internet通信，ipv4或者ipv6) 或者 AF_UNIX(用于本机进程通信)
    # Type: 套接字类型，可以是SOCKET_STREAM(流式套接字，用于TCP协议)或者SOCKET_DGRAM(数据报套接字，用于UDP协议)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error Message: ' + msg[1]
    sys.exit()


print 'Socket Created'


host = "127.0.0.1"
port = 5005

def you_input(s):
    while 1:
        x = raw_input('>')
        s.sendall(x)
        gevent.sleep(0)

def you_recv(s):
    while 1:
        if int(time.time()) % 10 == 0:
            protocol.C2S_HEARTBEAT.data = int(time.time())
            p = comm.copy_protocol('C2S_HEARTBEAT')
            p.set_data(int(time.time()))
            s.sendall(comm.pack_data(p.type_, p.data))
        print '------------'

        r, w, x = select.select([s, sys.stdin], [], [])
        for rr in r:
            if rr is s:
                header_reply = rr.recv(4)
                if header_reply:
                    type_, len_ = comm.struct_unpack(header_reply)
                    content_reply = rr.recv(len_)
                    content_reply = comm.unpack_data(content_reply)
                    print type_
                    print protocol.S2C_VERSION.type_
                    if protocol.S2C_VERSION.eq(type_):
                        print 'Version right!!'
                    elif protocol.ERR_VERSION.eq(type_):
                        print 'Version wrong!!'
                    elif protocol.S2C_HEARTBEAT.eq(type_):
                        print 'heartbeating ...'
                    elif protocol.S2C_LOGIN.eq(type_):
                        print 'S2C_LOGIN ...'


                    # print "type = %s, content=%s" % (type_, content_reply)
                
            else:
                msg = rr.readline()
                protocol.C2S_VERSION.data = '0.0.1'
                p = comm.copy_protocol('C2S_LOGIN')
                p.set_data(json.dumps({'name': 'daimin2', 'passwd': '123'}))
                s.sendall(comm.pack_data(p.type_, p.data))
        gevent.sleep(0)

try:
    remote_ip = socket.gethostbyname(host)
    s.connect((remote_ip, port))
    s.setblocking(0)
    # s.sendall('GET / HTTP/1.1\r\n\r\n')  # sendall会发送所有的string，而send可能只会发送部分，可以根据返回发送字节数做处理
    print '-----------------------------------------------------'
    gevent.joinall([
        # gevent.spawn(you_raw_input, s),
        gevent.spawn(you_recv, s)
        ])
        
except socket.gaierror:   # gaierror地址相关的错误
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip
