# coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement

import gdserver.message as msg
import protocol
from gdserver import user
from gdserver.handler import Handler


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
            # 开始查找
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
