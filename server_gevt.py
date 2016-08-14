# coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement
from gevent.server import StreamServer
import comm
import signal
import gevent

__author__ = 'daimin'


class JBServer(object):

    client_dict = {}

    def __init__(self):
        pass

    def on_message(self, sock, type_, message):
        pass

    def mainloop(self, socket_, address):
        """mainloop方法对应每个客户端都是一个协程
        """
        jb_sock = JBSocket(socket_, comm.tuple_as_md5(socket_.getpeername()))
        if jb_sock.sid not in JBServer.client_dict:
            self.client_dict[jb_sock.sid] = jb_sock

        while 1:
            try:
                header_data = jb_sock.recv(4)
                if header_data:
                    tid, len_ = comm.struct_unpack(header_data)
                    content_data = jb_sock.recv(len_)
                    if content_data:
                        content_data = comm.unpack_data(content_data)
                        self.on_message(jb_sock, tid, content_data)
                else:
                    break
            except Exception, e:
                comm.print_exception(e)
                break
        print('Client %s disconnected.' % (str(address), ))
        # 从客户socket列表中关闭并删除掉已经断开的socket
        jb_sock.close()
        del JBServer.client_dict[jb_sock.sid]

    def do_send_message(self, sock, tid, message, echo_msg=''):
        for sid, client_sock in JBServer.client_dict.iteritems():
            if client_sock is not sock:
                if message is not None:
                    client_sock.sendall(comm.pack_data(tid, message))
            else:
                if echo_msg is not None:
                    client_sock.sendall(comm.pack_data(tid, echo_msg))

    def runserver(self, host, port): 
        server = StreamServer((host, port), self.mainloop)
        gevent.signal(signal.SIGTERM, server.close)
        gevent.signal(signal.SIGQUIT, server.close)
        gevent.signal(signal.SIGINT, server.close)

        # to start the server asynchronously, use its start() method;
        # we use blocking serve_forever() here because we have no other jobs
        print('Starting server on port %s' % port)
        server.serve_forever()


class JBSocket(object):

    sid = ''

    def __init__(self, sock, sid):
        self._sock = sock
        self.sid = sid
        self._data = {}

    def recv(self, size_):
        return self._sock.recv(size_)

    def sendall(self, data):
        return self._sock.sendall(data)

    def get_sock(self):
        return self._sock

    def close(self):
        return self._sock.close()

    def set_data(self, k, v):
        self._data[k] = v

    def get_data(self, k):
        return self._data.get(k, None)

if __name__ == '__main__':
    JBServer().runserver('0.0.0.0', 5005)
