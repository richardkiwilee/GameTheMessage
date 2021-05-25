import sys
import logging
import logging.config
from GameTheMessage.lobby.settings import client, server
from GameTheMessage.lobby.settings import clear_all
from GameTheMessage.game.command import HostCommand, PublicCommand, PrivateCommand, QUIT_COMMAND
from GameTheMessage.game.desktop import Desktop
from GameTheMessage.game.game_msg import MsgBuilder
import json


class InputCycle:
    def __init__(self, setting, name, setting_path=None, game_inst=None):
        self.game = game_inst
        self.setting_path = setting_path
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        self.waiting_response = False       # 标记你是否处在响应点, 处于响应点内部分命令不可用
        self.setting = setting
        self.hc = HostCommand()
        self.pub = PublicCommand()
        self.pri = PrivateCommand()
        self.msg_builder = MsgBuilder(name)

    def input_cycle(self, sock_server, pipe_server, pipe_host, pipe_port, p1, p2=None):
        while True:
            try:
                data = sys.stdin.readline()
            except KeyboardInterrupt:
                data = None
            if not data:
                continue
            else:
                data = data.split('\n')[0]
                # 获得键盘数据，创建客户端套接字pipe_client，将键盘输入传输给pipe_server
                if data == QUIT_COMMAND:
                    sock_server.close()
                    pipe_server.close()
                    p1.terminate()
                    if p2 is not None:
                        p2.terminate()
                    clear_all()
                    break
                if PublicCommand.is_command(data):
                    pipe_client = client((pipe_host, pipe_port))
                    # pipe_client.send(bytes(data, "UTF-8"))
                    pipe_client.send(bytes(json.dumps({'data': 'add'}), "UTF-8"))
                    pipe_client.close()
                elif PrivateCommand.is_command(data):
                    PrivateCommand.run(data)
                elif HostCommand.is_command(data):
                    if data == 'edit':
                        HostCommand.edit(self.setting, self.setting_path)
                    elif data == 'start':
                        HostCommand.start(self.msg_builder, self.setting_path, (pipe_host, pipe_port))
                else:
                    self.logger.info('无效的命令')

    def input_cycle2(self, sock_server, pipe_server, pipe_host, pipe_port, p):
        while True:
            try:
                data = sys.stdin.readline()
            except KeyboardInterrupt:
                data = None
            if not data:
                continue
            else:
                data = data.split('\n')[0]
                # 获得键盘数据，创建客户端套接字pipe_client，将键盘输入传输给pipe_server
                if data == QUIT_COMMAND:
                    sock_server.close()
                    pipe_server.close()
                    p.terminate()
                    clear_all()
                    break

                if data == 'add':
                    # if self.setting_path is not None:
                    #     self.game.add()
                    if self.setting_path is not None:
                        pipe_client = client((pipe_host, pipe_port))
                        pipe_client.send(bytes(json.dumps({'user': '111', 'data': data, 'type': 'system', 'func': 'join'}), "UTF-8"))
                        pipe_client.close()
                    else:
                        self.logger.info('客户端走到了这里')
                        # sock_server.send(bytes(json.dumps({'user': '111', 'data': 'add', 'type': 'system', 'func': 'join'}), "UTF-8"))
                        pipe_client = client((pipe_host, pipe_port))
                        pipe_client.send(bytes('add', "UTF-8"))
                        pipe_client.close()
                if data == 'get':
                    self.logger.info(self.game.get())