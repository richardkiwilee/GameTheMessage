class Desktop:
    def __init__(self):
        self.gid = -1
        self.players = []
        self.cards = {}
        self.used = []
        self.executed = []
        self.turn = 1

    def get_turn(self):
        return self.turn

    def next_turn(self):
        self.turn += 1

    def card(self, name):
        return self.cards[name]

    def add_player(self, name):
        if name not in self.players:
            self.players.append(name)
            self.cards[name] = []

    def draw(self, name, num=2):
        for i in range(0, num):
            self.cards[name].append('A')

    def get_card(self, name):
        return self.cards[name]
