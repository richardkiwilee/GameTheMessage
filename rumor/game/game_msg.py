import json


class MsgBuilder:
    def __init__(self, username):
        self.user = username

    def encode(self, t, data, mid, func):
        if isinstance(data, str):
            j = {'user': self.user, 'type': t, 'data': data.split('\n')[0], 'mid': str(mid), 'func': func}
        else:
            j = {'user': self.user, 'type': t, 'data': data.decode().split('\n')[0], 'mid': str(mid), 'func': func}
        data = bytes(json.dumps(j), "UTF-8")
        return data

    @staticmethod
    def decode(msg) -> dict:
        j = json.loads(msg)     # type: dict
        return j

    def handle(self, data: dict):
        _user = data.get('user')
        _type = data.get('type')
        _data = data.get('data')
        _mid = data.get('mid')
        _func = data.get('func')
