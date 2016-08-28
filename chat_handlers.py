# coding:utf-8
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

    def check_logined(self):
        login_user = self._sock.get_data('login_user')
        if login_user is None:
            return self.send_message(self._obtain_err_msg(protocol.ERR_NOT_LOGIN, '用户还未登录')), False
        return login_user, True

    @staticmethod
    def _obtain_s2c_msg(tid, data=None, echo=None):
        """获取服务器发送给客户端消息
        """
        s2c_msg = protocol.get_S2C_proto(tid)
        s2c_msg.set_data(data)
        s2c_msg.set_echo(echo)
        return s2c_msg

    @staticmethod
    def _obtain_err_msg(errmsg, val):
        """获取服务器发送给客户端错误消息
        """
        err_msg = msg.Message(errmsg.TID, data=None, echo=val)
        return err_msg

    def finalize(self, sock_data):
        pass


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

    def record_loginuser(self, muser):
        self._server.app_dict['login_users'][muser.name] = muser

    def check_islogin_in_other_client(self, uname):
        return self._server.app_dict['login_users'].get(uname, False)

    def request(self, message, sock):
        super(LoginHandler, self).request(message, sock)
        uobj = json.loads(message.data)

        if uobj:
            try:
                uobj['name'] = uobj['name'].strip()
                uobj['passwd'] = uobj['passwd'].strip()
                # 先检查当前用户是否已经登录
                if self.check_islogin_in_other_client(uobj['name']):
                    return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo='当前用户已经在其它客户端登录'))

                if uobj['name'] == '' or uobj['passwd'] == '':
                    return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo='用户名或密码为空'))

                ouser = user.User.find_user_by_name(uobj['name'])
                if ouser.passwd != uobj['passwd']:
                    return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo='密码错误'))

                if not ouser:
                    ouser = user.User(**uobj)
                    ouser.save()
                ouser.sid = sock.sid
                sock.set_data('login_user', ouser)
                self.record_loginuser(ouser)
                return self.send_message(self._obtain_s2c_msg(message.TID, data=None, echo=uobj['name']))
            except Exception, oe:
                return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo=str(oe)))

        return self.send_message(msg.Message(protocol.ERR_LOGIN_FAIL.TID, echo=str(uobj) + ",登录失败"))  # 发送登录错误

    def finalize(self, sock_data):
        loguser = sock_data.get_data('login_user')
        if loguser.name in self._server.app_dict['login_users']:
            print("Finalize socket login data")
            del self._server.app_dict['login_users'][loguser.name]


class SendContHandler(Handler):
    def request(self, message, sock):
        super(SendContHandler, self).request(message, sock)
        login_user, ret = self.check_logined()
        if ret:
            if not sock.teams:
                return self.send_message(msg.Message(protocol.ERR_SEND_CONT.TID, echo="不存在聊天对象"))  # 发送登录错误
            return self.send_message(self._obtain_s2c_msg(message.TID,
                                                          " ==> %s \tFrom: 【%s】" % (message.data, login_user.name),
                                                                  " Me: %s" % message.data))


class FindChatHandler(Handler):
    def request(self, message, sock):
        super(FindChatHandler, self).request(message, sock)
        login_user, ret = self.check_logined()
        if ret:
            #开始查找
            myname = login_user.name
            findname = message.data
            if myname == findname:
                return self.send_message(msg.Message(protocol.ERR_FIND_CHAT.TID, echo="不能和自己聊天"))  # 发送登录错误

            for uname, ouser in self._server.app_dict['login_users'].iteritems():
                if findname == uname:
                    if ouser.action == user.User.CHATTING_ACTION:
                        return self.send_message(msg.Message(protocol.ERR_FIND_CHAT.TID, echo="查找客户正在聊天"))  # 发送登录错误

                    pair_sock = self._server.client_dict.get(ouser.sid, None)
                    if pair_sock is None:
                        return self.send_message(msg.Message(protocol.ERR_FIND_CHAT.TID, echo="查找用户不存在"))  # 发送登录错误
                    if pair_sock not in sock.teams:
                        sock.teams.append(pair_sock)

                    self._server.app_dict['login_users'][uname].action = user.User.CHATTING_ACTION
                    self._server.app_dict['login_users'][myname].action = user.User.CHATTING_ACTION

                    return self.send_message(self._obtain_s2c_msg(message.TID, data=findname, echo=findname))

            return self.send_message(msg.Message(protocol.ERR_FIND_CHAT.TID, echo="查找用户不存在"))  # 发送登录错误
