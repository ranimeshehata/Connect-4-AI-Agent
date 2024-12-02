import math
from node import Node
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc

def maximize(node, k, player1, turn, cached_dict):
    valid_moves = get_valid_moves(node.board)
    if node.depth == k or valid_moves == [] or is_terminal(node.board):
        if node.board in cached_dict:
            node.value = cached_dict[node.board]
            return node.value
        piece = "1" if player1 else "2"
        score = score_position(node.board, piece) 
        node.value = score
        cached_dict[node.board] = node.value
        return node.value

    max_value = -math.inf
    max_child = None
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth+1, 2, turn, move)
        node.children.append(child)

        value = minimize(child, k, player1, (turn % 2) + 1, cached_dict)   
        if value > max_value:
            max_value = value
            max_child = child

    node.value = max_value
    node.max_child = max_child
    return node.value


def minimize(node, k, player1, turn, cached_dict):
    valid_moves = get_valid_moves(node.board)
    if node.depth == k or valid_moves == [] or is_terminal(node.board):
        if node.board in cached_dict:
            node.value = cached_dict[node.board]
            return node.value
        piece = "1" if player1 else "2"
        score = score_position(node.board, piece) 
        node.value = score
        cached_dict[node.board] = node.value
        return node.value
    
    min_value = math.inf
    min_child = None
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth+1, 1, turn, move)
        node.children.append(child)

        value = maximize(child, k, player1, (turn % 2) + 1, cached_dict)
        if value < min_value:
            min_value = value
            min_child = child

    node.value = min_value
    node.max_child = min_child
    return node.value

def minimax(node, k, player1, turn):
    cached_dict = {}
    if player1:
        turn = 1
    else:
        turn = 2
    return maximize(node, k, player1, turn, cached_dict)

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


def print_best_moves(node):
    turn = 1
    while node.max_child:
        print("Player1 's move should be: ", node.max_child.move) if turn == 1 else print("Player2 's move should be: ",
                                                                                          node.max_child.move)
        turn = (turn % 2) + 1
        node = node.max_child
