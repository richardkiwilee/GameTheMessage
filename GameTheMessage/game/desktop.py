class Desktop:
    def __init__(self):
        self.gid = -1
        self.players = []
        self.cards = []
        self.used = []
        self.executed = []
        self.turn = 1

    def get_turn(self):
        return self.turn

    def next_turn(self):
        self.turn += 1
