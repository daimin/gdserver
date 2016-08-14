#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

import json
import protocol
import message as msg
import conf
import user
import time


class Handler(object):
    _instances = {}

    def __init__(self, server):
        self._server = server
        self._sock = None

    def send_message(self, message):
        self._server.send_message(self._sock, message)

    def request(self, message, sock):
        self._sock = sock

    @staticmethod
    def _obtain_s2c_msg(tid, val, echo=None):
        """获取服务器发送给客户端消息
        """
        s2c_msg = protocol.get_S2C_proto(tid)
        s2c_msg.set_data(val)
        if echo is not None:
            s2c_msg.set_echo(echo)
        return s2c_msg

    @staticmethod
    def _obtain_err_msg(errmsg, val):
        """获取服务器发送给客户端错误消息
        """
        err_msg = msg.Message(errmsg.TID, data=None, echo=val)
        return err_msg


class DefaultHandler(Handler):
    def request(self, message, sock):
        super(DefaultHandler, self).request(message, sock)
        return self.send_message(protocol.DEFAULT)


class VersionHandler(Handler):
    def request(self, message, sock):
        super(VersionHandler, self).request(message, sock)
        if message.data == conf.VERSION:
            return self.send_message(protocol.OK)  # 发送处理OK
        else:
            return self.send_message(protocol.ERR_VERSION)  # 发送错误的版本


class HeartbeatHandler(Handler):
    def request(self, message, sock):
        super(HeartbeatHandler, self).request(message, sock)
        return self.send_message(self._obtain_s2c_msg(message.TID, int(time.time())))


class LoginHandler(Handler):
    def request(self, message, sock):
        super(LoginHandler, self).request(message, sock)
        uobj = json.loads(message.data)

        if uobj:
            try:
                uobj['name'] = uobj['name'].strip()
                uobj['passwd'] = uobj['passwd'].strip()

                if uobj['name'] == '' or uobj['passwd'] == '':
                    return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo='用户名或密码为空'))

                ouser = user.User.find_user_by_name(uobj['name'])
                if ouser.passwd != uobj['passwd']:
                    return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo='密码错误'))

                if not ouser:
                    ouser = user.User(**uobj)
                    ouser.save()

                sock.set_data('login_user', ouser)
                return self.send_message(self._obtain_s2c_msg(message.TID, 1))
            except Exception, oe:
                return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo=str(oe)))

        return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, data=unicode(uobj) + ",登录失败"))  # 发送登录错误


class SendContHandler(Handler):
    def request(self, message, sock):
        super(SendContHandler, self).request(message, sock)
        login_user = sock.get_data('login_user')
        if login_user is not None:
            return self.send_message(self._obtain_s2c_msg(message.TID,
                                                          " ==> %s From: %s" % (message.data, login_user.name),
                                                          " Me: %s" % message.data))
        else:
            return self.send_message(self._obtain_err_msg(protocol.ERR_NOT_LOGIN, '用户还未登录'))