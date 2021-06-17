# 定义消息的结构


class MsgStructure:
    def __init__(self):
        self.id = 0
        self.user = ''
        self.msg = ''
        self.event = ''
        self.target = ''

    def data(self):
        _msg = {"id": self.id, "user": self.user}
        return _msg
