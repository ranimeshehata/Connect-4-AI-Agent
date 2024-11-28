import math
from utils import drop_disc, get_valid_moves, is_terminal, score_position

def minimax_alpha_beta(state, depth, alpha, beta, piece, maximizingPlayer, tree):
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
                minimax_alpha_beta(
                    child, depth - 1, alpha, beta, piece % 2 + 1, False, new_dict
                ),
            )
            alpha = max(alpha, value)
            if beta <= alpha:
                break
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
                minimax_alpha_beta(
                    child, depth - 1, alpha, beta, piece % 2 + 1, True, new_dict
                ),
            )
            beta = min(beta, value)
            if beta <= alpha:
                break
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value