import random
import time
from node import Node
from alpha_beta_pruning import alpha_beta_pruning
from minimax import minimax
from expectiminimax import expectiminimax
from utils import drop_disc, get_valid_moves, is_terminal, score_position

ROWS = 6
COLS = 7

def convert_from_string_to_grid(state):
    grid = [[0] * COLS for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            grid[i][j] = int(state[i * COLS + j])
    return grid

def convert_from_grid_to_string(grid):
    state = ""
    for i in range(ROWS):
        for j in range(COLS):
            state += str(grid[i][j])
    return state

def agent(grid, depth, option, player1_is_ai):
    state = convert_from_grid_to_string(grid)
    root = Node(None, state, 0, 1, 0, None)  # Root node for the AI
    valid_moves = get_valid_moves(state)
    scores = {}

    # Determine the AI piece based on player1_is_ai
    ai_piece = 1 if player1_is_ai else 2

    # Loop through valid moves and apply alpha-beta pruning for each
    for col in valid_moves:
        child_state = drop_disc(state, col, ai_piece)
        child_node = Node(root, child_state, 1, ai_piece, (ai_piece % 2) + 1, col)
        root.children.append(child_node)
        
        try:
            start = time.time()
            if option == 1:
                score = alpha_beta_pruning(child_node, depth, True, ai_piece)
            elif option == 2:
                score = minimax(child_node, depth, True, ai_piece)
            elif option == 3:
                score = expectiminimax(child_node, depth, True, ai_piece)
            end = time.time()
            print(f"Time taken for column {col} using {option}: {end - start:.4f} seconds")
            scores[col] = score
            
        except Exception as e:
            print(f"Error processing column {col}: {e}")
            scores[col] = float('-inf')  # Penalize invalid moves

    # Find the best move(s)
    max_value = max(scores.values(), default=float('-inf'))
    best_moves = [col for col, score in scores.items() if score == max_value]

    if not best_moves:
        raise ValueError("No valid moves available or all scores are invalid.")

    best_move = random.choice(best_moves)
    return best_move, root

def count_connected_fours(grid, piece):
    count = 0
    # Check horizontal locations for a win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if grid[r][c] == piece and grid[r][c + 1] == piece and grid[r][c + 2] == piece and grid[r][c + 3] == piece:
                count += 1

    # Check vertical locations for a win
    for r in range(ROWS - 3):
        for c in range(COLS):
            if grid[r][c] == piece and grid[r + 1][c] == piece and grid[r + 2][c] == piece and grid[r + 3][c] == piece:
                count += 1

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if grid[r][c] == piece and grid[r + 1][c + 1] == piece and grid[r + 2][c + 2] == piece and grid[r + 3][c + 3] == piece:
                count += 1

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if grid[r][c] == piece and grid[r - 1][c + 1] == piece and grid[r - 2][c + 2] == piece and grid[r - 3][c + 3] == piece:
                count += 1

    return count

def print_tree(node):
    queue = []
    queue.append(node)
    node_type = 0
    while queue:
        s = queue.pop(0)
        if s.node_type != node_type:
            print()
            print("Node type changed to", s.node_type)
            node_type = s.node_type

        print(s.value, " move:", s.move, "  ", end=" ")

        for child in s.children:
            queue.append(child)

# Example test case
board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [1, 2, 1, 2, 0, 2, 2],
    [1, 2, 2, 1, 1, 2, 1],
]

def main():
    start = time.time()
    option = 1
    Res = agent(board, 2, option)  # Assuming player1 is AI (option 1)
    print("Best Move:", Res[0])
    print("Tree Structure:")
    print_tree(Res[1])  # Prints the tree of nodes explored during alpha-beta pruning
    end = time.time()
    print("Execution Time:", end - start, "seconds")

if __name__ == "__main__":
    main()