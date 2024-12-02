from alpha_beta_pruning import alpha_beta_pruning
from minimax import minimize, maximize  
from expectiminimax import expectiminimax
from node import Node
import time

# Function takes board state, k, player1, and turn as input and returns the best move and time taken

def change2DtoString(board):
    return ''.join([str(cell) for row in board for cell in row])

def compete(board, k, player1):
    turn = 1
    # depth = 0, 1 for maximize
    node = Node(None, board, 0, 1, player1, None)
    start = time.time()
    alpha_beta_pruning(node, k, player1, turn)
    end = time.time()
    expanded = nodes_expanded(node)
    return node.max_child.move, (end-start), node.max_child.board, expanded

def nodes_expanded(node):
    if node.children == []:
        return 1
    count = 0
    for child in node.children:
        count += nodes_expanded(child)
    return count

def main():
    k = int(input("Enter the depth of the tree: "))
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 2, 0],
             [0, 1, 1, 1, 2, 2, 0]
             ]
    # player1 aymbol is 1, player2 symbol is 2, so if ai-agent started as player1, player1 = 0 
    player1 = int(input("Enter 1 if ai-agent started as player1, otherwise enter 0: "))
    # board = input("Enter the board state as a string: ")
    move, time_taken, new_board, nodes_number = compete(change2DtoString(board), k, player1)
    print("Best move: ", move)
    print("Time taken: ", time_taken)
    print("Board state after the move: ", new_board)
    print("Number of nodes expanded: ", nodes_number)


# 000000000000000000000000000000200000111220
# 000000000000000000000000000000100000222110
# 000000000000000000000000000000000000000000
if __name__ == "__main__":
    main()
    
    
