

import math
from node import Node

# IMPORTANT NOTES:
# Corner cases:
# 1. edges
# 2. if sides are 


def maximize(node, k, player1, turn, tree_root):
    
    if node.depth == k:
        node.value =  evaluate(node.board, player1) # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        return node
    node.children = get_children(node)
    max_value = -math.inf
    max_child = None
    for child in node.children:
        child.node_type = 3
        value = chance_node(child, k, player1, (turn+1)%2, tree_root)
        if value > max_value:
            max_value = value
            max_child = child
    node.value = max_value
    node.max_child = max_child
    return node.value


def get_children(node):
    # return children
    return []

def chance_node(node, k, player1, turn, tree_root, move):
    if node.depth == k:
        node.value = evaluate(node.board, player1) #evaluate children better
        return node
    main_child = get_node_by_move(node, move)
    left_child = get_node_by_move(node, move-1)
    right_child = get_node_by_move(node, move+1)
    if right_child is not None:
        node.children.append(right_child)
    if left_child is not None:
        node.children.append(left_child)
    expected_value = 0
    main_child_value = maximize(main_child, k, player1, turn, tree_root) if main_child.node_type == 1 else minimize(main_child, k, player1, turn, tree_root, move)
    
    if len(node.children) == 0:
        return main_child_value
    
    probability = 0.4/len(node.children)

    for child in node.children:
        if main_child.node_type == 1:
            value = maximize(child, k, player1, turn, tree_root)
        else:
            value = minimize(child, k, player1, turn, tree_root, move)
        expected_value += value * probability
    
    expected_value += main_child_value * (1 - 0.4)
    node.value = expected_value
    return node.value


    

def minimize(node, k, player1, turn, tree_root):
    if node.depth == k:
        node.value =  evaluate(node.board, player1) # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        return node
    node.children = get_children(node)
    min_value = math.inf
    min_child = None
    for child in node.children:
        child.node_type = 3
        value = chance_node(child, k, player1, (turn+1)%2, tree_root)
        if value < min_value:
            min_value = value
            min_child = child
    node.value = min_value
    node.min_child = min_child
    return node.value


def expectiminimax(node, k, player1, turn, tree_root):
    if player1 == 0:
        return maximize(node, k, player1, turn, tree_root)
    else:
        return minimize(node, k, player1, turn, tree_root)
    

def get_node_by_move(parent_node, move):
    node = Node() # calculate these accordingly, don't forget turn/type, type get from parent_node.parent.node_type and change it accordingly
    return node