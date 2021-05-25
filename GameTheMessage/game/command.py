import logging
import logging.config
from terminaltables import AsciiTable
import os
import configparser
from GameTheMessage.game.game_msg import MsgBuilder
from GameTheMessage.lobby.settings import client

QUIT_COMMAND = 'quit.'


class CommandBase:
    @staticmethod
    def is_command(cmd):
        raise NotImplementedError

    @staticmethod
    def run(cmd):
        raise NotImplementedError


class HostCommand(CommandBase):
    @staticmethod
    def is_command(cmd):
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

    @staticmethod
    def run(cmd):
        pass


class PrivateCommand(CommandBase):
    @staticmethod
    def run(cmd):
        if cmd in ['help', 'desktop', 'cls', 'cards', 'character']:
            eval(f'PrivateCommand.{cmd}()')
            return
        if cmd.split(' ')[0] in ['replay', 'tag']:
            func = getattr(PrivateCommand, cmd.split(' ')[0])
            func(cmd)
            return

    @staticmethod
    def beautiful_table(table_data: list):
        table = AsciiTable(table_data)
        print(table.table)

    @staticmethod
    def is_command(cmd):
        _cmd = [str(att) for att in dir(PrivateCommand) if not att.startswith('__')]
        return cmd.split(' ')[0] in _cmd

    @staticmethod
    def help():
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
    def desktop():
        """输出当前桌面"""
        pass

    @staticmethod
    def cls():
        """清空记录"""
        os.system('cls')

    @staticmethod
    def replay(turn=0):
        """回放数回合的记录"""
        pass

    @staticmethod
    def cards():
        """查看自己的人物卡及手牌"""
        pass

    @staticmethod
    def character(name):
        """查看一张人物卡"""
        pass

    @staticmethod
    def tag(name, identity):
        """标记一个角色的身份"""
        pass


class PublicCommand(CommandBase):
    @staticmethod
    def is_command(cmd):
        _cmd = [str(att) for att in dir(PublicCommand) if not att.startswith('__')]
        return cmd.split(' ')[0] in _cmd

    @staticmethod
    def pause():
        """请求长考"""
        pass

    @staticmethod
    def run(cmd):
        pass