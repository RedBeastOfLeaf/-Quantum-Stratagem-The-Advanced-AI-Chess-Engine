import chess, random
from models import BasicModel, StockfishModel, load_existing_model
from stockfish import Stockfish

sf = '/opt/homebrew/Cellar/stockfish/16/bin/stockfish'

#Supercomputer oficial path
# sf = '/N/u/tspugh/Quartz/Chess-Bot/stockfish/stockfish_14_x64_avx2'

class Environment:
    
    def __init__(self, filename=None, new_run=False, use_model=None) -> None:
        self.stockfish = Stockfish(path=sf)
        # self.player1 = ABPlayer(5)
        self.filename = filename
        if filename==None or new_run==True:
            self.player1 = BasicModel(0.01) if use_model==None else use_model
            if filename==None:
                self.filename = 'default_model.p'
        else:
            self.player1 = load_existing_model(filename)
        self.player2 = StockfishModel(self.stockfish)


        self.game_finished = False
        self.winner = None
        
    def makeNextMove(self, state : chess.Board, whitePlayer, blackPlayer, stockfish: Stockfish):
        if state.turn == chess.BLACK:
            move = blackPlayer.get_my_move(state, list(state.legal_moves))
            if move == None:
                self.game_finished = True
                self.winner = state.outcome().winner
                return
        elif state.turn == chess.WHITE:
            move = whitePlayer.get_my_move(state, list(state.legal_moves))
            if move == None:
                self.game_finished = True
                self.winner = state.outcome().winner
                return
        state.push(move)
        stockfish.make_moves_from_current_position([move.uci()])
            
            
    def run(self, numIterations):
        stockfishWins = 0
        modelWins = 0
        ties = 0

        whitePlayer = self.player1
        blackPlayer = self.player2

        for i in range(numIterations):
            print(f"Iteration {i+1}")
            self.stockfish = Stockfish(path=sf)
            self.player2 = StockfishModel(self.stockfish)
            game_random = random.randint(0, 1)
            if game_random == 1:
                whitePlayer = self.player2
                blackPlayer = self.player1
            else:
                whitePlayer = self.player1
                blackPlayer = self.player2

            state = chess.Board()
            while state.is_game_over() == False:
                self.makeNextMove(state, whitePlayer, blackPlayer, self.stockfish)
                #print(self.stockfish.get_board_visual())

            game_outcome = 0
            self.winner = state.outcome().winner
            if self.winner == None:
                ties += 1
            elif self.winner == chess.WHITE and game_random==1:
                stockfishWins += 1
                game_outcome = -1
            elif self.winner == chess.WHITE:
                modelWins += 1
                game_outcome = 1
            elif game_random == 1:
                modelWins += 1
                game_outcome = 1
            else:
                stockfishWins += 1
                game_outcome = -1
            self.player1.update_with_game_result(game_outcome, 'stockfish')

        self.player1.end_training(self.filename)
        return [stockfishWins, modelWins, ties]