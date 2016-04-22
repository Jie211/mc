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
    times = 1
    # times = 100 

    # 盤面を出力するか
    output = True
    # output = False

    print ("start:" + str(datetime.datetime.today()))

    # 勝負
    for i in range(0, times):
    # for i in [None]*times:

        # 盤面作成
        reverse_board = ReverseBoard.ReverseBoard()

        # プレイヤー
        # black_player = Player.NextStoneMaxAi(ReverseCommon.BLACK)
        # black_player = Player.Less_chance(ReverseCommon.BLACK)
        # black_player = Player.Less_chance(ReverseCommon.BLACK)
        black_player = Player.MC(ReverseCommon.BLACK)
        # white_player = Player.RandomAi(ReverseCommon.WHITE)
        # white_player = Player.Probability_select(ReverseCommon.WHITE)
        # white_player = Player.MC(ReverseCommon.WHITE)
        white_player = Player.Less_chance(ReverseCommon.WHITE)

        # ゲーム開始
        game = Game.Game(black_player, white_player, reverse_board)
        game.play(output)

        # 勝者判定
        if game.get_winner() == black_player:
            black_win += 1
        else:
            white_win += 1

        print ("black_win = "+str(black_win)+" white_win = "+str(white_win))

    print ("end"+ str(datetime.datetime.today()))

    # 各AIの勝利数
    print ("black:"+ str(black_win) + ", white:"+str( white_win))
