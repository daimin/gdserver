#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement
import server_gevt
import comm
import conf
import daemon
import protocol
import time
import json
import user

__author__ = 'daimin'


class ChatServer(server_gevt.JBServer):

    _handlers = {}

    def __init__(self):
        super(ChatServer, self).__init__()
        self.protos = comm.get_protocols()

    def register_handlers(self, sock):
        self._handlers[protocol.DEFAULT] = Handler(self, sock)
        self._handlers[protocol.VERSION] = VersionHandler(self, sock)
        self._handlers[protocol.HEARTBEAT] = HeartbeatHandler(self, sock)
        self._handlers[protocol.LOGIN] = LoginHandler(self, sock)
        self._handlers[protocol.SEND_CONT] = SendContHandler(self, sock)

    def send_message(self, sock, msg):
        super(ChatServer, self).do_send_message(sock, msg.type_, msg.data, msg.echo)

    def on_message(self, sock, type_, message):
        message = message.strip()
        handler = self._handlers.get(type_, self._handlers[protocol.DEFAULT])
        handler.request(message)


class Handler(object):
    
    _instances = {}

    def __init__(self, server, sock):
        self._server = ChatServer()
        self._sock = sock
        self._proto = protocol.DEFAULT

    def send_message(self, message):
        self._server.do_send_message(self._sock, message)

    def request(self, message):
        pass

    def _obtain_s2c_msg(type_, val, echo=None):
        s2c_msg = protocol.get_S2C_proto(message.type_)
        s2c_msg.set_data(val)
        if echo is not None:
            s2c_msg.set_echo(echo)
        return s2c_msg

    @staticmethod
    def get_instance(server, sock):
        if sock not in Handler._instances:
            Handler._instances[sock]  = Handler(server, sock)
        return Handler._instances[sock]


class VersionHandler(Handler):

    def request(self, message):
        if message.data == conf.VERSION:
            return self.send_message(protocol.OK)    # 发送处理OK
        else:
            return self.send_message(protocol.ERR_VERSION) #发送错误的版本



class HeartbeatHandler(Handler):
    def request(self, message):
        return self.send_message(self._obtain_s2c_msg(message.type_, int(time.time())))


class LoginHandler(Handler):
    def request(self, message):
        uobj = json.loads(message)
        if uobj:
            u = user.User(**uobj)
            ret = u.save()
            return self.send_message(self._obtain_s2c_msg(message.type_, ret))

        return self.send_message(protocol.ERR_LOGIN)   #发送登录错误

class SendContHandler(Handler):
    def request(self, message):
        self.send_message("Me: " + message + "From: " + str(self._sock.getpeername()) + " ==> " + message)

if __name__ == '__main__':
    
    config = {'daemon': 'start', 'pid-file': '/tmp/chat-server.pid', 'log-file':'log.log', 'user': 'daimin'}
    if conf.DAEMON:
        daemon.daemon_exec(config)
        daemon.set_user(config.get('user', None))
    ChatServer().runserver(config.get('host', '0.0.0.0'), config.get('port', 5005))

