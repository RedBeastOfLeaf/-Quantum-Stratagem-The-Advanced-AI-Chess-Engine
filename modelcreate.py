import chess
import chess.engine
import pickle
from heuristics import greedyHeuristic

def train_basic_model():
    # Create an empty chess board
    board = chess.Board()
    
    # List to store training data
    training_data = []

    # Number of games to play and collect data from
    num_games = 1000

    for _ in range(num_games):
        board = chess.Board()
        game_data = []

        while not board.is_game_over():
            # Use your heuristic function to determine the best move
            move = select_best_move(board)
            
            # Push the move to the board
            board.push(move)
            
            # Append the current board position and evaluation to the game data
            game_data.append((board.fen(), evaluate_position(board)))

        # Append the game data to the training data
        training_data.append(game_data)

    # Save the training data to a pickle file
    with open("training_data.p", "wb") as file:
        pickle.dump(training_data, file)

def select_best_move(board):
    # Replace this with your logic to select the best move using the heuristic
    # For example, you can use a simple minimax search or other methods
    # The example below returns the first legal move for demonstration purposes
    return list(board.legal_moves)[0]

def evaluate_position(board):
    # Use your heuristic function to evaluate the board position
    return greedyHeuristic(board)

if __name__ == "__main__":
    train_basic_model()
