#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import copy
import random
import ReverseCommon
import ReverseBoard
import Game


class Player:
    """ プレーヤの基盤クラス(AIも含む) """

    def __init__(self, color):
        """ コンストラクタ """
        self._color = color

    def next_move(self, board):
        """ 次の手を返す """
        pass

    @property
    def color(self):
        """ 自分の色を返す """
        return self._color


class RandomAi(Player):
    """ランダムで石を置くAI"""

    def next_move(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1
        else:
        # ランダムで次の手を選ぶ
           index = random.randint(0, len(all_candidates) - 1)
           return all_candidates[index]


class NextStoneMaxAi(Player):
    """確率によって今回の１手で最も石が取れる場所に置くAI"""

    def next_move(self, board):
        # 石を置ける全候補地
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1

        if random.randint(1, 100) <= 0:
            index = random.randint(0, len(all_candidates) - 1)
            return all_candidates[index]

        # 今回の一手で最も石が取れる場所一覧
        score_candidates_map = {}
        for candidates in all_candidates:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            score = ReverseCommon.get_score(next_board, self._color)

            if not score_candidates_map.has_key(score):
                score_candidates_map[score] = []

            score_candidates_map[score].append(candidates);

        max_score = max(score_candidates_map)
        max_score_candidates = score_candidates_map[max_score]
        return max_score_candidates[random.randint(0, len(max_score_candidates) - 1)]

class MC(Player):
    def next_rand(self, color, board):
        all_candidates = ReverseCommon.get_puttable_points(board, color)
        if len(all_candidates) == 0:
            return -1
        else:
            index = random.randint(0, len(all_candidates) - 1)
            return all_candidates[index]

    def other_color(self):
        if self._color == True:
            return  False
        else:
            return  True

    def who_win(self, board):
        if self._color == True:
            pc_color = False
        else:
            pc_color = True
        s_me = ReverseCommon.get_score(board, self._color)
        s_pc = ReverseCommon.get_score(board, pc_color)
        
        if s_me > s_pc:
            return 1
        else:
            return 0

    def next_move(self, board):
        
        score_map={}
        me_color=self._color
        pc_color=self.other_color()
        lock=False

        for i in xrange(50):
            next_board=copy.deepcopy(board)
            while True:
                me_candidates = self.next_rand(me_color, next_board)
                if lock == False:
                    save_candidates=copy.deepcopy(me_candidates)
                    lock=True
                if me_candidates != -1:
                    next_board = ReverseCommon.put_stone(next_board, me_color, me_candidates[0], me_candidates[1])
                    # ReverseCommon.print_board(next_board)
                    if ReverseCommon.is_game_set(next_board):
                        if self.who_win(next_board) == 1:
                            if not score_map.has_key(str(save_candidates)):
                                score_map[str(save_candidates)]=[1,save_candidates]
                                lock=False
                                break
                            else:
                                score_map[str(save_candidates)][0]+=1
                                lock=False
                                break
                        else:
                            lock=False
                            break
                else:
                    pass
                    # print "pass"

                enemy_candidates = self.next_rand(pc_color, next_board)
                if enemy_candidates != -1:
                    next_board = ReverseCommon.put_stone(next_board, pc_color, enemy_candidates[0], enemy_candidates[1])
                    # ReverseCommon.print_board(next_board)
                    if ReverseCommon.is_game_set(next_board):
                        if self.who_win(next_board) == 1:
                            if not score_map.has_key(str(save_candidates)):
                                score_map[str(save_candidates)]=[1,save_candidates]
                                lock=False
                                break
                            else:
                                score_map[str(save_candidates)][0]+=1
                                lock=False
                                break
                        else:
                            lock=False
                            break
                else:
                    pass
                    # print "pass"

        # print score_map
        # print max(score_map.values())
        # print type(max(score_map, key=(lambda x: score_map[x])))
        # print score_map
        # sys.exit()
        # return list(max(score_map, key=(lambda x: score_map[x])))
        # print max(score_map.values()[0])
        # print score_map
        if len(score_map)== 0:
            return self.next_rand(me_color, board)
        else:
            return max(score_map.values()[0])
