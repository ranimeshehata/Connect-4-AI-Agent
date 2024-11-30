from node import Node
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc
import math
import time

def maximize(node, k, player1, turn, alpha, beta, cached_dict):
    valid_moves = get_valid_moves(node.board)
    
    # Terminal condition: maximum depth, no moves, or terminal game state, return heuristic value
    if node.depth == k or valid_moves == [] or is_terminal(node.board):
        if node.board in cached_dict:
            node.value = cached_dict[node.board]
            return node.value
        score = score_position(node.board, str(turn))
        node.value =  -1*score if player1 else score  # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        cached_dict[node.board] = node.value
        return node.value
    
    max_value = -math.inf
    max_child = None
    
    for move in valid_moves:
        child_board = drop_disc(node.board, move, turn)
        child_node = Node(node, child_board, node.depth + 1, 2, turn, move)
        node.children.append(child_node)
        
        value = minimize(child_node, k, player1, (turn % 2) + 1, alpha, beta, cached_dict)
        
        if value > max_value:
            max_value = value
            max_child = child_node
        
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    
    node.value = max_value
    node.max_child = max_child
    return node.value

def minimize(node, k, player1, turn, alpha, beta, cached_dict):
    valid_moves = get_valid_moves(node.board)
    
    # Terminal condition: maximum depth, no moves, or terminal game state, return heuristic value
    if node.depth == k or valid_moves == [] or is_terminal(node.board):
        if node.board in cached_dict:
            node.value = cached_dict[node.board]
            return node.value
        score = score_position(node.board, str(turn))
        node.value =  -1*score if player1 else score  # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        cached_dict[node.board] = node.value
        return node.value
    
    min_value = math.inf
    min_child = None
    
    for move in valid_moves:
        child_board = drop_disc(node.board, move, turn)
        child_node = Node(node, child_board, node.depth + 1, 1, turn, move)
        node.children.append(child_node)
        
        value = maximize(child_node, k, player1, (turn % 2) + 1, alpha, beta, cached_dict)
        
        if value < min_value:
            min_value = value
            min_child = child_node
        
        beta = min(beta, value)
        if alpha >= beta:
            break
    
    node.value = min_value
    node.max_child = min_child
    return node.value

def alpha_beta_pruning(node, k, player1, turn):
    cached_dict = {}
    return maximize(node, k, player1, turn, -math.inf, math.inf, cached_dict)

# Print tree level by level
def print_tree(node):
    queue = []
    queue.append(node)
    while queue:
        current_node = queue.pop(0)
        print(f"Depth: {current_node.depth}, Value: {current_node.value}, Move: {current_node.move}")
        for child in current_node.children:
            queue.append(child)

def print_best_moves(node):
    turn = 1
    while node.max_child:
        print(f"Player {turn}'s move should be: {node.max_child.move}")
        turn = (turn % 2) + 1
        node = node.max_child

if __name__ == "__main__":
    # Example empty board
    board = "0" * 7 * 6  # Optimal move is 3
    board = "0" * 7 * 5 + "0012210"  # Optimal move is 3
    board = "0" * 7 * 4 + "0010000" + "0012200"  # Optimal move is 5 to block
    node = Node(None, board, 0, 1, 0, None)
    k = 8
    player1 = 0
    turn = 1

    print("Running Alpha-Beta Pruning...")
    start = time.time()
    alpha_beta_pruning(node, k, player1, turn)
    end = time.time()
    print("Printing Tree...")
    print_tree(node)
    print("Time taken: ", end - start)