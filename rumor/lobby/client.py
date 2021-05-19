from select import select
from multiprocessing import Process
from .settings import *
from rumor.lobby.server import InputCycle
import json
import logging
import logging.config
from rumor.game.game_msg import MsgBuilder
from multiprocessing.managers import BaseManager


def connect(sock_client, pipe_server, game_inst):
    game = game_inst        # type: TestGame
    # IO多路复用：循环监听套接字
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    rlist = [sock_client, pipe_server]
    wlist = []
    xlist = []
    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            if r is sock_client:
                data = sock_client.recv(BUFFERSIZE).decode()
                # 接受服务器消息 根据类型对game对象进行操作并输出信息等
                # logger.info('接受服务端消息：' + MsgBuilder.decode(data).get('data'))
                logger.info('接受服务端消息：' + data)
                for _data in data.split('}'):       # type: str
                    if _data == '':
                        continue
                    _data += '}'
                    _data = json.loads(_data)   # type: dict
                    logger.debug(_data)
                    if _data.get('data') == 'add':
                        game.add()

            elif r is pipe_server:
                logger.error('connect中的消息: 接受键盘输入并发送给服务端')
                # 接受键盘输入并发送给服务端
                conn, addr = pipe_server.accept()
                data = conn.recv(BUFFERSIZE)
                j = json.dumps({'user': 'client', 'data': data.decode().split('\n')[0], 'type': 'system', 'func': 'input'})
                data = bytes(j, "UTF-8")
                sock_client.send(data)
                conn.close()


def get_name():
    return input("输入你的昵称: ")


class TestGame:
    def __init__(self):
        self.data = {'mid': 0}

    def get(self):
        return self.data

    def add(self):
        self.data['mid'] += 1


class MyManager(BaseManager):
    pass


def join_lobby(setting):
    # 使用get_name函数获得用户名
    # name = get_name()
    name = 'test1'
    # 创建两个套接字
    # 套接字sock_client是一个TCP客户端，负责服务端与客户端的交流
    # 套接字pipe_server也是一个TCP服务端，不过起到管道的作用，负责接收键盘输入
    sock_client = client((setting.get('HOST', 'SOCKET_HOST'), setting.getint('HOST', 'SOCK_PORT')))
    sock_client.send(bytes(json.dumps({'user': name, 'data': '进入了房间。', 'type': 'system', 'func': 'join'}), "UTF-8"))
    pipe_server = server((setting.get('HOST', 'SOCKET_HOST'), CLI_PIPE_PORT))
    # 开始一个子进程，执行connect函数

    MyManager.register('GameInst', TestGame)
    manager = MyManager()
    manager.start()
    game_inst = manager.GameInst()      # type: TestGame

    p = Process(target=connect, args=(sock_client, pipe_server, game_inst))
    p.daemon = True
    p.start()
    c = InputCycle(setting, name=name, game_inst=game_inst)
    c.input_cycle2(sock_client, pipe_server, setting.get('HOST', 'SOCKET_HOST'), CLI_PIPE_PORT, p)
