

import math
import time
from node import Node
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc


def maximize(node, k, player1, turn, tree_root, cached_dict):
    
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
        child = Node(node, child_state, node.depth, 3, turn, move)  
        node.children.append(child)

        value = chance_node(child, k, player1, turn, tree_root, child.move, cached_dict)
        if value > max_value:
            max_value = value
            max_child = child
    node.value = max_value
    node.max_child = max_child
    return node.value


def minimize(node, k, player1, turn, tree_root, cached_dict):

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
        child = Node(node, child_state, node.depth, 3, turn, move)  
        node.children.append(child)
    
        value = chance_node(child, k, player1, turn, tree_root, child.move, cached_dict)
        if value < min_value:
            min_value = value
            min_child = child
    node.value = min_value
    node.max_child = min_child
    return node.value

    

def chance_node(node, k, player1, turn, tree_root, move, cached_dict):
    # determines child node types from parent node type of the chance node
    node_type = 2 if node.parent.node_type == 1 else 1
    main_child = Node(node, node.board, node.depth + 1, node_type, turn, move)
    node.children.append(main_child)

    if is_valid_move(node.board, move-1):
        left_state = drop_disc(node.board, move-1, turn)
        left_child = Node(node, left_state, node.depth + 1, node_type, turn, move-1)
        node.children.append(left_child)

    if is_valid_move(node.board, move+1):
        right_state = drop_disc(node.board, move+1, turn)
        right_child = Node(node, right_state, node.depth + 1, node_type, turn, move+1)
        node.children.append(right_child)
    
    expected_value = 0
    main_child_value = maximize(main_child, k, player1, (turn)%2 + 1, tree_root, cached_dict) if node_type == 1 else minimize(main_child, k, player1, (turn)%2 + 1, tree_root, cached_dict)
    
    if len(node.children) == 1:
        node.value = main_child_value
        return main_child_value
    probability = 0.2

    # for 2 children only, probability is 0.25 for side, 0.75 for main
    if len(node.children) == 2:
        probability = 0.25

    for child in node.children:
        if child == main_child:
            continue
        if node_type == 1:
            value = maximize(child, k, player1, (turn)%2 + 1, tree_root, cached_dict)
        else:
            value = minimize(child, k, player1, (turn)%2 + 1, tree_root, cached_dict)
        expected_value += (value * probability)

    # update probability for the main child to 0.6 if it was 0.2 per child, else  - 0.25
    probability = 0.6 if probability == 0.2 else 1 - probability

    expected_value += main_child_value * probability
    node.value = expected_value
    return node.value


def expectiminimax(node, k, player1, turn):
    if k % 2 != 0:
        k += 1
    cached_dict = {}
    if player1:
        turn = 1
    else:
        turn = 2
    return maximize(node, int(k//2), player1, turn, node, cached_dict)

     


