#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import sys
# from numba import jit
# import numba

# 定数
# 何も置かれていない
NONE = None
# 白
WHITE = False
# 黒
BLACK = True

# Common Functions


def get_score(board, color):
    """ 指定した色の現在のスコアを返す """
    score = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] == color:
                score += 1
    return score


def get_remain(board):
    """ 何も置かれていない場所の数を返す """
    count = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] is None:
                count += 1
    return count


def has_right_reversible_stone(board, i, j, color):
    """ 指定座標の右側に返せる石があるか調べる """
    enemy = not(bool(color))
    if j <= 5 and board[i][j+1] == enemy:
        for k in range(j + 2, 8):
            if board[i][k] == color:
                return True
            elif board[i][k] == NONE:
                break
    return False


def has_left_reversible_stone(board, i, j, color):
    """ 指定座標の左側に返せる石があるか調べる """
    enemy = not(bool(color))
    if j >=2 and board[i][j-1] == enemy:
        for k in range(j - 2, -1, -1):
            if board[i][k] == color:
                return True
            elif board[i][k] == NONE:
                break
    return False


def has_upper_reversible_stone(board, i, j, color):
    """ 指定座標の上に返せる石があるか調べる """
    enemy = not(bool(color))
    if i >= 2 and board[i-1][j] == enemy:
        for k in range(i - 2, -1, -1):
            if board[k][j] == color:
                return True
            elif board[k][j] == NONE:
                break
    return False


def has_lower_reversible_stone(board, i, j, color):
    """ 指定座標の下に返せる石があるか調べる """
    enemy = not(bool(color))
    if i <= 5 and board[i+1][j] == enemy:
        for k in range(i + 2, 8):
            if board[k][j] == color:
                return True
            elif board[k][j] == NONE:
                break
    return False


def has_right_upper_reversible_stone(board, i, j, color):
    """ 指定座標の右上に返せる石があるか調べる """
    enemy = not(bool(color))
    if i >= 2 and j <= 5 and board[i-1][j+1] == enemy:
        k = 2
        while i - k >= 0 and j + k < 8:
            if board[i-k][j+k] == color:
                return True
            elif board[i-k][j+k] == NONE:
                break
            k += 1
    return False


def has_left_lower_reversible_stone(board, i, j, color):
    """ 指定座標の左下に返せる石があるか調べる """
    enemy = not(bool(color))
    if j >= 2 and i <= 5 and board[i+1][j-1] == enemy:
        k = 2
        while i + k < 8 and j - k >= 0:
            if board[i+k][j-k] == color:
                return True
            elif board[i+k][j-k] == NONE:
                break
            k += 1
    return False


def has_left_upper_reversible_stone(board, i, j, color):
    """ 指定座標の左上に返せる石があるか調べる """
    enemy = not(bool(color))
    if i >= 2 and j >= 2 and board[i-1][j-1] == enemy:
        k = 2
        while i - k >= 0 and j - k >= 0:
            if board[i-k][j-k] == color:
                return True
            elif board[i-k][j-k] == NONE:
                break
            k += 1
    return False


def has_right_lower_reversible_stone(board, i, j, color):
    """ 指定座標の右下に返せる石があるか調べる """
    enemy = not(color)
    if i <= 5 and j <= 5 and board[i+1][j+1] == enemy:
        k = 2
        while i + k < 8 and j + k < 8:
            if board[i+k][j+k] == color:
                return True
            elif board[i+k][j+k] == NONE:
                break
            k += 1
    return False


def is_game_set(board):
    """ ゲーム終了か判定する """
    if len(get_puttable_points(board, WHITE)) == 0 and len(get_puttable_points(board, BLACK)) == 0:
        return True
    return False

def get_puttable_points(board, color):
    """ 指定した色が置ける座標をすべて返す """
    points = []
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != NONE:
                # 何か置かれている場所はする
                continue

            # 左右に走査
            if has_right_reversible_stone(board, i, j, color) or has_left_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue

            # 上下に走査
            if has_upper_reversible_stone(board, i, j, color) or has_lower_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue

            # 右斜め上、左斜め下
            if has_right_upper_reversible_stone(board, i, j, color) or has_left_lower_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue

            # 左上、右下
            if has_left_upper_reversible_stone(board, i, j, color) or has_right_lower_reversible_stone(board, i, j, color):
                points.append([i, j])
                continue
    return points

def put_stone(board, color, i, j):
    """ ひっくり返す """
    new_board = copy.deepcopy(board)

    # 右側をひっくり返しord[i][k] != color:
    if has_right_reversible_stone(new_board, i, j, color):
        k = j + 1
        while new_board[i][k] != color:
            new_board[i][k] = color
            k += 1

    # 左側をひっくり返していく
    if has_left_reversible_stone(new_board, i, j, color):
        k = j - 1
        while new_board[i][k] != color:
            new_board[i][k] = color
            k -= 1

    # 上側をひっくり返していく
    if has_upper_reversible_stone(new_board, i, j, color):
        k = i - 1
        while new_board[k][j] != color:
            new_board[k][j] = color
            k -= 1

    # 下側をひっくり返していく
    if has_lower_reversible_stone(new_board, i, j, color):
        k = i + 1
        while new_board[k][j] != color:
            new_board[k][j] = color
            k += 1

    # 右下をひっくりかえしていく
    if has_right_lower_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i+k][j+k] != color:
            new_board[i+k][j+k] = color
            k += 1

    # 左上をひっくりかえしていく
    if has_left_upper_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i-k][j-k] != color:
            new_board[i-k][j-k] = color
            k += 1

    # 右上をひっくりかえしていく
    if has_right_upper_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i-k][j+k] != color:
            new_board[i-k][j+k] = color
            k += 1

    # 左下をひっくり返していく
    if has_left_lower_reversible_stone(new_board, i, j, color):
        k = 1
        while new_board[i+k][j-k] != color:
            new_board[i+k][j-k] = color
            k += 1

    new_board[i][j] = color
    return new_board


def print_board(board):
    """盤面表示"""
    print ("   0 1 2 3 4 5 6 7")
    for i in range(0, 8):
        row = str(i) + " |"
        for j in range(0, 8):
            if board[i][j] == NONE:
                row += " "
            elif board[i][j] == WHITE:
                row += "○"
            else:
                row += "●"
            row += "|"
        print (row)
    print ("----")
    print ("white "+str(get_score(board, WHITE)))
    print ("black "+str(get_score(board, BLACK)))
    print ("")
def choose(candidates, probabilities):
    probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
    if probabilities[-1] > 1.0:
        #確率の合計が100%を超えていた場合は100％になるように調整する
        probabilities = [x/probabilities[-1] for x in probabilities]
        rand = random.random()
        for candidate, probability in zip(candidates, probabilities):
            if rand < probability:
                return candidate
            #どれにも当てはまらなかった場合はNoneを返す
        return None
