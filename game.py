import random
import time
import math
from alpha_beta_pruning import minimax_alpha_beta
from utils import drop_disc, get_valid_moves, is_terminal, score_position

ROWS = 6
COLS = 7

min_tree = {}

def convert_from_string_to_grid(state):
    grid = [[0] * 7 for _ in range(6)]
    for i in range(0, 6):
        for j in range(0, 7):
            grid[i][j] = int(state[i * 7 + j])
    return grid

def convert_from_grid_to_string(grid):
    state = ""
    for i in range(0, 6):
        for j in range(0, 7):
            state += str(grid[i][j])
    return state

def agent(grid, depth, option):
    min_tree.clear()
    state = convert_from_grid_to_string(grid)
    min_tree[state] = {
        "depth": depth,
        "piece": 1,
        "value": 0,
        "childs": [],
    }
    valid_moves = get_valid_moves(state)
    scores = dict(
        zip(
            valid_moves,
            [get_score(state, col, 2, depth, option) for col in valid_moves],
        )
    )
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]

    res = random.choice(max_cols)
    min_tree[state]["value"] = scores[res]
    return res, min_tree

def get_score(state, col, piece, depth, option):
    next_state = drop_disc(state, col, piece)
    if option == 1:
        new_dict = {
            next_state: {
                "depth": depth - 1,
                "piece": piece % 2 + 1,
                "value": 0,
                "childs": [],
            }
        }
        value = minimax_alpha_beta(next_state, depth - 1, piece % 2 + 1, False, new_dict)
        new_dict[next_state]["value"] = value
        min_tree[state]["childs"].append(new_dict)
        return value
    else:
        new_dict = {
            next_state: {
                "depth": depth - 1,
                "piece": piece % 2 + 1,
                "value": 0,
                "childs": [],
            }
        }
        value = minimax_alpha_beta(
            next_state, depth - 1, -math.inf, math.inf, piece % 2 + 1, False, new_dict
        )
        new_dict[next_state]["value"] = value
        min_tree[state]["childs"].append(new_dict)
        return value


def print_tree(tree, indent=0):
    state = list(tree.keys())[0]
    print(
        "    " * indent
        + f"{state} | Depth: {tree[state]['depth']}, Piece: {tree[state]['piece']}, Value: {tree[state]['value']}"
    )
    childs = tree[state]["childs"]
    for child in childs:
        print_tree(child, indent + 1)


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
    Res = agent(board, 8, 2)
    print(Res[0])
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()