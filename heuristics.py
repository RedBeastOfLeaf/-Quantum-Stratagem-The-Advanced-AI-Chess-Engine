# from board import *
import math
import chess

pawnVal = 1
knightVal = 3
bishopVal = 3
rookVal = 5
queenVal = 9

def greedyHeuristic(board: chess.Board):
    result = 0
    if board.is_game_over() == True and board.outcome().winner == chess.WHITE:
        return 10000
    if board.is_game_over() == True and board.outcome().winner == chess.BLACK:
        return 10000
    numPieces = 64
    for i in range(0, 8):
        for j in range(0, 8):
            piece = board.piece_at(chess.square(i, j))
            if piece == None:
                numPieces -= 1
                continue
            piece = piece.symbol()
            if piece == "p":
                result -= pawnVal
            elif piece == "r":
                result -= rookVal
            elif piece == "n":
                result -= knightVal
            elif piece == "b":
                result -= bishopVal
            elif piece == "q":
                result -= queenVal
            elif piece == "P":
                result += pawnVal
            elif piece == "R":
                result += rookVal
            elif piece == "N":
                result += knightVal 
            elif piece == "B":
                result += bishopVal
            elif piece == "Q":
                result += queenVal
    return result
            