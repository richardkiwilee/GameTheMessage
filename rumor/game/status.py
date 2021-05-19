from enum import Enum


class GameStatus(Enum):
    LOBBY = 0
    DISBAND = 1
    DECLAR_DRAW = 2
    SUCCESS_DRAW = 3
    DECLAR_DELIVER = 4
    DECLAR_RECEIVE = 6
    SUCCESS_RECEIVE = 7
    INTERRUPT = 8
    LONG_THINKING = 9
    DECLAR_WIN = 10
    SUCEESS_WIN = 11


class PlayerStatus(Enum):
    MY_DRAW = 0
    MY_DELIVER = 1
    MY_END = 2
    NY_LONG_THINK = 3
    MY_DECLAR = 4

    OTHER_DRAW = 5
    OTHER_DELIVER = 6
    OTHER_END = 7
    OTHER_LONG_THINK = 8
    OTHER_DECLAR = 9

    MY_DEATH = 10
    OTHER_DEATH = 11


