from select import select
from multiprocessing import Process
from .settings import *
import json
import logging
import logging.config
from multiprocessing.managers import BaseManager
from GameTheMessage.game.desktop import Desktop
from GameTheMessage.game.input_cycle import InputCycle
from GameTheMessage.lobby.msg_parser import MsgPhaser


def connect(sock_client, pipe_server, game_inst, name):
    game = game_inst        # type: Desktop
    # IO多路复用：循环监听套接字
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    parser = MsgPhaser(name)
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
                # for _data in data.split('}'):       # type: str
                #     if _data == '':
                #         continue
                #     _data += '}'
                #     _data = json.loads(_data)   # type: dict
                #     logger.debug(_data)
                #     if _data.get('data') == 'add':
                #         game.add()
                msg = json.loads(data)
                parser.parse(msg)

            elif r is pipe_server:
                # 接受键盘输入并发送给服务端
                conn, addr = pipe_server.accept()
                data = conn.recv(BUFFERSIZE)
                j = json.dumps({'user': name, 'data': data.decode().split('\n')[0],
                                'id': 0})
                data = bytes(j, "UTF-8")
                sock_client.send(data)
                conn.close()


def get_name():
    return input("输入你的昵称: ")


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

    MyManager.register('DesktopInst')
    manager = MyManager(address=('127.0.0.1', 6666), authkey=b'abracadabra')
    manager.connect()
    game_inst = manager.DesktopInst()      # type: Desktop
    p = Process(target=connect, args=(sock_client, pipe_server, game_inst, name))
    p.daemon = True
    p.start()

    c = InputCycle(setting, name=name, game_inst=game_inst)
    c.input_cycle(sock_client, pipe_server, setting.get('HOST', 'SOCKET_HOST'), CLI_PIPE_PORT, p1=p, p2=None)
    # while True:
    #     _input = input('->')
    #     if _input == 'exit':
    #         p.terminate()
    #         sock_client.close()
    #         pipe_server.close()
    #         break
