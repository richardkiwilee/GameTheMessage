import json
import logging


class MsgPhaser:
    def __init__(self, name):
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        self.name = name

    def parse(self, msg: dict):
        if msg.get('target') is not None:
            if self.name not in msg.get('target').split(','):
                # self.logger.info('不是给我的消息')
                pass
            else:
                # 给我的消息 进行处理
                pass
