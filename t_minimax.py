import math
from node import Node
from minimax import maximize
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc

ROWS = 6
COLS = 7

def print_board(state):
    """Prints the Connect Four board in a human-readable format."""
    for r in range(ROWS):
        print(" | ".join(state[r * COLS:(r + 1) * COLS]))
    print("-" * 29)  # Separator for the board

def create_initial_state():
    """Creates an empty board state."""
    return "0" * (ROWS * COLS)

def main():
    """Main function to test the algorithm."""
    # Initialize the game
    initial_state = create_initial_state()
    current_state = initial_state
    depth_limit = 20  # Maximum depth for the AI to search
    user_piece = "1"  # The user's piece
    ai_piece = "2"    # The AI's piece
    turn = 1          # 1 = user, 2 = AI

    while not is_terminal(current_state):
        print_board(current_state)
        if turn == 1:
            # User's turn
            print("Your turn! Choose a column (0-6):")
            valid_moves = get_valid_moves(current_state)
            print("Valid moves:", valid_moves)
            user_move = -1

            # Get valid input from the user
            while user_move not in valid_moves:
                try:
                    user_move = int(input("Enter your move: "))
                    if user_move not in valid_moves:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Please enter a valid number.")

            # Drop the user's piece
            current_state = drop_disc(current_state, user_move, user_piece)

        else:
            # AI's turn
            print("AI is thinking...")
            root = Node(None, current_state, 0, 1, ai_piece, None)
            maximize(root, depth_limit, player1=0, turn=2)
            best_move = root.max_child.move
            print(f"AI chooses column {best_move}")
            current_state = drop_disc(current_state, best_move, ai_piece)

        # Switch turn
        turn = 3 - turn

    # Print final state
    print_board(current_state)
    print("Game Over!")

if __name__ == "__main__":
    main()
