import random
import sys

# Initialize the Tic-Tac-Toe board
board = [' ' for _ in range(9)]

# Function to display the board
def display_board():
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    sys.stdout.flush()  # Ensure the output is flushed and printed

# Function to check for win condition
def check_winner(player, board):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
                      (0, 3, 6), (1, 4, 7), (2, 5, 8)]  # Columns, Diagonals
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return ' ' not in board

# Heuristic function: Score the board for A* search (1: win, -1: loss, 0: draw/ongoing)
def evaluate_board(board):
    if check_winner('O', board):
        return 1  # AI wins
    elif check_winner('X', board):
        return -1  # AI loses
    else:
        return 0  # Draw or game ongoing

# A* Search to find the best move
def a_star_search(board):
    best_score = float('-inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '  # Undo move
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Minimax function for decision-making in A* (with recursion)
def minimax(board, depth, is_maximizing):
    score = evaluate_board(board)
    if score != 0 or is_board_full(board):
        return score
    
    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                best_score = max(best_score, minimax(board, depth + 1, False))
                board[i] = ' '
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                best_score = min(best_score, minimax(board, depth + 1, True))
                board[i] = ' '
        return best_score

# Function for rule-based AI agent (X)
def rule_based_ai_move(board):
    # 1. If AI can win, take the winning move
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_winner('X', board):
                return
            board[i] = ' '
    
    # 2. If opponent can win, block them
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner('O', board):
                board[i] = 'X'
                return
            board[i] = ' '
    
    # 3. If center is free, take it
    if board[4] == ' ':
        board[4] = 'X'
        return
    
    # 4. Otherwise, pick a random move
    empty_spaces = [i for i in range(9) if board[i] == ' ']
    move = random.choice(empty_spaces)
    board[move] = 'X'

# Function to simulate a game between the two AIs
def play_game(print_game=False):
    global board
    board = [' ' for _ in range(9)]
    turn = 'X' if random.random() < 0.5 else 'O'  # Randomly decide who starts
    
    if print_game:
        print(f"Game start! {'Rule-based AI (X)' if turn == 'X' else 'A* AI (O)'} goes first.")
        sys.stdout.flush()  # Flush print

    while True:
        if turn == 'X':
            rule_based_ai_move(board)
            if print_game:
                display_board()
            if check_winner('X', board):
                if print_game:
                    print("Rule-based AI (X) wins!")
                    sys.stdout.flush()  # Flush print
                return 'X'
            turn = 'O'
        else:
            move = a_star_search(board)
            board[move] = 'O'
            if print_game:
                display_board()
            if check_winner('O', board):
                if print_game:
                    print("A* AI (O) wins!")
                    sys.stdout.flush()  # Flush print
                return 'O'
            turn = 'X'
        
        if is_board_full(board):
            if print_game:
                print("It's a draw!")
                sys.stdout.flush()  # Flush print
            return 'D'

# Simulation and statistics gathering
def simulate_games(n):
    results = {'X': 0, 'O': 0, 'D': 0}
    
    for i in range(n):
        # Print the game count and scoreboard at the start of each game
        print(f"\nGame {i+1} / {n}")
        print(f"Current Scoreboard - X (Rule-based): {results['X']}, O (A*): {results['O']}, Draws: {results['D']}")
        sys.stdout.flush()  # Flush print to ensure the game number is shown
        # Play and print each game
        result = play_game(print_game=True)
        
        # Increment the result counts
        results[result] += 1
    
    return results

# Run the simulation of 1000 games and print each game
n_games = 1000
results = simulate_games(n_games)

# After 1000 games, print the final results
print(f"\nAfter {n_games} games:")
print(f"Rule-based AI (X) wins: {results['X']}")
print(f"A* AI (O) wins: {results['O']}")
print(f"Draws: {results['D']}")
sys.stdout.flush()  # Ensure everything is printed

# Automatically calculate the win/draw/loss percentages
total_games = results['X'] + results['O'] + results['D']
x_win_percentage = (results['X'] / total_games) * 100
o_win_percentage = (results['O'] / total_games) * 100
draw_percentage = (results['D'] / total_games) * 100

print(f"\nOut of {total_games} games:")
print(f"Rule-based AI (X) win percentage: {x_win_percentage:.2f}%")
print(f"A* AI (O) win percentage: {o_win_percentage:.2f}%")
print(f"Draw percentage: {draw_percentage:.2f}%")
sys.stdout.flush()  # Flush final results to print
