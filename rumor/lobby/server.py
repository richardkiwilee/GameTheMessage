from select import select
from multiprocessing import Process
from rumor.lobby.settings import *
import shelve
import logging
import logging.config
from rumor.game.core import Game
from rumor.game.input_cycle import InputCycle
import json
import configparser
from multiprocessing.managers import BaseManager
import sys
import random
# https://my.oschina.net/u/4258573/blog/3327582

class TestGame:
    def __init__(self):
        self.data = {'mid': 0}

    def get(self):
        return self.data

    def add(self):
        self.data['mid'] += 1


class MyManager(BaseManager):
    pass


class HostMgr:
    def __init__(self, _sock_server, _pipe_server, game_inst):
        self.game = game_inst   # type: TestGame
        self.sock_server = _sock_server
        self.pipe_server = _pipe_server
        self.rlist = [_sock_server, _pipe_server]
        self.wlist = []
        self.xlist = []
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        self.logger.info('房间已经建立。')

    def start(self):
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock_server:
                    # 接受客户端连接
                    conn, addr = self.sock_server.accept()
                    self.rlist.append(conn)
                elif r is self.pipe_server:
                    # 接收键盘输入并发送到所有客户端去
                    conn, addr = self.pipe_server.accept()
                    _data = conn.recv(BUFFERSIZE)
                    self.logger.info('接受键盘输入')      # 服务端输入add的时候走到这里
                    if random.randint(0, 1):
                        for c in self.rlist[2:]:
                            c.send(_data)
                    else:
                        # 这里需要与外部保持一致
                        self.logger.info('服务端键盘输入被拒绝')
                    conn.close()
                else:
                    # 接收客户端信息
                    # 将客户端信息发送到所有的客户端中去
                    self.logger.info('客户端接收到了消息')
                    try:
                        _data = r.recv(BUFFERSIZE)
                    except Exception as ex:
                        logging.warning(ex)
                        r.close()
                        self.rlist.remove(r)
                    else:
                        if json.loads(_data).get('data') == 'add' and random.randint(0, 1):
                            self.logger.info('客户端请求被接受发送到所有client: ' + json.loads(_data).get('data'))
                            for c in self.rlist[2:]:
                                c.send(_data)
                            self.game.add()
                        else:
                            self.logger.info('客户端请求被拒绝.')


def listen(_sock_server, _pipe_server, game_inst):
    # IO多路复用：循环监听套接字
    h = HostMgr(_sock_server, _pipe_server, game_inst)
    h.start()


def create_lobby(config: str):
    # 首先将ports内容都删除
    setting = configparser.ConfigParser(allow_no_value=True)
    setting.read(config)
    clear_all()
    # 创建两个套接字
    # 套接字sock_server是一个TCP服务端，负责服务端与客户端的交流
    # 套接字pipe_server也是一个TCP服务端，不过起到管道的作用，负责接收键盘输入
    sock_server = server((setting.get('HOST', 'SOCKET_HOST'), setting.getint('HOST', 'SOCK_PORT')))
    pipe_server = server((setting.get('HOST', 'SOCKET_HOST'), setting.getint('HOST', 'SER_PIPE_PORT')))
    # 开始一个子进程，执行listen函数
    MyManager.register('GameInst', TestGame)
    manager = MyManager()
    manager.start()
    game_inst = manager.GameInst()      # type: TestGame

    p = Process(target=listen, args=(sock_server, pipe_server, game_inst))
    p.daemon = True
    p.start()
    c = InputCycle(setting, name='房主大人', setting_path=config, game_inst=game_inst)
    c.input_cycle2(sock_server, pipe_server,
                  setting.get('HOST', 'SOCKET_HOST'), setting.getint('HOST', 'SER_PIPE_PORT'), p)
