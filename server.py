#coding:utf-8
__author__ = 'daimin'


import socket, select
import sys

conn_list = []
write_list = []
RECV_BUFFER = 4096
PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(10)

def broadcast_data(sock, message):
    global conn_list
    for socket_ in conn_list:
        if socket_ != server_socket and socket_ != sock:
            try:
                socket_.sendall(message)
            except:
                socket_.close()
                conn_list.remove(socket_)

conn_list.append(server_socket) # 这里其实可以开多个服务端的socket来处理客户端的请求

print "Chat server started on port " + str(PORT)

while 1:
    # 这里的参数分别表示监控读事件，写事件，异常事件的文件描述符(fd)，返回的是符合条件的文件描述符，也就是发生了相应事件的描述符
    read_sockets, write_sockets, error_sockets = select.select(conn_list, write_list , [])

    for sock in read_sockets:
        if sock == server_socket:
            sockfd, addr = server_socket.accept()
            conn_list.append(sockfd)
            write_list.append(sockfd)
            print 'Client (%s, %s) connected' % addr

            broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
        else:
            try:
                data = sock.recv(RECV_BUFFER)
                if data:
                    broadcast_data(sock, "\r<{}>{}".format(sock.getpeername(), data))
            except:
                broadcast_data(sock, "Client (%s, %s) was offline" % addr)
                print "Client (%s, %s) was offline" % addr
                sock.close()
                conn_list.remove(sock)
                continue

server_socket.close()
