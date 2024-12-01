

import math
import time
from node import Node
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc

# IMPORTANT NOTES:
# Corner cases:
# 1. edges
# 2. if sides are 
# node (self, parent, board, depth, node_type, player, move)

def maximize(node, k, player1, turn, tree_root, cached_dict):
    
    valid_moves = get_valid_moves(node.board)
    if node.depth == k or valid_moves == [] or is_terminal(node.board):
        if node.board in cached_dict:
            node.value = cached_dict[node.board]
            return node.value
        piece = "1" if player1 else "2"
        score = score_position(node.board, piece) # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        node.value = score
        cached_dict[node.board] = node.value
        return node.value
    
    max_value = -math.inf
    max_child = None
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth, 3, turn, move)  # not increasing depth, as it is chance node
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
        score = score_position(node.board, piece) # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        node.value = score
        cached_dict[node.board] = node.value
        return node.value
    
    min_value = math.inf
    min_child = None
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth, 3, turn, move)  # not increasing depth, as it is chance node
        node.children.append(child)
    
        value = chance_node(child, k, player1, turn, tree_root, child.move, cached_dict)
        if value < min_value:
            min_value = value
            min_child = child
    node.value = min_value
    node.max_child = min_child
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
    

def get_node_by_move(parent_node, move):
    node = Node() # calculate these accordingly, don't forget turn/type, type get from parent_node.parent.node_type and change it accordingly
    return node

def get_children(node):
    # return children
    return []

def chance_node(node, k, player1, turn, tree_root, move, cached_dict):
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
    main_child_value = maximize(main_child, k, player1, (turn)%2 + 1, tree_root, cached_dict) if node_type == 1 else minimize(main_child, k, player1, (turn)%2 + 1, tree_root, cached_dict)
    
    if len(node.children) == 1:
        node.value = main_child_value
        return main_child_value
    
    probability = 0.4/(len(node.children)-1)

    for child in node.children:
        if child == main_child:
            continue
        if node_type == 1:
            value = maximize(child, k, player1, (turn)%2 + 1, tree_root, cached_dict)
        else:
            value = minimize(child, k, player1, (turn)%2 + 1, tree_root, cached_dict)
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
    # board = "0"*7*6 # optimal move is 3
    board = "0"*7*4 + "0000200" + "0111220" # optimal move is 0
    # board = "0"*7*4 + "0001200" + "0111220" ,player1 = 1 #value is  -6153.84 best move is 6
    # board = "0"*7*3 + "0000200" + "0001200" + "1111222" # best move is 4
    # board = [0]*6
    # board = [0, 0, 0, 0, 0, 1000]
    # board = "0"*7*5 + "0012210" # optimal move is 3
    # board = "0"*7*4 + "0010000" + "0012200" # optimal move is 5 to block
    # print(board)
    node = Node(None, board, 0, 1, 0, None)
    # player1 = 0 if ai-agent, else 1
    # turn = 1 if player1, else 2
    k = 4
    player1 = 0
    turn = 1
    # expectiminimax(node, k, player1, turn)
    # print(expectiminimax(node, k, player1, turn))
    # print(node.value)
    # player1 = 1
    
    print(expectiminimax(node, k, player1, turn))
    # print_tree(node)
    print()
    print("value is ",node.value)
    print("best move is", node.max_child.move)
    #     print("best move is", node.max_child.move)
    # for k in range(1, 15):
    #     t1 = time.time()
    #     node = Node(None, board, 0, 1, 0, None)
    #     value = expectiminimax(node, k, player1, turn)
    #     t2 = time.time()
    #     print("k is ", k)
    #     print("Time taken is ", t2-t1)
    #     print("value is ",value)
    #     print("best move is", node.max_child.move)


