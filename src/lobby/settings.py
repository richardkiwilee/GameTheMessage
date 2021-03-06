import os
from socket import *
from random import randint
import shelve

# 客户端client.py文件中供pipe_server和pipe_client使用的套接字地址
# 因为每个客户端都必须有不同的套接字来作起到连接键盘输入和网络套接字之间的管道的作用
# 使用一个文件记录下每一次运行出现的端口号，以保证不重复
if not os.path.exists("ports.dat"):
    f = shelve.open("ports")
    f["ports"] = []
f = shelve.open("ports")
while True:
    n = randint(4500, 10000)
    if n not in f["ports"]:
        f['ports'].append(n)
        break
f.close()
CLI_PIPE_PORT = n

# 缓冲区大小
BUFFERSIZE = 1024


# 返回一个TCP服务端套接字
def server(addr):
    sock = socket(AF_INET, SOCK_STREAM, 0)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(10)
    return sock


# 返回一个TCP客户端套接字
def client(addr):
    sock = socket(AF_INET, SOCK_STREAM, 0)
    sock.connect(addr)
    return sock


def clear_all():
    _f = shelve.open("ports")
    _f['ports'].clear()
    _f.close()
