import logging
import logging.config


class Game:
    def __init__(self):
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        self.logger.info('房间实例实例化。')
        self.players = []
        self.mid = 0
