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
    root = Node(None, state, 0, 1, 0, None)  
    
    start = time.time()
    if option == 1:
        score = alpha_beta_pruning(root, depth, player1_is_ai, 1)
    elif option == 2:
        score = minimax(root, depth, player1_is_ai, 1)
    elif option == 3:
        score = expectiminimax(root, depth, player1_is_ai, 1)
    end = time.time()
    print(f"Time taken for algorithm: {end - start:.4f} seconds")
    

    best_move = root.max_child.move
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