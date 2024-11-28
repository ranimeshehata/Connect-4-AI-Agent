ROWS = 6
COLS = 7

def drop_disc(state, column, piece):
    for row in range(5, -1, -1):
        if state[row * 7 + column] == '0':
            new_state = ( state[:row * 7 + column] + str(piece)[0] + state[row * 7 + column + 1:])
            break
    return new_state

def is_valid_move(state, column):
    return state[column] == '0'

def get_valid_moves(state):
    valid_moves = []
    for i in range(7):
        if is_valid_move(state, i):
            valid_moves.append(i)
    return valid_moves

def is_terminal(state):
    for i in range(6):
        for j in range(7):
            if state[i * 7 + j] == '0':
                return False
    return True

def score_position(state, piece):
    rows = ROWS
    cols = COLS
    score = 0
    center_array = [state[r * cols + cols // 2] for r in range(rows)]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score horizontal
    for r in range(rows):
        for c in range(cols - 3):
            start = r * cols + c
            window = state[start : start + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(cols):
        for r in range(rows - 3):
            start = r * cols + c
            window = state[start : start + 4 * cols : cols]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            start = r * cols + c
            window = [state[start - i * (cols - 1)] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals
    for r in range(3, rows):
        for c in range(3, cols):
            start = r * cols + c
            window = [state[start - i * (cols + 1)] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
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