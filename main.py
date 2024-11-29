from expectiminimax import expectiminimax
from minimax import maximize, minimize, print_tree
from alpha_beta_pruning import alpha_beta_pruning, print_best_moves, print_tree
from node import Node
import time

def main():
    board = "0"*7*4 + "0110000" + "0122200" # optimal move is 0
    k = 4
    player1 = 0
    turn = 1
    
    node = Node(None, board, 0, 1, 0, None)
    start= time.time()
    alpha_beta_pruning(node, k, player1, turn)
    end = time.time()
    print("Alpha beta pruning")
    print(node.value)
    print("best move ", node.max_child.move)
    print_best_moves(node)
    print("Time taken: ", end-start)
    # print_tree(node)
    
    node2 = Node(None, board, 0, 1, 0, None)
    t1 = time.time()
    expectiminimax(node2, 3, player1, turn)
    t2 = time.time()
    print("Time taken for expectiminimax: ", t2-t1)
    print("Expectiminimax")
    print(node2.value)
    print("best move ", node2.max_child.move)





if __name__ == "__main__":
    main()