#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

from chatserver.chat_handlers import *
from gdserver import  conf
from gdserver import daemon, server_gevt
from gdserver.handler import DefaultHandler, VersionHandler, HeartbeatHandler, LoginHandler

__author__ = 'daimin'


class ChatServer(server_gevt.JBServer):

    _handlers = {}
    app_dict = {"login_users": {}}   # 应用级别的数据, 预定义了一些数据

    def __init__(self):
        super(ChatServer, self).__init__()
        self._register_handlers()

    def _register_handlers(self):
        print("Register handlers")
        
        self._handlers[protocol.DEFAULT.TID] = DefaultHandler(self)
        self._handlers[protocol.VERSION.TID] = VersionHandler(self)
        self._handlers[protocol.HEARTBEAT.TID] = HeartbeatHandler(self)
        self._handlers[protocol.LOGIN.TID] = LoginHandler(self)
        self._handlers[protocol.SEND_CONT.TID] = SendContHandler(self)
        self._handlers[protocol.FIND_CHAT.TID] = FindChatHandler(self)

    def send_message(self, sock, msg_):
        if msg_.TID < protocol.ERR_NONE:
            super(ChatServer, self).do_send_message(sock, msg_.TID, msg_.data, msg_.echo)
        else:
            msg_.echo = msg_.data  #可能默认是填写的data变量
            super(ChatServer, self).do_send_message(sock, msg_.TID, None, msg_.echo)

    def on_message(self, sock, tid, message):
        message = message.strip()
        msg_obj = msg.Message(int(tid), data=message)
        handler = self._handlers.get(tid, self._handlers[protocol.DEFAULT.TID])
        handler.request(msg_obj, sock)

    def finalize(self, sock_data):
        for k, h in self._handlers.iteritems():
            h.finalize(sock_data)

if __name__ == '__main__':
    
    config = {'daemon': 'start', 'pid-file': '/tmp/chat-gdserver.pid', 'log-file':'log.log', 'user': 'daimin'}
    if conf.DAEMON:
        daemon.daemon_exec(config)
        daemon.set_user(config.get('user', None))
    ChatServer().runserver(config.get('host', '0.0.0.0'), config.get('port', 5005))

