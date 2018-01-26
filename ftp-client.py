#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket
import os
import hashlib

ip_port = ('127.0.0.1',7777)

sk = socket.socket()
sk.connect(ip_port)

while True:
    client_input = input("cmd#:").strip()
    if len(client_input) == 0 :
        continue
    if client_input == 'q':
        break
    file=client_input.split(" ")[1]
    print ("inputfilename:",file)
    sk.send(bytes(client_input,'utf8'))
    rec_filesize=sk.recv(1024)
    print ((rec_filesize).decode())
    if not rec_filesize:
        break
    else:
        sk.send("准备接收".encode())
    #filename = "testftp.new"
    f = open(file + ".new", "wb")  # 新文件，没有的话会创建
    #if os.path.exists(file) is True:
    #    print ("文件存在:",file)
    #    continue
    received_size = 0
    m = hashlib.md5()
    while received_size < int(rec_filesize):
        data = sk.recv(1024)
        received_size += len(data)
        #print (received_size)
        f.write(data)
        m.update(data)
    if int(rec_filesize) == received_size:
        print("文件传输完毕")
        md5=(sk.recv(500).decode())
        print (file,"服务端MD5:",md5)
        print (file + ".new","客户端MD5",m.hexdigest())
        f.close()
sk.close()