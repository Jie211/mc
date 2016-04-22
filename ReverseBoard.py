#!/usr/bin/python
# -*- coding: utf-8 -*-
import ReverseCommon


class ReverseBoard:
    """ オセロ盤 """
    def __init__(self):
        """ Constructor """
        # ボード初期化
        self._board = [[ReverseCommon.NONE for i in range(8)] for j in range(8)]
        self._board[3][3] = ReverseCommon.WHITE
        self._board[4][4] = ReverseCommon.WHITE
        self._board[3][4] = ReverseCommon.BLACK
        self._board[4][3] = ReverseCommon.BLACK

        # 黒のターンに初期化
        self._turn = ReverseCommon.BLACK

    def change_turn(self):
        """ 交代 """
        if self._turn == ReverseCommon.WHITE:
            self._turn = ReverseCommon.BLACK
        else:
            self._turn = ReverseCommon.WHITE

    def put_stone(self, color, i, j):
        """ 置く & ひっくり返す """
        self._board = ReverseCommon.put_stone(self._board, color, i, j)

        # プレーヤ交代
        enemy = not(color)
        if len(ReverseCommon.get_puttable_points(self._board, enemy)) > 0:
            self.change_turn()

    def is_game_set(self):
        """ ゲームセットか返す"""
        return ReverseCommon.is_game_set(self._board)

    def is_my_turn(self, color):
        """ 自分のターンか返す """
        if self._turn == color:
            return True
        return False

    @property
    def board(self):
        """ 盤面を返す"""
        return self._board


class CustomReverseBoard(ReverseBoard):
    """ 途中状態の盤面を作るようのクラス """
    def __init__(self, board, turn):
        self._board = board
        self._turn = turn
