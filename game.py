# from board import *
from ai import *
from pygameHelper import *
from time import sleep
from threading import Thread

from stockfish import Stockfish
stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe")

# * You can basically ignore most of  this file as it just mainly just does the gui. It does also have the logic for making valid moves however.

# board -> the current board, initialized how chess boards are
# board = Board()
board = chess.Board()

# reverse -> if the visual of the board is White's perspective or not
whitePerspective = True
clicked = False
# move -> the current move selected
move = None
# running -> whether pygame is running or not
running = True

# The bot that is playing for white and for black respectively. Called from the ai.py file
# whitePlayer = ManualPlayer()
whitePlayer = ABPlayer(5)
blackPlayer = StockfishAI(stockfish)

# The rest of this is all visual pygame stuff you can ignore :)
def tryMakeMove():
    global running, clicked, move, whitePlayer, blackPlayer
    while running and board.is_game_over() == False:
        if board.turn == chess.BLACK and not isinstance(blackPlayer, ManualPlayer):
            print("black player making move...")
            move = blackPlayer.findMove(board)
            if move == None:
                print("White Wins")
                return
            board.push(move)
            stockfish.make_moves_from_current_position([move.uci()])
            print(stockfish.get_board_visual())
        if board.turn == chess.WHITE and not isinstance(whitePlayer, ManualPlayer):
            print("white player making move...")
            move = whitePlayer.findMove(board)
            if move == None:
                print("Black Wins")
                return
            print(move)
            board.push(move)
            stockfish.make_moves_from_current_position([move.uci()])
            print(stockfish.get_board_visual())

Thread(target=tryMakeMove).start()
while doPygame and running and board.is_game_over() == False:
    showBoard(whitePerspective, board)
    showPieces(whitePerspective, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if board.is_game_over() == False and ((board.turn == chess.WHITE and isinstance(whitePlayer, ManualPlayer)) or (board.turn == chess.BLACK and isinstance(blackPlayer, ManualPlayer))):
            if not clicked and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
                changed = False
                posX = event.pos[0]
                posY = event.pos[1]
                boardX = 7 - (posX-offsetX) // size
                boardY = 7 - (posY-offsetY) // size
                realBoardX = boardX
                realBoardY = boardY
                if not whitePerspective:
                    realBoardX = 7-boardX
                    realBoardY = 7-boardY
                if not whitePerspective:
                    realBoardX = 7-boardX
                    realBoardY = 7-boardY
                curMove = chess.Move.from_uci(boardToFide(graphic.selected[0], graphic.selected[1], realBoardX, realBoardY))
                # if graphic.selected == None or [realBoardX, realBoardY] not in board.validMove(graphic.selected[0], graphic.selected[1]):
                if graphic.selected == None or board.is_valid(curMove):
                    if (boardX < 0 or boardX > 7) or (boardY < 0 or boardY > 7):
                        graphic.selected = None
                        changed = True
                    elif not graphic.selected == None:
                        if not whitePerspective and 7-graphic.selected[0] == boardX and 7-graphic.selected[1] == boardY:
                            graphic.selected = None
                            changed = True
                        elif whitePerspective and graphic.selected[0] == boardX and graphic.selected[1] == boardY:
                            graphic.selected = None
                            changed = True
                    if not changed:
                        if not whitePerspective:
                            graphic.selected = (7-boardX, 7-boardY)                    
                        else:
                            graphic.selected = (boardX, boardY)
                # elif [realBoardX, realBoardY] in board.validMove(graphic.selected[0], graphic.selected[1]):
                elif board.is_valid(curMove):
                    makingTurn = False
                    board.push(curMove)
                    # move = boardToFide(graphic.selected[0], graphic.selected[1], realBoardX, realBoardY)
                    # board.makeMove(graphic.selected[0], graphic.selected[1], realBoardX, realBoardY)
                    stockfish.make_moves_from_current_position([curMove.uci()])
                    graphic.selected = None
            elif event.type != pygame.MOUSEBUTTONDOWN:
                clicked = False
                    
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60
pygame.quit()
