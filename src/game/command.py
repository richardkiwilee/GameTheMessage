import logging
import logging.config
from terminaltables import AsciiTable, SingleTable, DoubleTable
import os
import configparser
from src.game.game_msg import MsgBuilder
from src.lobby.settings import client
from src.game.desktop import Desktop

QUIT_COMMAND = 'quit.'


class CommandBase:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def beautiful_table(table_data: list):
        table = DoubleTable(table_data)
        print(table.table)

    def is_command(self, cmd):
        raise NotImplementedError

    def run(self, cmd):
        # if cmd in ['help', 'desktop', 'cls', 'cards', 'character']:
        #     eval(f'PrivateCommand.{cmd}()')
        #     return
        # if cmd.split(' ')[0] in ['replay', 'tag']:
        #     func = getattr(PrivateCommand, cmd.split(' ')[0])
        #     func(cmd)
        #     return
        try:
            g = cmd.split(' ')
            if '__self__' in dir(eval(f'self.{g[0]}')):  # 普通方法
                func = getattr(self, g[0])
                func(cmd)
            else:
                eval(f'self.{g[0]}({cmd})')
        except Exception as ex:
            logging.error(f'command:"{cmd}" error occur: {ex}')


class HostCommand(CommandBase):
    def is_command(self, cmd):
        _cmd = [str(att) for att in dir(HostCommand) if not att.startswith('__')]
        return cmd.split(' ')[0] in _cmd

    @staticmethod
    def edit(setting: configparser.ConfigParser, setting_path=None):
        """编辑游戏设置"""

        def saved_input(section: str, option: str, desc: str, c: type, _setting: configparser.ConfigParser):
            _input = input(f'{section}[{desc}:{c.__name__}]({_setting.get(section, option)})')
            while True:
                if _input != '':
                    try:
                        convert_int = int(_input)
                        _setting.set(section, option, str(convert_int))
                        break
                    except Exception as ex:
                        logging.warning(ex)
                        _input = input(f'\r{section}[{desc}:{c.__name__}]({_setting.get(section, option)})')
                else:
                    break

        if setting_path is None:
            logging.warning('非房主无法修改配置参数。')
            return
        saved_input('GAME', 'TURN_TIME', '回合时长', int, setting)
        saved_input('GAME', 'RESPONSE_TIME', '响应时限', int, setting)
        saved_input('GAME', 'ADDITIONAL_THINKING_TIME', '长考时限', int, setting)
        saved_input('GAME', 'ASK_BY_ORDER', '顺序询问', int, setting)
        saved_input('GAME', 'CONFUSE_RESPONSE', '响应混淆', int, setting)
        saved_input('ADVANCERULES', 'PREDICT_DECIPHER', '预言破译规则', int, setting)
        saved_input('ADVANCERULES', 'NO_DELIVERY_DEATH', '无可用情报死亡', int, setting)
        setting.write(open(setting_path, 'w'))

    @staticmethod
    def start(builder: MsgBuilder, setting_path, hp: tuple):
        """开始游戏"""
        if setting_path is None:
            logging.warning('非房主无法启动游戏。')
            return None
        pipe_client = client(hp)
        pipe_client.send(builder.encode('system', 'game init', 0, 'init'))
        pipe_client.close()
        pipe_client = client(hp)
        pipe_client.send(builder.encode('system', 'game init', 0, 'init'))
        pipe_client.close()
        pipe_client = client(hp)
        pipe_client.send(builder.encode('system', 'game init', 0, 'init'))
        pipe_client.close()
        pipe_client = client(hp)
        pipe_client.send(builder.encode('system', 'game init', 0, 'init'))
        pipe_client.close()
        pipe_client = client(hp)
        pipe_client.send(builder.encode('system', 'game init', 0, 'init'))
        pipe_client.close()


class PrivateCommand(CommandBase):
    def __init__(self, name):
        super().__init__(name)
        self.tags = {}

    def is_command(self, cmd):
        _cmd = [str(att) for att in dir(PrivateCommand) if not att.startswith('__')]
        return cmd.split(' ')[0] in _cmd

    @staticmethod
    def help(cmd=None):
        """查看帮助"""
        h = [['命令类别', '命令格式', '描述'],
             ['房主', 'edit', '编辑游戏设置'],
             ['房主', 'start', '开始游戏'],
             ['本地', 'help', '显示此帮助'],
             ['本地', 'desktop', '输出当前台面'],
             ['本地', 'cls', '清空屏幕'],
             ['本地', 'replay', '重放最新n回合'],
             ['本地', 'cards', '查看我的人物卡和手牌'],
             ['本地', 'character', '根据名称查看一张人物卡'],
             ['本地', 'tag', '标记一名玩家的身份'],
             ['响应', 'pause', '请求长考']
             ]
        PrivateCommand.beautiful_table(h)

    @staticmethod
    def cls(cmd=None):
        """清空记录"""
        os.system('cls')

    @staticmethod
    def replay(cmd):
        """回放数回合的记录"""
        turn = cmd.split(' ')[1]
        pass

    @staticmethod
    def character(cmd):
        """查看一张人物卡"""
        name = cmd.split(' ')[1]

    def tag(self, cmd):
        """标记一个角色的身份"""
        name = cmd.split(' ')[1]
        try:
            identity = cmd.split(' ')[2]
            self.tags[name] = identity
        except IndexError:
            if name in self.tags.keys():
                self.tags.__delitem__(name)


class PublicCommand(CommandBase):
    def is_command(self, cmd):
        _cmd = [str(att) for att in dir(PublicCommand) if not att.startswith('__')]
        return cmd.split(' ')[0] in _cmd

    @staticmethod
    def pause():
        """请求长考"""
        pass

    @staticmethod
    def ready():
        """玩家准备"""


class GameInstCommand(CommandBase):
    """远程进程类共享 对公共信息的类直接同步"""

    def is_command(self, cmd):
        _cmd = [str(att) for att in dir(GameInstCommand) if not att.startswith('__')]
        return cmd.split(' ')[0] in _cmd

    def desktop(self, inst: Desktop):
        """输出当前桌面"""
        print(inst.desktop())
        self.beautiful_table([[], []])
        return inst.desktop()

    def card(self, inst: Desktop):
        # 查看自己手牌
        print(inst.card(self.name))
        return inst.card(self.name)

    def used(self, inst: Desktop):
        # 查看弃牌堆
        print(inst.used())
        return inst.used()
