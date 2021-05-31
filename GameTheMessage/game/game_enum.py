import enum


class Camp(enum):
    # 阵营
    AGENT = 1   # 特工
    LURKER = 2  # 潜伏
    MILITARY = 3    # 军情


class Intelligence(enum):
    # 情报
    SECRET = 1  # 密电
    DIRECT = 2  # 直达
    TEXT = 3    # 文本


class Skill(enum):
    # 技能
    TRYOUT = 1      # 试探
    SECRETLY = 2    # 秘密下达
    PUBLIC = 3      # 公开文本
    INTERCEPT = 4   # 截获
    TRANSFER = 5    # 转移
    LURING = 6      # 调虎离山
    BURN = 7        # 烧毁
    CHANGE = 8      # 调包
    DIVORCE = 9     # 离间
    DANGEROUS = 10  # 危险情报
    PENETRATE = 11  # 识破
    REINFORCE = 12  # 增援
    SECRETDOC = 13  # 机密文件
    DECIPHER = 14   # 破译
    LOCK = 15       # 锁定


class Phase(enum):
    # 游戏状态
    LOBBY = 0       # 房间内
    TURNSTART = 1   # 回合开始
    DRAW = 2        # 抽牌
    ACTION1 = 3     # 行动阶段1
    DECLARE = 4     # 宣告传递情报
    TRANSFER = 5    # 情报到达
    RECEIVE = 6     # 宣告接收情报
    ACTION2 = 7     # 行动阶段2
    TURNEND = 8     # 回合结束
