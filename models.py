#!/usr/bin/env python
# coding: utf-8


import numpy as np
import sklearn
import igraph as ig
import pickle
import chess
from ai import StockfishAI
import random


IMPOSSIBLE = -999999
MOVE_OPTS = 4096

def load_existing_model(file_name):
    file_opened = open(file_name, 'rb')
    model = pickle.load(file_opened)
    file_opened.close()
    return model

class BasicModel:
    
    def __init__(self, temperature=0):
        
        #keys are state, values is 4096
        self.moves_dict = {}
        self.move_opts = MOVE_OPTS
        self.current_trace = []
        self.learning_rate = 0.8
        self.gamma = 0.5
        self.ending_multiplier = 20
        self.success_log = []
        self.temperature = temperature

    def has_state(self, state):
	    return state in self.moves_dict
    
    def get_my_move(self, state, possible_moves):
        """
        Returns a chess.move representing the move, given the state
        """

        state = state.fen()
            
        if state in self.moves_dict:
            
            if np.random.rand() >= self.temperature:
                maximum = max(np.array(self.moves_dict[state])[:,0])
                if maximum == 0:
                    zeros = [i for i in range(len(self.moves_dict[state])) if self.moves_dict[state][i][0] == 0]
                    try:
                        index_choice = random.choice(zeros)
                    except:
                        index_choice = int(np.random.rand()*len(possible_moves))
                else:
                    index_choice = list(np.array(self.moves_dict[state])[:,0]).index(maximum)
            else:
                positives = [i for i in range(len(self.moves_dict[state])) if self.moves_dict[state][i][0] >= 0]
                if len(positives) > 0:
                    index_choice = random.choice(positives)
                else:
                    index_choice = int(np.random.rand()*len(possible_moves))

            
        else:
            self.moves_dict[state] = []
            if possible_moves is not None and len(possible_moves) > 0:
                for mv in possible_moves:
                    self.moves_dict[state] += [[0, mv]]
            else:
                return None
            index_choice = int(np.random.rand()*len(possible_moves))
        if len(self.moves_dict[state]) > 0:
            move = self.moves_dict[state][index_choice][1]
        else:
            move = None
        self.current_trace += [(state, index_choice)]
        return move

    
    def update_with_game_result(self, result, competitor='unknown'):
        """
        Refreshes the trace and updates Q-Table
        """
        print(result)
        last_state, last_move = self.current_trace[-1]
        self.moves_dict[last_state][last_move][0] = (1-self.learning_rate)*self.moves_dict[last_state][last_move][0] + self.learning_rate*(result*self.ending_multiplier)
        for i, pair in enumerate(self.current_trace[-2::-1]):
            state, move = pair
            next_max = max(np.array(self.moves_dict[self.current_trace[i+1][0]])[:,0])
            self.moves_dict[state][move][0] = (1-self.learning_rate)*self.moves_dict[state][move][0] + self.learning_rate*(result + self.gamma*next_max)

        experience_metric = self.get_experience_metric()
        game_result = GameResult(result, len(self.current_trace),  experience_metric, competitor)
        self.success_log += [game_result]
        self.current_trace = []
        
    def end_training(self, file_name):
        file_opened = open(file_name, 'wb')
        pickle.dump(self, file_opened, protocol=pickle.HIGHEST_PROTOCOL)
        file_opened.close()

    #to be considered with k-means
    def get_related_moves(self, moves):
        pass

    def get_experience_metric(self):
        count = 0
        for key,  value in self.moves_dict.items():
            count += len([x for x in value if x[0] >= 0])
        return count

class StockfishModel(BasicModel):
    def __init__(self, stockfish):
        self.stockfish = stockfish
        self.model = StockfishAI(stockfish)

    def has_state(self, state):
        return None

    def get_my_move(self, state, possible_moves):
        return self.model.findMove(state)

    def update_with_game_result(self, result, competitor='unknown'):
        return None

    def end_training(self, file_name):
        pass

    # to be considered with k-means
    def get_related_moves(self, moves):
        pass

    def get_experience_metric(self):
        pass

class GameResult:

    def __init__(self, result, moves, experience=0, competitor='unknown'):
        """

        :param result: 1 if a win, -1 if a loss, 0 if a tie
        :param moves: How many moves the game lasted for (that BaseMovel played)
        :param experience: A metric of experience
        :param competitor: The string representation of the model competitor
        """
        self.result = result
        self.moves = moves
        self.experience = experience
        self.competitor = competitor
