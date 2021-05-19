import json
import logging


class RumorProtocol:
    def __init__(self, user):
        self.user = user

    def encode(self, func, data):
        pass

    @staticmethod
    def decode(data):
        pass


class MessageHandle:
    def __init__(self):
        pass

    @staticmethod
    def handle(data):
        return {'level': logging.INFO, 'msg': data}
