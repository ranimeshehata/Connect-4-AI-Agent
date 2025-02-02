from expectiminimax import expectiminimax
from minimax import minimax, minimize, print_tree
from alpha_beta_pruning import alpha_beta_pruning, print_best_moves, print_tree
from node import Node
from utils import nodes_expanded
import time

def main():
    # board = "0"*7*6 # optimal move is 
    # board = "0"*7*3 + "0001200" + "0001200" + "0111222" # optimal move is 4 
    board = "0"*7*4 + "0110000" + "0122200" # optimal move is 5
    # board = "0"*7*4 + "0002000" + "0111220" # optimal move is 0
    # board = "0"*7*3 + "0000100" + "20012200" + "1111222" # optimal move is 3
    # board = "0"*7*3 + "0001000" + "20012200" + "1111222" # optimal move is 3
    board = "000000000000000000000000000000100000222110"
    board = "000000000000000000000000000000000000000000"
    board = "000000000000000000000000000000000200111220"

    k = 5
    player1 = 0
    turn = 1
    
    node = Node(None, board, 0, 1, 0, None)
    start= time.time()
    alpha_beta_pruning(node, k, player1, turn)
    end = time.time()
    print("Alpha beta pruning")
    print(node.value)
    print("best move ", node.max_child.move)
    # print_best_moves(node)
    print("Time taken: ", end-start)
    # print_tree(node)
    print("Number of nodes expanded: ", nodes_expanded(node))
    
    # node2 = Node(None, board, 0, 1, 0, None)
    # t1 = time.time()
    # expectiminimax(node2, k, player1, turn)
    # t2 = time.time()
    # print("Expectiminimax")
    # print(node2.value)
    # print("best move ", node2.max_child.move)
    # print("Time taken for expectiminimax: ", t2-t1)
    # print("Number of nodes expanded: ", nodes_expanded(node2))

    # print(board)
    # node3 = Node(None, board, 0, 1, 0, None)
    # start = time.time()
    # minimax(node3, k, player1, turn)
    # end = time.time()
    # print("Minimax")
    # print(node3.value)
    # print("best move ", node3.max_child.move)
    # print("Time taken: ", end-start)
    # print("Number of nodes expanded: ", nodes_expanded(node3))
    # print("print tree: ", print_tree(node3))

    # 000000000000000000000000000000200000111220
    # 000000000000000000000000000000000000000000



if __name__ == "__main__":
    main()