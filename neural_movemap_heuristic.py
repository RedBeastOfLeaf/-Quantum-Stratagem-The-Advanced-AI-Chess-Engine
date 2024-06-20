import chess
import tensorflow as tf
import numpy as np
from environment import Environment
import pickle
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import HeNormal
from tensorflow.keras import layers, models

# Define neural network architecture with complex hidden layers
model = models.Sequential([
    layers.Input(shape=(64 * 6 + 1,)),
    layers.Dense(4096, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(2048, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(1024, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(512, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(256, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(128, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(64, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(32, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(16, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(8, activation='relu', kernel_initializer=HeNormal()),
    layers.Dense(1, activation='linear')
])

# Define the Adam optimizer with a learning rate (you can adjust it)
adam = Adam(learning_rate=0.01)  # Adjust the learning rate

# Compile the model with the Adam optimizer
model.compile(optimizer=adam, loss='mean_squared_error', metrics=['accuracy'])  # Use 'mean_squared_error' loss

# Function to convert the board state into the input format expected by the neural network
def convert_board_to_input(board):
    input_data = np.zeros((1, 64 * 6 + 1))
    for i in range(64):
        piece = board.piece_at(i)
        if piece is not None:
            input_data[0, i * 6 + piece_color(piece)] = 1
    input_data[0, -1] = side_to_move(board)
    return input_data

# Helper function to determine the color of a chess piece
def piece_color(piece):
    if piece.color == chess.WHITE:
        return 1
    elif piece.color == chess.BLACK:
        return -1
    else:
        return 0

# Helper function to determine the side to move
def side_to_move(board):
    return 1 if board.turn == chess.WHITE else -1

# Function to select the best move based on move likelihoods
def select_best_move(board, move_likelihoods):
    legal_moves = list(board.legal_moves)
    move_scores = {}
    for i, move in enumerate(legal_moves):
        move_scores[move] = move_likelihoods[0, i]
    best_move = max(move_scores, key=move_scores.get)
    return best_move

def train_neural_network(num_epochs=100, games_per_epoch=10):
    # Initialize success_logs to store game outcomes with game lengths, results, wins, and losses
    success_logs = []

    # Initialize the environment
    environment = Environment('neural_network_model.keras', new_run=True)

    for epoch in range(num_epochs):
        epoch_logs = []

        for _ in range(games_per_epoch):
            epoch_logs += environment.run(1)  # Log success data

        # Training within the epoch
        X = []
        Y = []
        for outcome in epoch_logs:
            if isinstance(outcome, tuple):
                board, game_outcome = outcome
                X.append(convert_board_to_input(board))
                Y.append(np.array([game_outcome]))

        if len(X) > 0 and len(Y) > 0:
            X = np.array(X)
            Y = np.array(Y)
            model.fit(X, Y, epochs=100, verbose=0)  # Run multiple epochs

        # Append epoch data to the overall success_logs
        success_logs += epoch_logs

    # Save the neural network and success_logs with game lengths, results, wins, and losses
    data = {
        'model': model,
        'success_logs': success_logs
    }
    try:
        with open('trained_model_and_logs.p', 'wb') as file:
            pickle.dump(data, file)
    except FileNotFoundError:
        print("Error: Could not open file 'trained_model_and_logs.p'.")


# Train the neural network with the updated model architecture
train_neural_network()
