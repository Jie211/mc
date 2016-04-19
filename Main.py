#!/usr/bin/python
# -*- coding: utf-8 -*-

# Main function
import ReverseBoard
import Player
import ReverseCommon
import Game
import datetime

if __name__ == "__main__":
    # 勝利数
    black_win = 0
    white_win = 0

    # 試行回数
    # times = 1
    times = 10

    # 盤面を出力するか
    # output = True
    output = False

    print "start:", datetime.datetime.today()

    # 勝負
    for i in range(0, times):

        # 盤面作成
        reverse_board = ReverseBoard.ReverseBoard()

        # プレイヤー
        # black_player = Player.NextStoneMaxAi(ReverseCommon.BLACK)
        black_player = Player.MC(ReverseCommon.BLACK)
        white_player = Player.RandomAi(ReverseCommon.WHITE)

        # ゲーム開始
        game = Game.Game(black_player, white_player, reverse_board)
        game.play(output)

        # 勝者判定
        if game.get_winner() == black_player:
            black_win += 1
        else:
            white_win += 1

    print "end", datetime.datetime.today()

    # 各AIの勝利数
    print "black:", black_win, ", white:", white_win
