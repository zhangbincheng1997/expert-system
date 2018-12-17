#!/usr/bin/python
# -*- coding: UTF-8 -*-

import platform
import time
from os import system

ROW = COL = 3
board = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]
ME = 'X'
AI = 'Y'


class Position():
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score


"""
--------------
| 0 || 1 || 2 |
| 3 || 4 || 5 |
| 6 || 7 || 8 |
--------------
各位置出现次数(4是关键点)：
0:3     1:2     2:3
3:2     4:4     5:2
6:3     7:2     8:3

获胜的算法：
012     345     678
036     147     258
048     246
"""


# 胜利条件
def win(player):
    wins = [[board[0], board[1], board[2]], [board[3], board[4], board[5]], [board[6], board[7], board[8]],
            [board[0], board[3], board[6]], [board[1], board[4], board[7]], [board[2], board[5], board[8]],
            [board[0], board[4], board[8]], [board[2], board[4], board[6]]]
    state = [player, player, player]
    if state in wins:
        return True
    else:
        return False


# AI预测-局面打分，AI希望自己高分
def score_for_ai():
    if win(AI):  # AI胜利
        return +1
    elif win(ME):  # 人类胜利
        return -1
    return 0  # 打平


# 棋盘是否存在空位
def empty():
    if board.count(0) != 0:
        return True
    return False


# pos位置是否有棋
def check(pos):
    if board[pos] == 0:
        return True
    else:
        return False


# 允许走棋
def move(pos, player):
    board[pos] = player


# 极大极小值算法
# 返回值：[pos_x, pos_y, score]
def minimax(player, step):
    if step == 0 or win(ME) or win(AI):
        return Position(-1, -1, score_for_ai())  # pos_x pos_y 后面会更新

    # 初始化最优值
    from math import inf as infinity
    if player == ME:
        best = Position(-1, -1, +infinity)
    elif player == AI:
        best = Position(-1, -1, -infinity)

    for i in range(ROW):
        for j in range(COL):
            if board[i * ROW + j] == 0:  # 试探
                board[i * ROW + j] = player  # 记录
                nextp = ME if (player == AI) else AI  # 思考对手下棋
                P = minimax(nextp, step - 1)  # 继续极大极小值算法
                board[i * ROW + j] = 0  # 重置

                P.x, P.y = i, j

                if player == ME:  # 极小 min value
                    if P.score < best.score:
                        best = P
                elif player == AI:  # 极大 max value
                    if P.score > best.score:
                        best = P

    return best


# AI走棋
def ai_turn():
    print('AI思考中......')
    time.sleep(1)  # 假装思考
    step = board.count(0)  # 思考步数

    if board[5 - 1] == 0:  # 优化：中间有优势
        pos = 5 - 1
    else:  # 极大极小值算法
        P = minimax(AI, step)
        pos = P.x * ROW + P.y
    move(pos, AI)
    flush()
    render()


# 人类走棋
def me_turn():
    while True:
        pos = input('请输入下棋位置[1-9]：')
        if pos.isdigit() and 1 <= int(pos) <= 9:
            pos = int(pos) - 1  # 下标从零开始
        else:
            print('输入不合法')
            continue

        if check(pos):
            move(pos, ME)
            flush()
            render()
            break
        else:
            print('此处不允许下棋')
            continue


# 渲染游戏
def render():
    print('--------------')
    for x in range(ROW):
        for y in range(COL):
            print('|', board[x * ROW + y], '|', end='')
        print()
    print('--------------')


# 刷新屏幕
def flush():
    os_name = platform.system().lower()
    if os_name == 'windows':
        system('cls')
    else:
        system('clear')


if __name__ == '__main__':
    choice = input("请选择棋子类型：[X/Y]，默认'X' >>> ")
    if choice == 'Y':
        ME = 'Y'
        AI = 'X'

    choice = input("请选择是否先手：[T/F]，默认'T' >>> ")
    if choice == 'F':
        choice = False
    else:
        choice = True

    render()

    # 游戏开始
    while True:
        if not empty():
            print('平手')
            break

        if choice:
            me_turn()
        else:
            ai_turn()
        choice = not choice  # 轮到对方

        if win(ME):
            print('玩家胜利！！！')
            break
        elif win(AI):
            print('AI胜利！！！')
            break
