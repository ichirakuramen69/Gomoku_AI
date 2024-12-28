# Gomoku Game

Gomoku is a strategic board game where two players take turns placing their pieces on a grid. The first player to align 5 of their pieces in a row, column, or diagonal wins. This project is a Python-based implementation of the Gomoku game, featuring a human player versus an AI opponent.

## Features

- **Interactive Gameplay**: Play against an AI opponent in a visually rendered grid.
- **AI Intelligence**: The AI uses the MiniMax algorithm with alpha-beta pruning for strategic decision-making.
- **Dynamic Visualization**: The game board is rendered using the Pygame library with responsive graphics.
- **Win Detection**: Detects winning sequences of 5 consecutive pieces.

## Requirements

- Python 3.8 or higher
- Pygame library

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd gomoku-game
    ```

2. Install the required dependencies:
    ```bash
    pip install pygame
    ```

3. Run the game:
    ```bash
    python gomoku.py
    ```

## Gameplay Instructions

1. **Objective**: Align 5 of your pieces consecutively (horizontally, vertically, or diagonally).
2. **Human Player**: The human player uses black pieces and makes the first move after the AI's initial placement.
3. **AI Player**: The AI opponent uses white pieces and employs a strategic decision-making algorithm.
4. **Mouse Controls**: Click on a cell to place your piece.

## Key Components

### Constants
- Defines board size, colors, and gameplay settings.

### Functions

- **Initialize_Board()**: Sets up an empty game board.
- **Show_Board()**: Renders the grid and background.
- **PlayerPiece()**: Draws player pieces on the board.
- **CheckValidMove()**: Ensures moves are within bounds and on empty cells.
- **MakeMove()**: Updates the board with a player's move.
- **WinnerCheck()**: Detects a winning sequence of 5 consecutive pieces.
- **ValidMoveFinder()**: Finds potential moves for optimization.
- **Board_Evaluate()**: Scores the board based on piece patterns.
- **MiniMax()**: Implements the AI's decision-making with alpha-beta pruning.
- **CriticalMoveFinder()**: Identifies immediate winning or blocking moves.

## Screenshots

Add screenshots here to showcase gameplay and the UI.

## Future Improvements

- Enhance AI depth for more challenging gameplay.
- Add multiplayer support for two human players.
- Include more dynamic visual effects.
- Implement difficulty levels for AI.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Enjoy playing Gomoku!

