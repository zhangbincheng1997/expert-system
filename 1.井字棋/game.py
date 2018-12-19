#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
from abc import ABCMeta, abstractmethod

ROW = COL = 3  # 棋盘大小
SPACE = '-'  # 空格标签
HUMAN = 'HUMAN'  # 人类棋子标签
COMPUTER = 'COMPUTER'  # 电脑棋子标签


# 棋盘是否有空位
def empty(board):
    if board.count(SPACE) == 0:
        return False
    else:
        return True


# 判断player是否胜利
def winner(board, player):
    """
        --------------
        | 0 || 1 || 2 |
        | 3 || 4 || 5 |
        | 6 || 7 || 8 |
        --------------
        获胜的算法：
        012     345     678
        036     147     258
        048     246
    """
    wins = [[board[0], board[1], board[2]], [board[3], board[4], board[5]], [board[6], board[7], board[8]],
            [board[0], board[3], board[6]], [board[1], board[4], board[7]], [board[2], board[5], board[8]],
            [board[0], board[4], board[8]], [board[2], board[4], board[6]]]
    state = [player, player, player]
    if state in wins:
        return True
    else:
        return False


# 定义抽象基类
class Player(metaclass=ABCMeta):

    def __init__(self, chess):
        self.chess = chess

    @abstractmethod
    def move(self):
        pass


class Computer(Player):

    def __init__(self, chess='O'):
        Player.__init__(self, chess)

    def minimax(self, board, player, next_player, alpha=-2, beta=2):
        if winner(board, COMPUTER):  # 电脑胜利
            return +1
        if winner(board, HUMAN):  # 人类胜利
            return -1
        elif not empty(board):
            return 0  # 平局

        for move in range(ROW * COL):
            if board[move] == SPACE:  # 尝试下棋
                board[move] = player  # 记录
                val = self.minimax(board, next_player, player, alpha, beta)  # 继续思考对手怎么下棋
                board[move] = SPACE  # 重置

                if player == COMPUTER:  # 极大 max value
                    if val > alpha:
                        alpha = val
                    if alpha >= beta:  # 剪枝
                        return beta
                else:  # 极小 min value
                    if val < beta:
                        beta = val
                    if beta <= alpha:  # 剪枝
                        return alpha

        if player == COMPUTER:
            return alpha
        else:
            return beta

    def move(self, board):
        best = -2
        my_moves = []
        for move in range(ROW * COL):
            if board[move] == SPACE:  # 尝试下棋
                board[move] = COMPUTER  # 记录
                score = self.minimax(board, HUMAN, COMPUTER)  # 思考对手怎么下棋
                board[move] = SPACE  # 重置

                if score > best:  # 找到更优的位置
                    best = score
                    my_moves = [move]
                if score == best:  # 一样优秀的位置
                    my_moves.append(move)

        pos = random.choice(my_moves)  # 随机挑出一个位置
        board[pos] = COMPUTER


class Human(Player):

    def __init__(self, chess='X'):
        Player.__init__(self, chess)

    def move(self, board):
        looping = True
        while looping:
            try:
                inp = input("请输入下棋位置[1-9]：")
                pos = int(inp) - 1  # 输入的下标从1开始
                if 0 <= pos <= 8:
                    if board[pos] == SPACE:
                        looping = False
                    else:
                        print("此处不允许下棋")
                else:
                    print("输入不合法：[1-9]")
            except:
                print("输入不合法：Error")

        board[pos] = HUMAN


class Game:

    def __init__(self):
        # 初始化游戏
        self.board = [SPACE] * (ROW * COL)
        self.computer = Computer()
        self.human = Human()

        choice = input("请选择棋子类型：[X/O]，默认'X' >>> ")
        if choice == 'O':
            self.computer.chess = 'X'
            self.human.chess = 'O'
        else:
            self.computer.chess = 'O'
            self.human.chess = 'X'

        choice = input("请选择是否先手：[T/F]，默认'T' >>> ")
        if choice == 'F':
            self.current_player = self.computer
        else:
            self.current_player = self.human

    # 切换玩家
    def switch(self):
        if self.current_player == self.computer:
            self.current_player = self.human
        else:
            self.current_player = self.computer

    # 渲染游戏
    def render(self):
        print('--------------')
        for i in range(ROW):
            for j in range(COL):
                k = i * ROW + j
                if self.board[k] == HUMAN:
                    print('|', self.human.chess, '|', end='')
                elif self.board[k] == COMPUTER:
                    print('|', self.computer.chess, '|', end='')
                else:
                    print('|', self.board[k], '|', end='')
            print()
        print('--------------')

    # 开始游戏
    def start(self):
        # 渲染游戏
        self.render()

        # 游戏状态机
        while True:
            self.current_player.move(self.board)
            self.render()

            if winner(self.board, HUMAN):
                print("人类胜利！！！")
                exit(0)
            elif winner(self.board, COMPUTER):
                print("电脑胜利！！！")
                exit(0)
            elif not empty(self.board):
                print("平局！！！")
                exit(0)

            # 切换玩家
            self.switch()


if __name__ == '__main__':
    Game().start()
