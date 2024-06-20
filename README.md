# Quantum Stratagem: The Advanced AI Chess Engine

# Chess AI and Simulation Framework

## Introduction

This project provides a robust framework for chess AI and game simulation, integrating various machine learning techniques and AI algorithms to analyze and play chess at different levels of proficiency. The framework is built in Python and includes integration with the Stockfish engine for high-level move analysis and the Pygame library for graphical representations.

## Features

- **Multiple AI Models:** Supports different types of AI models for diverse strategies and analysis depth.
- **Stockfish Integration:** Leverages the powerful Stockfish engine for move generation and evaluation.
- **Graphical Interface:** Utilizes Pygame for interactive game visualizations, making it suitable for real-time analysis and demonstration.
- **Customizable Parameters:** Allows easy adjustments of AI behavior through changeable parameters like depth of search and learning rates.

## Win Rate Visualization

To visualize the performance of the chess AI models, the win rate is graphically represented below. This provides a clear snapshot of the AI's effectiveness in simulated matches.

![Win Rate: 33%](path_to_your_image.png)



## AI Models

### 1. Alpha-Beta Pruning AI (`ABPlayer`)
- Implements alpha-beta pruning to optimize the minimax algorithm, reducing the number of nodes evaluated in the decision tree.
- Utilizes a heuristic function to evaluate non-terminal board states, significantly enhancing move decision efficiency.

### 2. Neural MoveMap Heuristic (`NeuralMoveMap`)
- Employs a neural network to predict the best move based on the current board state.
- Trained on numerous simulated games to refine its move predictions under various scenarios.

### 3. K-Nearest Neighbors (KNN) Approach
- Uses a simple yet effective KNN algorithm to decide moves based on historical game data.
- Compares current game situations with past games to find the most successful outcomes.

## Simulation Environment

- **Chess Board Management:** Handles all aspects of chess board setup, move validation, and game state updates.
- **Game Simulation:** Simulates games between different AI models or an AI and a human player, providing insights into AI performance and strategy development.
- **Result Tracking:** Collects and analyzes results from simulations to adjust strategies and improve model performance.

  

## Getting Started

To get started with this project, clone the repository and ensure you have Python installed. You'll also need to install dependencies listed in `requirements.txt` and then to run a simulation:

```bash
python game.py



