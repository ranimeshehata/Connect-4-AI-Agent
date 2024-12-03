from alpha_beta_pruning import alpha_beta_pruning
from minimax import minimize, maximize  
from expectiminimax import expectiminimax
from node import Node
import time

# Function takes board state, k, player1, and turn as input and returns the best move and time taken

def change2DtoString(board):
    return ''.join([str(cell) for row in board for cell in row])

def compete(board_2D, player1):
    if player1 == 2:
        player1 = 0
    board = change2DtoString(board_2D)
    k = 5
    turn = 1
    node = Node(None, board, 0, 1, player1, None)
    alpha_beta_pruning(node, k, player1, turn)
    print(node.max_child.board)
    return node.max_child.move

def nodes_expanded(node):
    if node.children == []:
        return 1
    count = 0
    for child in node.children:
        count += nodes_expanded(child)
    return count

def main():
    # k = int(input("Enter the depth of the tree: "))
    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 2, 0],
             [0, 1, 1, 1, 2, 2, 0]
             ]
    # if ai-agent started as player1, player1 = 1, otherwise player1 0
    player1 = int(input("Enter 1 if ai-agent started as player1, otherwise enter 2: "))
    t1 = time.time()
    move = compete(board, player1)
    t2 = time.time()
    print("Best move: ", move)
    print("time is", t2 - t1)
    
if __name__ == "__main__":
    main()
    
    
