#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket
import os

#导入 socket、subprocess模块
import socket
import subprocess
import time
import hashlib

class ftpserver(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def start(self):
        # 创建socket对象
        sk = socket.socket()
        ip_port = (self.host,self.port)
        sk.bind(ip_port)
        # 设置最大连接数，超过后排队
        sk.listen(5)
        while True:
            print('server waiting...')
            conn, addr = sk.accept()
            print("client:", addr)
            while True:
                client_data = conn.recv(1024)
                if not client_data:
                    break
                    print("close client")
                client_cmd = str(client_data, 'utf8')  # 接收客户端指令
                print("recv_cmd:", client_cmd)
                try:
                    cmd, filename = client_cmd.split()
                    if os.path.isfile(filename):  # 如果是文件
                        f = open(filename, "rb")
                        m = hashlib.md5()
                        file_size = os.stat(filename).st_size  # 获取文件大小
                        print("filesize", file_size)
                        conn.send(str(file_size).encode())
                        rec_file_check = conn.recv(1024)
                        print((rec_file_check).decode())
                        for file in f:
                            conn.send(file)  # 发送数据
                            m.update(file)
                        f.close()
                        md5 = m.hexdigest()
                        conn.send(str(md5).encode())
                        print(filename, "MD5:", md5)
                except ValueError as e:
                    print('ValueError:', e)
        conn.close()

    def wget(self):
        pass

s = ftpserver('0.0.0.0',7777)
s.start()




