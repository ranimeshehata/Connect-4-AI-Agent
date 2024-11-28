class Node:
    def __init__(self, parent, board, depth, node_type, player, move):
        self.parent = parent
        self.board = board
        self.depth = depth
        self.player = player
        self.node_type = node_type # 1 = max, 2 = min, 3 = chance
        self.children = []
        self.value = 0
        self.max_child = None
        self.move = move
        



    def add_child(self, child):
        self.children.append(child)