from heuristics import *
import time
import copy
import numpy as np

IMPOSSIBLE = -999999
MOVE_OPTS = 4096

def sortMoves(board:chess.Board, validMoves):
    result = []
    for move in validMoves:
        if move.to_square != None:
            result.insert(0, move)
        else:
            result.append(move)
    return result

class ManualPlayer:
    def __init__(self) -> None:
        pass

# this should be simple enough, just calls the stockfish ai and gets the best move. Can mess with parameters to make it stupider :)
class StockfishAI:
    def __init__(self, stockfish) -> None:
        self.stockfish = stockfish
        pass
    
    def findMove(self, board) -> chess.Move:
        result = self.stockfish.get_best_move()
        result = chess.Move.from_uci(result)
        return result
    
# This is an alpha-beta pruning (a faster but just as effective min-max) ai, that will make the best move given how it sees the board heuristic
class ABPlayer():
    def __init__(self, max_depth):
        # max_depth -> how far in the future does it need to look (exponentially expensive)
        self.max_depth = max_depth
        # heuristic -> what heuristic it should use to calculate the board score, taken from heuristics.py
        self.heuristic = greedyHeuristic
            
    # alphaBeta pruning algorithm (just makeMove, see state, undoMove, see what works best, pretty simple)
    def alphaBeta(self, board: chess.Board, depth, alpha, beta):
        if board.is_game_over() != False or depth == 0:
            return (None, self.heuristic(board))
        validMoves = list(board.legal_moves)
        validMoves = sortMoves(board, validMoves)
        if board.turn == chess.WHITE:
            bestVal = (None, -math.inf)
            for child in validMoves:
                board.push(child)
                v = self.alphaBeta(board, depth-1, alpha, beta)
                if child != board.pop():
                    print("all hell has broke lose")
                if v[1] > bestVal[1]:
                    bestVal = (child, v[1])
                alpha = max(alpha, bestVal[1])
                if beta <= alpha:
                    break
            return bestVal
        else:
            bestVal = (None, math.inf)
            for child in validMoves:
                board.push(child)
                v = self.alphaBeta(board, depth-1, alpha, beta)
                if child != board.pop():
                    print("all hell has broke lose")
                if v[1] < bestVal[1]:
                    bestVal = (child, v[1])
                beta = min(beta, bestVal[1])
                if beta <= alpha:
                    break
            return bestVal
            
    def findMove(self, currentBoard: chess.Board) -> chess.Move:
        board = copy.deepcopy(currentBoard)
        print(self.heuristic(board))
        move, score = self.alphaBeta(board, self.max_depth, -math.inf, math.inf)
        print(score)
        return move
    
class BasicModel:
    
    def __init__(self, temperature=0):
        
        #keys are state, values is 4096
        self.moves_dict = {}
        self.move_opts = MOVE_OPTS
        self.current_trace = []
        self.learning_rate = 1
        self.gamma = 0.5
        self.ending_multiplier = 20
        self.temperature = 0
        
    
    def findMove(self, state):
        """
        Returns a 4-tuple representing the move, given the state
        """
        if self.current_trace[-1][0] == state:
            self.moves_dict[state][self.current_trace[-1][1]] = IMPOSSIBLE
            
        if state in self.moves_dict:
            
            if np.random.rand() >= self.temperature:
                maximum = max(self.moves_dict[state])
                if maximum == 0:
                    zeros = [i for i in range(self.move_opts) if self.moves_dict[state][i] == 0]
                    index_choice = zeros[int(np.random.rand()*len(zeros))]
                else:
                    index_choice = list(self.moves_dict[state]).index(maximum)
            else:
                positives = [i for i in range(self.move_opts) if self.moves_dict[state][i] >= 0]
                index_choice = positives[int(np.random.rand()*len(positives))]
            
        else:
            
            self.moves_dict = np.zeros(self.move_opts)
            index_choice = int(np.random.rand()*self.move_opts)
        
        move = self.convert_to_move(index_choice)
        self.current_trace += [(state, index_choice)]
        
        return move
    
    def convert_to_move(self, move_num):
        """
        Returns a tuple of 4 nums:
        0,1 - the x and y of the piece to move
        2,3 - the x and y of the location to go
        """
        if self.move_opts == MOVE_OPTS:
            val = []
            for x in range(4):
                val += [int(move_num/pow(8,3-x))%8]
            return tuple(val)
        return (0,0,0,0)
    
    def update_with_game_result(self, result):
        """
        Refreshes the trace and updates Q-Table
        """
        last_state, last_move = self.current_trace[-1]
        self.moves_dict[state][move] = (1-self.learning_rate)*self.moves_dict[state][move] + self.learning_rate*(result*self.ending_multiplier)
        for i, state, move in enumerate(self.current_trace[-2::-1]):
            next_max = max(self.moves_dict[self.current_trace[i+1][0]])
            self.moves_dict[state][move] = (1-self.learning_rate)*self.moves_dict[state][move] + self.learning_rate*(result + self.gamma*next_max)
        self.current_trace = []
        
    def end_training(self, file_name):
        pass
        
    def get_related_moves(self, moves):
        pass