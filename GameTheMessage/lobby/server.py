from select import select
from multiprocessing import Process
from GameTheMessage.lobby.settings import *
import logging
import logging.config
import json
import configparser
from multiprocessing.managers import BaseManager
import random
from GameTheMessage.game.desktop import Desktop
from GameTheMessage.game.input_cycle import InputCycle
from GameTheMessage.__version__ import version


class MyManager(BaseManager):
    pass


class HostMgr:
    def __init__(self, _sock_server, _pipe_server, game_inst: Desktop):
        self.game = game_inst  # type: Desktop
        self.sock_server = _sock_server
        self.pipe_server = _pipe_server
        self.rlist = [_sock_server, _pipe_server]
        self.wlist = []
        self.xlist = []
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        self.logger.info('房间已经建立。')

    def start(self):
        ready_status = []
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
                    self.logger.info('接受键盘输入')  # 服务端输入add的时候走到这里
                    for c in self.rlist[2:]:
                        c.send(_data)
                    conn.close()
                else:
                    # 接收客户端信息
                    # 将客户端信息发送到所有的客户端中去
                    try:
                        _data = r.recv(BUFFERSIZE)
                        self.logger.info(f'接收到了客户端发送来的消息: {json.loads(_data)}')
                        # 服务端接受客户端的消息 进行处理 后将结果发送到所有客户端
                        # ret = handle(_data)
                        if json.loads(_data).get('data') == '进入了房间。':
                            # 校验版本号
                            user = json.loads(_data).get('user')
                            self.game.add_player(user)
                            ret = {"id": 0, 'msg': f'version={version}', 'target': user}
                        elif json.loads(_data).get('data') == 'ready':
                            user = json.loads(_data).get('user')
                            ready_status.append(user)
                            if set(ready_status) == set(self.game.get_players()):
                                self.logger.info('所有玩家准备完成，游戏开始。')
                        else:
                            ret = {"id": random.randint(0, 10), 'msg': 'test'}
                        for c in self.rlist[2:]:
                            c.send(bytes(json.dumps(ret), "UTF-8"))
                            # self.game.add()
                    except Exception as ex:
                        logging.warning(ex)
                        r.close()
                        self.rlist.remove(r)


def listen(_sock_server, _pipe_server, inst: Desktop):
    # IO多路复用：循环监听套接字
    h = HostMgr(_sock_server, _pipe_server, inst)
    h.start()


def remote_manager(inst):
    MyManager.register('DesktopInst', callable=lambda: inst)
    m = MyManager(address=('127.0.0.1', 6666), authkey=b'abracadabra')
    s = m.get_server()
    s.serve_forever()


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
    MyManager.register('DesktopInst', Desktop)
    manager = MyManager()
    manager.start()
    game_inst = manager.DesktopInst()  # type: Desktop

    p1 = Process(target=listen, args=(sock_server, pipe_server, game_inst))
    p2 = Process(target=remote_manager, args=(game_inst,))
    p1.daemon = True
    p1.start()
    p2.daemon = True
    p2.start()
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - 服务端主循环 - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    # while True:
    #     _input = input('->')
    #     if _input == 'exit':
    #         p1.terminate()
    #         p2.terminate()
    #         logger.info('退出...')
    #         break
    #     if _input == 'turn':
    #         logger.info(game_inst.get_turn())
    c = InputCycle(setting, name='服务端主进程', setting_path=config, game_inst=game_inst)
    c.input_cycle(sock_server, pipe_server,
                  setting.get('HOST', 'SOCKET_HOST'), setting.getint('HOST', 'SER_PIPE_PORT'), p1=p1, p2=p2)
