from expectiminimax import expectiminimax
from minimax import maximize, minimize, print_tree
from alpha_beta_pruning import alpha_beta_pruning, print_best_moves, print_tree
from node import Node
import time

def main():
    board = "0"*7*4 + "0000200" + "0111220" # optimal move is 0
    node = Node(None, board, 0, 1, 0, None)
    k = 9
    player1 = 0
    turn = 1
    start=time.time()
    alpha_beta_pruning(node, k, player1, turn)
    end=time.time()
    print("Alpha beta pruning")
    print(node.value)
    print("best move ", node.max_child.move)
    print_best_moves(node)
    print("Time taken: ", end-start)
    # print_tree(node)




if __name__ == "__main__":
    main()