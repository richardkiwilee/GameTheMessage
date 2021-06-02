class Desktop:
    def __init__(self):
        self.players = []       # 玩家列表
        self.cards = {}         # 玩家手牌
        self.deck = []  # 牌堆
        self.used = []          # 弃牌堆
        self.executed = []      # 除外堆
        self.turn = 1           # 当前回合
        self.current_player = None  # 当前玩家
        self.player_order = None    # 玩家行动列表
        self.player_identity = {}   # 保存玩家身份
        self.response_stack = []    # 响应栈
        self.current_msgid = 0

    def get_cmid(self):
        return self.current_msgid

    def get_turn(self):
        """获得当前回合数"""
        return self.turn

    def _next_turn(self):
        """回合数加1"""
        self.turn += 1

    def card(self, name):
        """玩家查询自己的手牌"""
        return self.cards[name]

    def add_player(self, name):
        """玩家加入游戏"""
        if name not in self.players:
            self.players.append(name)
            self.cards[name] = []

    def _draw(self, name, num=2):
        """玩家抽取牌"""
        for i in range(0, num):
            self.cards[name].append('A')

    def desktop(self) -> list:
        """返回台面信息"""
        # [[player1, player2, player3...],
        # [角色卡1, 隐藏, 角色卡2...],
        # [情报1, 情报1, NULL...],
        # [情报2, NULL, NULL...],
        # [手牌4, 手牌3，手牌2...] ]
        try:
            players = [p for p in self.player_order]
            identity = [self.player_identity[p] for p in self.player_order]
            cards_view = [[], [], ]     # 将手牌转换成正确格式
            card_num = [len(self.cards[p]) for p in self.player_order]
            rt = [players, identity] + cards_view + [card_num]
            print(rt)
        except Exception as ex:
            rt = [['player1', 'player2', 'player3...'],
         ['角色卡1', '隐藏', '角色卡2...'],
         ['情报1', '情报1', 'NULL...'],
         ['情报2', 'NULL', 'NULL...'],
         ['手牌4', '手牌3','手牌2...'] ]
        return rt

    def used(self) -> list:
        # 查看弃牌堆
        return self.used

    def get_players(self) -> list:
        return self.players
