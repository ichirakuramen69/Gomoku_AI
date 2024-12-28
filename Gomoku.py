import pygame
import sys
import math

# Constants defining game parameters and visual settings
WINDOW_DIMENSION = 600                                          # Size of the game window in pixels
BOARD_DIMENSION = 10                                            # Number of rows and columns on the game board
CELL_DIMENSION = WINDOW_DIMENSION // BOARD_DIMENSION            # Size of each cell on the board
BLACK = (0, 0, 0)                                               # Color for human player's pieces
WHITE = (255, 255, 255)                                         # Color for AI player's pieces
BACKGROUND_COLOR = (50, 150, 50)                                # Green background color
GRID_COLOR = (0, 0, 0)                                          # Color of grid lines
FRAME_RATE = 60                                                 # Game's rendering frame rate
HUMAN = 1                                                       # Identifier for human player
AI = 2                                                          # Identifier for AI player
SEQUENCE_LENGTH = 5                                             # Number of consecutive pieces needed to win

# Initialize Pygame for game rendering
pygame.init()

# Set up the game screen with specified dimensions
screen = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))
pygame.display.set_caption("Gomoku Game")
clock = pygame.time.Clock()

def Initialize_Board():
    """
    Create board as 2D list filled with zeros.
    Zero represents an empty cell, 1 represents human player, 2 represents AI.
    """
    return [[0 for _ in range(BOARD_DIMENSION)] for _ in range(BOARD_DIMENSION)]

def Show_Board():
    """
    Render the game board grid by drawing horizontal and vertical lines.
    Fills the background and creates a grid pattern.
    """
    screen.fill(BACKGROUND_COLOR)
    for x in range(BOARD_DIMENSION):
        # Draw vertical lines
        pygame.draw.line(screen, GRID_COLOR, (x * CELL_DIMENSION, 0), (x * CELL_DIMENSION, WINDOW_DIMENSION))
        # Draw horizontal lines
        pygame.draw.line(screen, GRID_COLOR, (0, x * CELL_DIMENSION), (WINDOW_DIMENSION, x * CELL_DIMENSION))

