import math
from utils import drop_disc, get_valid_moves, is_terminal, score_position

def minimax(state, depth, piece, maximizingPlayer, tree):
    if depth == 0 or is_terminal(state):
        return score_position(state, piece)
    valid_location = get_valid_moves(state)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_location:
            child = drop_disc(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "piece": piece % 2 + 1,
                    "value": 0,
                    "childs": [],
                }
            }
            value = max(
                value,
                minimax(
                    child, depth - 1, piece % 2 + 1, False, new_dict
                ),
            )
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value
    else:
        value = math.inf
        for col in valid_location:
            child = drop_disc(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "piece": piece % 2 + 1,
                    "value": 0,
                    "childs": [],
                }
            }

            value = min(
                value,
                minimax(
                    child, depth - 1, piece % 2 + 1, True, new_dict
                ),
            )
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value