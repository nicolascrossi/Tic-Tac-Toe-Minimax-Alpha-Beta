import random
import time
import math

board: list[str | int] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# This represents all the triplets that can win the game, i.e. if you put a piece on each place in a member of win_combinations you have won
win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)] # can be list of lists instead of list of tuples

use_ai = False

while True:
    reply = input("Do you want to play against the AI? (y/n)\n")
    if reply == "y":
        use_ai = True
        break
    elif reply == "n":
        use_ai = False
        break
    print("Input was not \'y\' or \'n\'. Try again.")
  

# This function prints the board. This can be customized as necessary.
def draw_board():
    print()
    print(str(board[0]) + "|" + str(board[1]) + "|" + str(board[2]))
    print("-+-+-")
    print(str(board[3]) + "|" + str(board[4]) + "|" + str(board[5]))
    print("-+-+-")
    print(str(board[6]) + "|" + str(board[7]) + "|" + str(board[8]))
    print()

def draw_given_board(board):
    print()
    print(str(board[0]) + "|" + str(board[1]) + "|" + str(board[2]))
    print("-+-+-")
    print(str(board[3]) + "|" + str(board[4]) + "|" + str(board[5]))
    print("-+-+-")
    print(str(board[6]) + "|" + str(board[7]) + "|" + str(board[8]))
    print()

# Given a player, this returns the other player. Optional helper function.
def other_player(player):
    if player == "X":
        return "O"
    else:
        return "X"

# This function asks the player for a move input and inserts its mark at that location. It verifies the input is correct and after making the move, it checks if that move was a winning move. If not, this function initiates the next move by calling itself.
def make_move(player, move):
    board[move] = player
    draw_board()
    if not check_win(player):
        move = ask_move(other_player(player))
        make_move( other_player(player), move)

# This function asks the player where to move using the input() function and validates the answer. It returns the move. A move is valid if: it is less than or equal to 0, greather than or equal to 9, not already
def ask_move(player):
  while True:
    try:

      if use_ai and player == "O":
        # ai_thinking()
        # return ai_move_smarter(player)
        return ai_ab(player)
      else:
        move = input("Player " + player + ": ")
        move = int(move)
        
        # TODO: Check for valid move, return only if valid
        if move >= 0 and move <= 8:
          if board[move] != 'X' and board[move] != 'O':
            return move

        print("\n That's invalid. Try again.")
    except ValueError:
      print("\n That's not a number. Try again.")

def ai_move_random(player):
    move = random.randint(0, 8)
    while board[move] == "X" or board[move] == "O":
        move = random.randint(0, 8)
    return move

def ai_move_smarter(player):
  # Check if it's possible to win before worrying about blocking
  for combo in win_combinations:
    p_counter = 0 # Num pieces belonging to player
    op_counter = 0 # Num pieces belonging to other_player(player)
    free = None # A free spot
      
    for spot in combo: # Examine each spot in the current win combo
      if board[spot] == player:
        p_counter += 1
      elif board[spot] == other_player(player):
        op_counter += 1
      else:
        free = spot
    if p_counter == 2 and op_counter == 0: # AI can win
      return free

  # Now check if we need to block
  for combo in win_combinations:
    p_counter = 0 # Num pieces belonging to player
    op_counter = 0 # Num pieces belonging to other_player(player)
    free = None # A free spot
      
    for spot in combo: # Examine each spot in the current win combo
      if board[spot] == player:
        p_counter += 1
      elif board[spot] == other_player(player):
        op_counter += 1
      else:
        free = spot
    if p_counter == 0 and op_counter == 2: # AI needs to block or lose
      return free

  return ai_move_random(player)


def heuristic(board: list[int | str], player: str, next_player: str) -> int | float:
    # Check for a win
    for combo in win_combinations:
        if (board[combo[0]] == board[combo[1]] == board[combo[2]]):
            if board[combo[0]] == player:
                return math.inf # Winning is always best
            if board[combo[0]] == other_player(player):
                return -math.inf # Losing is always worst
    
    # Check for tie
    empty = False
    for spot in board:
        if spot != 'O' and spot != 'X':
            empty = True
            break
    if not empty:
        return 0 # Tie is meh

    # Check for two in a rows
    op_two_row = 0
    p_two_row = 0
    for combo in win_combinations:
        p = 0
        op = 0
        for spot in combo:
            if board[p] == player:
                p += 1
            elif board[p] == other_player(player):
                op += 1
        if p == 2 and op == 0:
            # Player has an unblocked two in a row
            p_two_row += 1
        elif p == 0 and op == 2:
            # Enemy has an unblocked two in a row
            op_two_row += 1

    if p_two_row > 1 and player == next_player:
        return 1000 # Player can win
    elif op_two_row > 1 and other_player(player) == next_player:
        return -1000 # Enemy can win
    elif p_two_row >= 2 and other_player(player) == next_player:
        return 900 # Player can win once it's their turn again
    elif op_two_row >= 2 and player == next_player:
        return -900 # Enemy can win once it's their turn again

    return p_two_row * 10 + op_two_row * -10 # Player wants more two in a rows


def alpha_beta(board: list[int | str], alpha: float, beta: float, starting_player: str, cur_player: str, maximizing: bool) -> int | float:
    if check_win_given(board): # We just want to know if the game ended
        return heuristic(board, starting_player, cur_player)
    
    if maximizing:
        value = -math.inf

        for i in range(0, 9):
            if type(board[i]) == int:
                # Space is free
                new_board = board.copy()
                new_board[i] = cur_player
                
                value = max(value, alpha_beta(new_board, alpha, beta, starting_player, other_player(cur_player), False))

                if value >= beta:
                    break

                alpha = max(alpha, value)
        
        return value
    else:

        value = math.inf

        for i in range(0, 9):
            if type(board[i]) == int:
                # Space is free
                new_board = board.copy()
                new_board[i] = cur_player
                
                value = min(value, alpha_beta(new_board, alpha, beta, starting_player, other_player(cur_player), True))

                if value <= alpha:
                    break

                beta = min(beta, value)
        
        return value


def ai_ab(player: str) -> int:
    best_move = None
    best_score = -math.inf
    for i in range(0, 9):
        if type(board[i]) == int:
            print(f"Testing move {i}")
            new_board = board.copy()
            new_board[i] = player

            score = alpha_beta(new_board, best_score, math.inf, player, other_player(player), False)
            print(f"Move has score {score}")
            if best_move is None or best_score < score:
                print(f"Updated best move")
                best_move = i
                best_score = score
    
    if best_move is None:
        return ai_move_random(player)

    return best_move


# Function for aesthetics only
def ai_thinking():
    print("AI is thinking", end = "", flush = True)
    time.sleep(random.uniform(0.5, 1.2))
    print(".", end = "", flush = True)
    time.sleep(random.uniform(0.5, 1.2))
    print(".", end = "", flush = True)
    time.sleep(random.uniform(0.5, 1.2))
    print(".", flush = True)

    
# This function checks for a win or tie condition and is called after every move. Return true if the game ends.
def check_win(player):
    # Check for win
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]]:
            print("Player " + player + " has won!")
            return True

    # Check for a tie
    for spot in board:
        if spot != 'O' and spot != 'X':
            return False

    print("It's a tie!")
    return True

def check_win_given(board):
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return True

    # Check for a tie
    for spot in board:
        if spot != 'O' and spot != 'X':
            return False

    return True

# Initiate the game by drawing the board, telling the player what to do, and making the first move.
def tic_tac_toe():
    print("Let's play Tic Tac Toe!")
    draw_board()
    make_move("X", ask_move("X"))

tic_tac_toe()
