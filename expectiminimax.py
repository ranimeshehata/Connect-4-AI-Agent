

import math
from node import Node
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc

# IMPORTANT NOTES:
# Corner cases:
# 1. edges
# 2. if sides are 
# node (self, parent, board, depth, node_type, player, move)

def maximize(node, k, player1, turn, tree_root):
    
    valid_moves = get_valid_moves(node.board)
    if node.depth == k or valid_moves == []:
        score = score_position(node.board, str(turn))
        node.value =  -1*score if player1 else score  # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        return node.value
    
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth, 3, turn, move)  # not increasing depth, as it is chance node
        node.children.append(child)

    max_value = -math.inf
    max_child = None
    for child in node.children:
        value = chance_node(child, k, player1, turn, tree_root, child.move)
        if value > max_value:
            max_value = value
            max_child = child
    node.value = max_value
    node.max_child = max_child
    return node.value


def minimize(node, k, player1, turn, tree_root):

    valid_moves = get_valid_moves(node.board)
    if node.depth == k or valid_moves == []:
        score = score_position(node.board, str(turn))
        node.value =  -1*score if player1 else score  # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        return node.value
    
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth, 3, turn, move)  # not increasing depth, as it is chance node
        node.children.append(child)
    
    min_value = math.inf
    min_child = None
    for child in node.children:
        child.node_type = 3
        value = chance_node(child, k, player1, turn, tree_root, child.move)
        if value < min_value:
            min_value = value
            min_child = child
    node.value = min_value
    node.min_child = min_child
    return node.value


def expectiminimax(node, k, player1, turn):
    return maximize(node, k, player1, turn, node)
    

def get_node_by_move(parent_node, move):
    node = Node() # calculate these accordingly, don't forget turn/type, type get from parent_node.parent.node_type and change it accordingly
    return node

def get_children(node):
    # return children
    return []

def chance_node(node, k, player1, turn, tree_root, move):
    # if node.depth == k:
    #     node.value = score_position(node.board, player1) #evaluate children better
    #     return node
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
    main_child_value = maximize(main_child, k, player1, (turn)%2 + 1, tree_root) if node_type == 1 else minimize(main_child, k, player1, (turn)%2 + 1, tree_root)
    
    if len(node.children) == 1:
        node.value = main_child_value
        return main_child_value
    
    probability = 0.4/(len(node.children)-1)

    for child in node.children:
        if child == main_child:
            continue
        if node_type == 1:
            value = maximize(child, k, player1, (turn)%2 + 1, tree_root)
        else:
            value = minimize(child, k, player1, (turn)%2 + 1, tree_root)
        expected_value += (value * probability)
    
    expected_value += main_child_value * (1 - 0.4)
    node.value = expected_value
    return node.value

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
            
        print(s.value ," move:",s.move,"  ", end=" ")

        for child in s.children:
            queue.append(child)

        
    

if __name__ == "__main__":
    board = "0"*7*6 # optimal move is 3
    board = "0"*7*5 + "0012210" # optimal move is 3
    board = "0"*7*4 + "0010000" + "0012200" # optimal move is 5 to block
    # print(board[9])
    node = Node(None, board, 0, 1, 0, None)
    # player1 = 0 if ai-agent, else 1
    # turn = 1 if player1, else 2
    k = 2
    player1 = 0
    turn = 1
    # expectiminimax(node, k, player1, turn)
    # print(expectiminimax(node, k, player1, turn))
    # print(node.value)
    # player1 = 1
    
    print(expectiminimax(node, k, player1, turn))
    print_tree(node)
    print()
