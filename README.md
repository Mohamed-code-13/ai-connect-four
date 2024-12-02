# Connect Four

This repository contains a project developed for the (CSE351) Introduction to Artificial Intelligence course. The goal is to implement a Connect Four game with an AI agent powered by Minimax and its variations.

## Game Description

Connect Four is a two-player game where players alternate dropping coloured discs into a vertical grid. The objective is to align four of their discs vertically, horizontally, or diagonally. The game ends when the board is full, and the player with more connected fours is the winner.

## Features

- **Human vs. Computer mode**: Play against an AI agent.
- **Artificial Intelligence Algorithms**:
  - Minimax without alpha-beta pruning.
  - Minimax with alpha-beta pruning.
  - Expected Minimax: Includes probabilistic moves for disc placement.
- **Minimax Tree Visualization**:
  - The Minimax tree is displayed with every computer move.
- **Heuristic Pruning**:
  - A custom heuristic function evaluates game states, truncating the game tree after K levels.
  - Adjustable K parameter at game start.
  - The heuristic function considers various factors like scores and potential points for each player.
  - The heuristic function prioritises states where the computer is closer to winning and penalize those favoring the human.

## Deliverables

1. **Code**:
   - Well-commented source code in Python.
2. **Report**:
   - Sample runs with corresponding Minimax trees.
   - Performance comparisons between algorithms (e.g., time and nodes expanded for different K values).
   - Descriptions of data structures, algorithms, assumptions, and any additional work.

## Getting Started

### Prerequisites

- Python3.
- PyQt5 library for GUI and AI.

### Running the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/mosheriif/ai-connect-four.git
   ```
2. Run the code: Ensure you have Python installed and execute the following to start the program.
   ```bash
   main.py
   ```

## Heuristic Evaluation

The heuristic is evaluated at the terminal nodes, which are either those where the depth reaches K, or when a final state is reached (game end). It is evaluated for both players, the computer and the human, where Player One is assumed to always be the Human, and Player Two is assumed to be the Computer, and the difference between them is calculated. If the current node is a maximising node, then the difference is left as is, otherwise, the evaluated difference is multiplied by -1.

The heuristic function works by prioritising states where the computer is closer to winning searching, such that there are four possible consecutive slots, where there are Computer tiles and/or empty slots. A four-slot window is considered invalid, if it contains Human tiles.

Four consecutive Computer tiles are given a 100,000 score, one empty tile and three Computer tiles are given a score of 1,000, two Computer tiles are given a score of 500, and one Computer tile is given a score of 10. These values were set through trial and error.

Assuming the Computer is the starting player, it usually starts at the center, even though it was not explicitly stated. This is due to the fact that the position with the highest possible fours is the center position, thus having the highest score.