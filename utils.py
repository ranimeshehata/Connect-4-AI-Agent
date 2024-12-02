ROWS = 6
COLS = 7

def string_to_arrayint(state):
    return [int(state[i:i+7]) for i in range(0, len(state), 7)]

def arrayint_to_string(array):
    state = ""
    j = ""
    for i in array:
        if(len(str(i)) < 7):
            j = '0'*(7-len(str(i))) + str(i)
        state += j
    return state

def drop_disc(state, column, piece):
    # piece is taken from the turn
    for row in range(5, -1, -1):
        if state[row * 7 + column] == '0':
            new_state = ( state[:row * 7 + column] + str(piece) + state[row * 7 + column + 1:])
            break
    return new_state

def is_valid_move(state, column):
    if column < 0 or column >= 7:
        return False
    return state[column] == '0'

def get_valid_moves(state):
    valid_moves = []
    for i in range(7):
        if is_valid_move(state, i):
            valid_moves.append(i)
    # center is 3, prioritize it
    valid_moves.sort(key=lambda x: abs(x - 3))
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
            if(window.count("0") == 4):
                continue
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(cols):
        for r in range(rows - 3):
            start = r * cols + c
            window = state[start : start + 4 * cols : cols]
            if(window.count("0") == 4):
                continue
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            start = r * cols + c
            window = [state[start - i * (cols - 1)] for i in range(4)]
            if(window.count("0") == 4):
                continue
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals
    for r in range(3, rows):
        for c in range(3, cols):
            start = r * cols + c
            window = [state[start - i * (cols + 1)] for i in range(4)]
            if(window.count("0") == 4):
                continue
            score += evaluate_window(window, piece)

    return score


def evaluate_window(window, piece):
    opponent_piece = "1" if piece == "2" else "2"
    score = 0

    # Evaluate consecutive pieces for player
    consecutive_pieces = 0
    max_consecutive_pieces = 0
    free_slots = 0
    for i in window:
        if i == piece:
            consecutive_pieces += 1
            max_consecutive_pieces = max(max_consecutive_pieces, consecutive_pieces)
            continue
        elif i == "0":
            free_slots += 1
        else:
            consecutive_pieces = 0


    if consecutive_pieces == 4:
        score += 1000000  
    elif consecutive_pieces == 3 and free_slots == 1:
        score += 500000 
    elif consecutive_pieces == 2 and free_slots == 2:
        score += 2000  
    elif consecutive_pieces == 2 and free_slots > 2:
        score += 10  

    # Evaluate consecutive pieces for opponent
    opponent_consecutive = 0
    max_opponent_consecutive = 0
    free_slots = 0
    for i in window:
        if i == opponent_piece:
            opponent_consecutive += 1
            max_opponent_consecutive = max(max_opponent_consecutive, opponent_consecutive)
            continue
        elif i == "0":
            free_slots += 1
        else:
            opponent_consecutive = 0

    if opponent_consecutive == 4:
        score -= 800000  # Block opponent's win condition
    elif opponent_consecutive == 3 and free_slots == 1:
        score -= 400000  
    elif opponent_consecutive == 2 and free_slots == 2:
        score -= 1000  
    elif opponent_consecutive == 2 and free_slots > 2:
        score -= 5  

    # Consider position in the board (center prioritization)
    center_column = (window[2] == piece)
    if center_column:
        score += 150  

    return score

def nodes_expanded(node):
    if node.children == []:
        return 1
    count = 0
    for child in node.children:
        count += nodes_expanded(child)
    return count
