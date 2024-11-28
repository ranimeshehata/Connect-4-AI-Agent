from game import convert_from_string_to_grid, ROWS, COLS, min_tree, drop_disc, get_valid_moves, is_terminal, score_position
from alpha_beta_pruning import minimax_alpha_beta
import math

def count_window(board, window, player):
    number_of_windows = 0
    # Hirozontal windows
    for i in range(6):
        for j in range(7 - window + 1):
            if (
                board[i][j : j + window].count(player) == window
                and board[i][j : j + window].count(player % 2 + 1) == 0
            ):
                number_of_windows += 1
    # Vertical windows
    for i in range(6 - window + 1):
        for j in range(7):
            arr = [board[i + k][j] for k in range(window)]
            if arr.count(player) == window and arr.count(player % 2 + 1) == 0:
                number_of_windows += 1
    # Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            arr = [board[i + k][j + k] for k in range(window)]
            if arr.count(player) == window and arr.count(player % 2 + 1) == 0:
                number_of_windows += 1
    # Negative Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            arr = [board[i + window - 1 - k][j + k] for k in range(window)]
            if arr.count(player) == window and arr.count(player % 2 + 1) == 0:
                number_of_windows += 1
    return number_of_windows


# def evaluate_window(window, piece):
#     opponent_piece = "1" if piece == "2" else "2"
#     score = 0
#     if window.count("2") == 4:
#         score += 100000
#     elif window.count("2") == 3 and window.count("0") == 1:
#         score += 100
#     if window.count("2") == 2 and window.count("0") == 2:
#         score += 2

#     if window.count("1") == 4:
#         score -= 10000
#     elif window.count("1") == 3 and window.count("0") == 1:
#         score -= 500
#     elif window.count("1") == 2 and window.count("0") == 2:
#         score -= 1
#     return score

def evaluate_window(window, piece):
    """Evaluates the score of a given window for a specific piece."""
    opponent_piece = "1" if piece == "2" else "2"
    score = 0

    # Evaluate offensive potential
    consecutive_pieces = window.count(str(piece))
    free_slots = window.count("0")
    if consecutive_pieces == 4:
        score += 100000  # Win condition
    elif consecutive_pieces == 3 and free_slots == 1:
        score += 5000  # Strong winning opportunity
    elif consecutive_pieces == 2 and free_slots == 2:
        score += 200  # Potential winning connection
    elif consecutive_pieces == 2 and free_slots > 2:
        score += 10  # Encourage building connections

    # Evaluate defensive potential
    opponent_consecutive = window.count(str(opponent_piece))
    if opponent_consecutive == 4:
        score -= 50000  # Block opponent's win condition
    elif opponent_consecutive == 3 and free_slots == 1:
        score -= 4000  # Block opponent's strong winning opportunity
    elif opponent_consecutive == 2 and free_slots == 2:
        score -= 100  # Block opponent's potential winning connection
    elif opponent_consecutive == 2 and free_slots > 2:
        score -= 5  # Discourage opponent from building connections

    # Consider position in the board (center prioritization)
    center_column = window[2] == piece
    if center_column:
        score += 150  # Encourage occupying the center

    return score



# def score_position(state, piece):
#     rows = ROWS
#     cols = COLS
#     score = 0
#     center_array = [state[r * cols + cols // 2] for r in range(rows)]
#     center_count = center_array.count(piece)
#     score += center_count * 6

#     # Score horizontal
#     for r in range(rows):
#         for c in range(cols - 3):
#             start = r * cols + c
#             window = state[start : start + 4]
#             score += evaluate_window(window, piece)

#     # Score vertical
#     for c in range(cols):
#         for r in range(rows - 3):
#             start = r * cols + c
#             window = state[start : start + 4 * cols : cols]
#             score += evaluate_window(window, piece)

#     # Score positively sloped diagonals
#     for r in range(3, rows):
#         for c in range(cols - 3):
#             start = r * cols + c
#             window = [state[start - i * (cols - 1)] for i in range(4)]
#             score += evaluate_window(window, piece)

#     # Score negatively sloped diagonals
#     for r in range(3, rows):
#         for c in range(3, cols):
#             start = r * cols + c
#             window = [state[start - i * (cols + 1)] for i in range(4)]
#             score += evaluate_window(window, piece)

#     return score