#coding:utf-8
from __future__ import absolute_import, division, print_function, \
    with_statement


__author__ = 'daimin'

from gevent.server import StreamServer
import gevent
import signal
import comm


class JBServer(object):

    client_list = []

    def __init__(self):
        pass

    def on_message(self, sock, type_, message):
        pass

    def mainloop(self, socket_, address):
        while 1:
            header_data = socket_.recv(4)
            if header_data:
                type_, len_ = comm.struct_unpack(header_data)
                content_data = socket_.recv(len_)
                if content_data:
                    content_data = comm.unpack_data(content_data)
                    self.on_message(socket_, type_, content_data)
            else:
                break
        print('Client %s disconnected.' % (str(address), ))
        socket_.close()

    def send_message(self, sock, type_, message):
        sock.sendall(comm.pack_data(type_, message))

    def runserver(self, host, port): 
        server = StreamServer((host, port), self.mainloop)
        gevent.signal(signal.SIGTERM, server.close)
        gevent.signal(signal.SIGQUIT, server.close)
        gevent.signal(signal.SIGINT, server.close)

        # to start the server asynchronously, use its start() method;
        # we use blocking serve_forever() here because we have no other jobs
        print('Starting server on port %s' % port)
        server.serve_forever()

if __name__ == '__main__':
    JBServer().runserver('0.0.0.0', 5005)