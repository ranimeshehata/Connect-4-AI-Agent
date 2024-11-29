import math
from node import Node
from utils import score_position, is_valid_move, get_valid_moves, is_terminal, drop_disc

def maximize(node, k, player1, turn, alpha, beta):
    
    valid_moves = get_valid_moves(node.board)
    
    #if terminal node or depth reached, return heuristic value
    if node.depth == k or valid_moves == []:
        score = score_position(node.board, str(turn))
        node.value =  -1*score if player1 else score  # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        return node.value
    
    # <maxChild, maxUtility> = <null, -infinity>
    max_value = -math.inf 
    max_child = None
    
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth+1, 2, turn, move)
        node.children.append(child)
        
        value = minimize(child, k, player1, turn, alpha, beta)
        
        # <maxChild, maxUtility> = <child, value> if value > maxUtility
        # alpha = max(alpha, max_value)
        if value > max_value:
            max_value = value
            max_child = child
        alpha = max(alpha, max_value)
        
        # if beta <= alpha, break (pruning)
        if beta <= alpha:
            break
        
    node.value = max_value
    node.max_child = max_child
    return node.value


def minimize(node, k, player1, turn, alpha, beta):
    
    valid_moves = get_valid_moves(node.board)
    
    #if terminal node or depth reached, return heuristic value
    if node.depth == k or valid_moves == []:
        score = score_position(node.board, str(turn))
        node.value =  -1*score if player1 else score  # evaluate heuristic function, player1 if ai-agent then heuristic positive, else negative
        return node.value
    
    # <minChild, minUtility> = <null, infinity>
    min_value = math.inf
    min_child = None
    
    for move in valid_moves:
        child_state = drop_disc(node.board, move, turn)
        child = Node(node, child_state, node.depth+1, 1, turn, move)
        node.children.append(child)
        
        value = maximize(child, k, player1, turn, alpha, beta)
        
        # <minChild, minUtility> = <child, value> if value < minUtility
        # beta = min(beta, min_value)
        if value < min_value:
            min_value = value
            min_child = child
        beta = min(beta, min_value)
        
        # if beta <= alpha, break (pruning)
        if beta <= alpha:
            break
        
    node.value = min_value
    node.min_child = min_child
    return node.value


def alpha_beta_pruning(node, k, player1, turn):
    return maximize(node, k, player1, turn, -math.inf, math.inf)

# print tree level by level
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
    # alpha_beta_pruning(node, k, player1, turn)
    # print(alpha_beta_pruning(node, k, player1, turn))
    # print(node.value)
    # player1 = 1
    
    print(alpha_beta_pruning(node, k, player1, turn))
    print_tree(node)
    print()


# def minimax_alpha_beta(node, state, depth, alpha, beta, piece, maximizingPlayer, tree):
#     if depth == 0 or is_terminal(state):
#         return score_position(state, piece)
#     valid_location = get_valid_moves(state)
#     if maximizingPlayer:
#         value = -math.inf
#         for col in valid_location:
#             child = drop_disc(state, col, piece)
#             new_dict = {
#                 child: {
#                     "depth": depth - 1,
#                     "piece": piece % 2 + 1,
#                     "value": 0,
#                     "childs": [],
#                 }
#             }
#             value = max(
#                 value,
#                 minimax_alpha_beta(
#                     child, depth - 1, alpha, beta, piece % 2 + 1, False, new_dict
#                 ),
#             )
#             alpha = max(alpha, value)
#             if beta <= alpha:
#                 break
#             new_dict[child]["value"] = value
#             tree[state]["childs"].append(new_dict)
#         return value
#     else:
#         value = math.inf
#         for col in valid_location:
#             child = drop_disc(state, col, piece)
#             new_dict = {
#                 child: {
#                     "depth": depth - 1,
#                     "piece": piece % 2 + 1,
#                     "value": 0,
#                     "childs": [],
#                 }
#             }

#             value = min(
#                 value,
#                 minimax_alpha_beta(
#                     child, depth - 1, alpha, beta, piece % 2 + 1, True, new_dict
#                 ),
#             )
#             beta = min(beta, value)
#             if beta <= alpha:
#                 break
#             new_dict[child]["value"] = value
#             tree[state]["childs"].append(new_dict)
#         return value