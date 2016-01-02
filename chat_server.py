#coding:utf-8

from __future__ import absolute_import, division, print_function, \
    with_statement
__author__ = 'daimin'

import server_gevt
import comm
import protocol
import conf
import daemon
import time


class ChatServer(server_gevt.JBServer):

    def __init__(self):
        super(ChatServer, self).__init__()
        self.protos = comm.get_protocols()

    def send_message(self, sock, msg):
        super(ChatServer, self).send_message(sock, msg.type_, msg.data)
    
    def on_message(self, sock, type_, message):
        hander = ChatHandler.get_instance(self, sock)
        message = message.strip()
        getattr(hander, 'handle_%s' % self.protos.get(type_, 'ERR_NO_SUPPORT').label)(message)


class ChatHandler(object):
    
    _instances = {}

    def __init__(self, server, sock):
        self._sock = sock
        self._server = server

    def send_message(self, message):
        self._server.send_message(self._sock, message)

    @staticmethod
    def get_instance(server, sock):
        if sock not in ChatHandler._instances:
            ChatHandler._instances[sock]  = ChatHandler(server, sock)
        return ChatHandler._instances[sock]

    def handle_ERR_NO_SUPPORT(self, type_, message):
        self.send_message(comm.copy_protocol('ERR_NO_SUPPORT'))

    def handle_C2S_VERSION(self, message):
        print('handle_C2S_VERSION=========' + message)
        if message == conf.VERSION:
            self.send_message(comm.copy_protocol('S2C_VERSION'))
        else:
            self.send_message(comm.copy_protocol('ERR_VERSION'))

    def handle_C2S_HEARTBEAT(self, message):
        print('handle_C2S_HEARTBEAT=========' + message)
        p = comm.copy_protocol('S2C_HEARTBEAT')
        p.set_data(int(time.time()))
        self.send_message(p)




if __name__ == '__main__':
    
    config = {'daemon': 'start', 'pid-file': '/tmp/chat-server.pid', 'log-file':'log.log', 'user': 'daimin'}

    daemon.daemon_exec(config)
    daemon.set_user(config.get('user', None))
    ChatServer().runserver(config.get('host', '0.0.0.0'), config.get('port', 5005))