def PlayerPiece(row, col, color):
    """
    Draw a circular piece on the board at the specified row and column.
    """
    pygame.draw.circle(
        screen,
        color,
        (col * CELL_DIMENSION + CELL_DIMENSION // 2, row * CELL_DIMENSION + CELL_DIMENSION // 2),
        CELL_DIMENSION // 2 - 2
    )

def CheckValidMove(board, row, col):
    """
    Check if a move is valid on the board.
    """
    return 0 <= row < BOARD_DIMENSION and 0 <= col < BOARD_DIMENSION and board[row][col] == 0

def MakeMove(board, row, col, player):
    """
    Place a player's piece on the board at the specified location.
    """
    board[row][col] = player

def WinnerCheck(board, player):
    """
    Check if the specified player has won by having 5 consecutive pieces.
    """
    # Possible winning directions: horizontal, vertical, diagonal (both ways)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if board[row][col] != player:
                continue
            for dr, dc in directions:
                count = 0
                for i in range(SEQUENCE_LENGTH):
                    r, c = row + dr * i, col + dc * i
                    if 0 <= r < BOARD_DIMENSION and 0 <= c < BOARD_DIMENSION and board[r][c] == player:
                        count += 1
                    else:
                        break
                if count == SEQUENCE_LENGTH:
                    return True
    return False

def ValidMoveFinder(board, radius=2):
    """
    Find valid moves near existing pieces to optimize AI move selection.
    """
    moves = set()
    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            if board[row][col] != 0:
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        nr, nc = row + dr, col + dc
                        if CheckValidMove(board, nr, nc):
                            moves.add((nr, nc))
    return list(moves)

def Board_Evaluate(board, player):
    """
    Evaluate the board state for a given player.
    Calculates a score based on piece patterns and strategic positioning.
    """
    score = 0
    opponent = HUMAN if player == AI else AI
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def PatternCount(row, col, dr, dc, target):
        """
        Count consecutive pieces in a specific direction.
        """
        count = 0
        for i in range(SEQUENCE_LENGTH):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < BOARD_DIMENSION and 0 <= c < BOARD_DIMENSION and board[r][c] == target:
                count += 1
            else:
                break
        return count

    for row in range(BOARD_DIMENSION):
        for col in range(BOARD_DIMENSION):
            for dr, dc in directions:
                if board[row][col] == player:
                    # Reward player's piece patterns
                    score += PatternCount(row, col, dr, dc, player) ** 2
                elif board[row][col] == opponent:
                    # Penalize opponent's piece patterns
                    score -= PatternCount(row, col, dr, dc, opponent) ** 2
    return score

def MiniMax(board, depth, alpha, beta, maximizing_player):
    """
    Implement MiniMax algorithm with alpha-beta pruning for AI decision making.
    """
    # Check termination conditions
    if depth == 0 or WinnerCheck(board, HUMAN) or WinnerCheck(board, AI):
        return None, Board_Evaluate(board, AI)

    # Find valid moves near existing pieces
    valid_moves = ValidMoveFinder(board)
    best_move = None

    if maximizing_player:
        # AI's turn: maximize the evaluation score
        max_eval = -math.inf
        for row, col in valid_moves:
            board[row][col] = AI
            _, eval = MiniMax(board, depth - 1, alpha, beta, False)
            board[row][col] = 0
            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        # Human's turn: minimize the evaluation score
        min_eval = math.inf
        for row, col in valid_moves:
            board[row][col] = HUMAN
            _, eval = MiniMax(board, depth - 1, alpha, beta, True)
            board[row][col] = 0
            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move, min_eval

def AI_move(board):
    """
    Determine the AI's next move using a strategic approach.
    """
    # First, check for immediate winning or blocking moves
    critical_move = CriticalMoveFinder(board, AI)
    if critical_move:
        return critical_move

    # Then check for critical human threats to block
    critical_threat = CriticalMoveFinder(board, HUMAN)
    if critical_threat:
        return critical_threat

    # Use MiniMax algorithm for strategic decision making
    move, _ = MiniMax(board, depth=2, alpha=-math.inf, beta=math.inf, maximizing_player=True)
    return move

def CriticalMoveFinder(board, player):
    """
    Find a critical move that would result in an immediate win for the player.
    """
    for row, col in ValidMoveFinder(board):
        board[row][col] = player
        if WinnerCheck(board, player):
            board[row][col] = 0
            return (row, col)
        board[row][col] = 0
    return None

def main():
    """
    Handles user interactions and AI moves.
    """
    # Initialize game board
    board = Initialize_Board()
    game_over = False
    turn = AI  # AI starts first

    # AI makes the first move in the center of the board
    center = BOARD_DIMENSION // 2
    MakeMove(board, center, center, AI)
    turn = HUMAN

    # Main game loop
    while True:
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Human player's turn
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == HUMAN:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_DIMENSION, x // CELL_DIMENSION
                if CheckValidMove(board, row, col):
                    MakeMove(board, row, col, HUMAN)
                    if WinnerCheck(board, HUMAN):
                        print("Human wins !!!")
                        game_over = True
                    turn = AI

        # AI's turn
        if turn == AI and not game_over:
            move = AI_move(board)
            if move:
                MakeMove(board, move[0], move[1], AI)
                if WinnerCheck(board, AI):
                    print("AI wins !!!")
                    game_over = True
                turn = HUMAN

        # Render the game board
        Show_Board()
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if board[row][col] == HUMAN:
                    PlayerPiece(row, col, BLACK)
                elif board[row][col] == AI:
                    PlayerPiece(row, col, WHITE)

        # Update display and maintain frame rate
        pygame.display.flip()
        clock.tick(FRAME_RATE)

# Entry point of the game
if __name__ == "__main__":
    main()