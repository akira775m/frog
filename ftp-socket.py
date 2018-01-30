#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import socket, threading, subprocess, hashlib, os

def tcplink(conn,addr):
    print('server waiting...')
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

# 创建一个socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口（这里的ip要在不同的情况下更改）
sk.bind(('0.0.0.0', 7777))
# 每次只允许一个客户端接入
sk.listen(1)
print ('Waiting for connection...')
while True:
    conn, addr = sk.accept()
    # 建立一个线程用来监听收到的数据
    t = threading.Thread(target = tcplink, args = (conn, addr))
    # 线程运行
    t.start()




