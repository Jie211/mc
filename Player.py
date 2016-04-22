#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import operator

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
            # if score in score_candidates_map:
                score_candidates_map[score] = []

            score_candidates_map[score].append(candidates);

        max_score = max(score_candidates_map)
        max_score_candidates = score_candidates_map[max_score]
        return max_score_candidates[random.randint(0, len(max_score_candidates) - 1)]

class Probability_select(Player):
    
    def other_color(self):
        if self._color == True:
            return  False
        else:
            return  True
    def most_score(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1
        score_candidates_map = {}
        for candidates in all_candidates:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            score = ReverseCommon.get_score(next_board, self._color)
            if not score_candidates_map.has_key(score):
            # if score in score_candidates_map:
                score_candidates_map[score]=[]
            score_candidates_map[score].append(candidates)
        
        max_score = max(score_candidates_map)
        max_score_candidates = score_candidates_map[max_score]
        return max_score_candidates[random.randint(0, len(max_score_candidates)-1)]

    def check_end(self, board, score, candidate):
        if ReverseCommon.is_game_set(board):
            if self.who_win(board) == 1:
                score[str(candidate)][0] +=1
                return True
            else:
                return True
        else:
            return False

    def less_ai(self, board):
        pc_color = self.other_color()
        me_color = self._color

        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1
        chance_candidates_map={}
        for candidates in all_candidates:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            enemy_candidates = ReverseCommon.get_puttable_points(next_board, pc_color)
            if len(enemy_candidates) == 0:
                return candidates

            get_chance = len(enemy_candidates)
            if not chance_candidates_map.has_key(get_chance):
            # if get_chance in chance_candidates_map:
                chance_candidates_map[get_chance]=[]
            chance_candidates_map[get_chance].append(candidates)

        min_chance = min(chance_candidates_map)
        min_chance_candidates = chance_candidates_map[min_chance]
        return min_chance_candidates[0]

    def max_ai(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1

        if random.randint(1, 100) <= 0:
            index = random.randint(0, len(all_candidates) - 1)
            return all_candidates[index]

        score_candidates_map = {}
        for candidates in all_candidates:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            score = ReverseCommon.get_score(next_board, self._color)

            if not score_candidates_map.has_key(score):
            # if score in score_candidates_map:
                score_candidates_map[score] = []

            score_candidates_map[score].append(candidates);

        max_score = max(score_candidates_map)
        max_score_candidates = score_candidates_map[max_score]
        return max_score_candidates[random.randint(0, len(max_score_candidates) - 1)]

    def rand_ai(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1
        else:
            # ランダムで次の手を選ぶ
           index = random.randint(0, len(all_candidates) - 1)
           return all_candidates[index]

    def choose(self, candidates, probabilities):
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

    def get_plan(self):
        return self.choose([1, 2, 3], [0.7, 0.2, 0.1])
    def next_move(self, board):
        plan = self.get_plan()
        if plan == 1:
            return self.rand_ai(board)
        elif plan == 2:
            return self.max_ai(board)
        elif plan == 3:
            return self.less_ai(board)



class Less_chance(Player):
    def other_color(self):
        if self._color == True:
            return  False
        else:
            return  True
    def most_score(self, board):
        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1
        score_candidates_map = {}
        for candidates in all_candidates:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            score = ReverseCommon.get_score(next_board, self._color)
            if not score_candidates_map.has_key(score):
            # if score in score_candidates_map:
                score_candidates_map[score]=[]
            score_candidates_map[score].append(candidates)
        
        max_score = max(score_candidates_map)
        max_score_candidates = score_candidates_map[max_score]
        return max_score_candidates[random.randint(0, len(max_score_candidates)-1)]

    def check_end(self, board, score, candidate):
        if ReverseCommon.is_game_set(board):
            if self.who_win(board) == 1:
                score[str(candidate)][0] +=1
                return True
            else:
                return True
        else:
            return False

    def next_move(self, board):
        pc_color = self.other_color()
        me_color = self._color

        all_candidates = ReverseCommon.get_puttable_points(board, self._color)
        if len(all_candidates) == 0:
            return -1
        chance_candidates_map={}
        for candidates in all_candidates:
            next_board = ReverseCommon.put_stone(board, self._color, candidates[0], candidates[1])
            enemy_candidates = ReverseCommon.get_puttable_points(next_board, pc_color)
            if len(enemy_candidates) == 0:
                return candidates

            get_chance = len(enemy_candidates)
            if not chance_candidates_map.has_key(get_chance):
            # if get_chance in chance_candidates_map:
                chance_candidates_map[get_chance]=[]
            chance_candidates_map[get_chance].append(candidates)

        min_chance = min(chance_candidates_map)
        min_chance_candidates = chance_candidates_map[min_chance]
        print str(me_color)+" Less "+str(min_chance_candidates[0])
        return min_chance_candidates[0]

            



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

    def check_end(self, board, score, candidate):
        if ReverseCommon.is_game_set(board):
            if self.who_win(board) == 1:
                map_index = candidate[0]*10+candidate[1]
                score[map_index] +=1
                # score[str(candidate)][0] +=1
                return True
            else:
                return True
        else:
            return False

    def next_move(self, board):
        score_map = {}
        me_color = self._color
        pc_color = self.other_color()

        main_candidates = ReverseCommon.get_puttable_points(board, me_color)
        if len(main_candidates) == 0:
            return -1

        for this_candidate in main_candidates:
            this_board = ReverseCommon.put_stone(board, me_color, this_candidate[0], this_candidate[1])

            # score_map[str(this_candidate)] = [0,this_candidate]
            map_index=this_candidate[0]*10+this_candidate[1]
            score_map[map_index] = 0

            for i in range(50):
                # loop_board = copy.deepcopy(this_board)
                loop_board = this_board[:]
                # loop_board2 = ReverseCommon.Copy(this_board, use_deepcopy=False)
                # if loop_board != loop_board2:
                  # print "!!!!!!!!!!!!"
                # else:
                  # print id(loop_board)
                  # print id(loop_board2)
                # sys.exit()
                while True:
                    if self.check_end(loop_board, score_map, this_candidate):
                        break
                    enemy_candidates = self.next_rand(pc_color, loop_board)
                    if enemy_candidates == -1:
                        pass
                    else:
                        loop_board = ReverseCommon.put_stone(loop_board, pc_color, enemy_candidates[0], enemy_candidates[1])
                        if self.check_end(loop_board, score_map, this_candidate):
                            break
                    me_candidates = self.next_rand(me_color, loop_board)
                    if me_candidates == -1:
                        pass
                    else:
                        loop_board = ReverseCommon.put_stone(loop_board, me_color, me_candidates[0], me_candidates[1])
        get_max =  max(score_map.iteritems(), key=operator.itemgetter(1))[0]
        ans = [get_max/10, get_max%10]
        print main_candidates
        print score_map
        print str(me_color)+" MC "+str(ans)
        return ans



