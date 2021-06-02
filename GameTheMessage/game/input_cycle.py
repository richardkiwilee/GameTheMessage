import sys
import logging
import logging.config
from GameTheMessage.lobby.settings import client, server
from GameTheMessage.lobby.settings import clear_all
from GameTheMessage.game.command import HostCommand, PublicCommand, PrivateCommand, QUIT_COMMAND, GameInstCommand
from GameTheMessage.game.desktop import Desktop
from GameTheMessage.game.game_msg import MsgBuilder
import json


class InputCycle:
    def __init__(self, setting, name, game_inst: Desktop, setting_path=None):
        self.game = game_inst   # type: Desktop
        self.setting_path = setting_path
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        self.waiting_response = False       # 标记你是否处在响应点, 处于响应点内部分命令不可用
        self.setting = setting
        self.name = name
        self.host_command = HostCommand(self.name)
        self.public_command = PublicCommand(self.name)
        self.private_command = PrivateCommand(self.name)
        self.inst_command = GameInstCommand(self.name)
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
                if self.public_command.is_command(data):
                    pipe_client = client((pipe_host, pipe_port))
                    # pipe_client.send(bytes(data, "UTF-8"))
                    pipe_client.send(bytes(data, "UTF-8"))
                    pipe_client.close()
                elif self.private_command.is_command(data):
                    self.private_command.run(data)
                elif self.host_command.is_command(data):
                    if data == 'edit':
                        HostCommand.edit(self.setting, self.setting_path)
                    elif data == 'start':
                        HostCommand.start(self.msg_builder, self.setting_path, (pipe_host, pipe_port))
                elif self.inst_command.is_command(data):
                    if data == 'desktop':
                        print('here')
                        if self.game is None:
                            self.logger.error('game is None')
                        else:
                            print(self.game.desktop())
                    else:
                        self.logger.error(f'嗯？{data}')
                        self.inst_command.run(self.game)
                else:
                    self.logger.info('无效的命令')
