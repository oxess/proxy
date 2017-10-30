#!/usr/bin/python

import threading
import socket
import os
import re


hr = re.compile(ur"GET\s(https?:\/\/)([\w\.]+)(.*)\s(HTTP\/([\d\.]+))")

def recvall(sock):
    data = ""
    while True:
        part = sock.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data

class Header:
    """"""

    def __init__(self):
        self.host = 'localhost'
        self.port = 80

    def parse(self, h):
        self.text = h
        lines = h.split("\n")
        for line in lines:
            m = hr.search(line)
            if m:
                self.host = m.group(2)
                # if m.group(3):
                #     self.port = int(m.group(3))



HOST, PORT = ('localhost', 1234)

_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_sock.bind((HOST, PORT))
_sock.listen(1)

try:
    while True:
        client, addr = _sock.accept()
        addr, port = addr

        print "Connect from %s" % addr

        header = Header()
        header.parse(recvall(client))

        print "Connect to: %s:%s" % (header.host, header.port)

        _dst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _dst.connect((header.host, header.port))

        _sock.sendall(header.text)

        while True:
            pack = recvall(_sock)
            print pack
            _dst.sendall(pack)

            pack = recvall(_dst)
            print pack
            client.sendall(pack)

except Exception as e:
    print e
    _sock.close()
