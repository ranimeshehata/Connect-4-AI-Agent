from game_logic import GameLogic
import numpy as np
from typing import Tuple, Optional, Dict
import random


class Node:
    def __init__(self, board, move=None, parent=None):
        self.board = board.copy()
        self.move = move
        self.parent = parent
        self.children = []
        self.value = 0

    def add_child(self, child_node):
        self.children.append(child_node)


class AIAgent:
    def __init__(self, game: GameLogic, max_depth: int):
        self.game = game
        self.max_depth = max_depth
        self.root = None

    def print_tree(self, node: Node, depth: int = 0, prefix: str = ""):
        if node is None:
            return

        move_str = f"Move: {node.move}" if node.move is not None else "Root"
        value_str = f"Value: {node.value}"
        print(f"{prefix}├── {move_str} | {value_str}")

        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")
            self.print_tree(child, depth + 1, new_prefix)

    def minimax(self, depth: int, maximizing: bool, use_alpha_beta: bool = False,
                alpha: float = float('-inf'), beta: float = float('inf')) -> Tuple[int, Optional[int]]:
        if depth == 0 or self.game.check_win(self.game.HUMAN) or \
                self.game.check_win(self.game.AI) or self.game.is_board_full():
            return self.game.evaluate_position(self.game.AI), None

        valid_moves = self.game.get_valid_moves()
        best_move = random.choice(valid_moves) if valid_moves else None

        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                board_backup = self.game.board.copy()
                self.game.make_move(move, self.game.AI)

                current_node = Node(self.game.board, move, self.root)
                eval_score, _ = self.minimax(depth - 1, False, use_alpha_beta, alpha, beta)
                current_node.value = eval_score
                if self.root is not None:
                    self.root.add_child(current_node)

                self.game.board = board_backup

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                if use_alpha_beta:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board_backup = self.game.board.copy()
                self.game.make_move(move, self.game.HUMAN)

                current_node = Node(self.game.board, move, self.root)
                eval_score, _ = self.minimax(depth - 1, True, use_alpha_beta, alpha, beta)
                current_node.value = eval_score
                if self.root is not None:
                    self.root.add_child(current_node)

                self.game.board = board_backup

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                if use_alpha_beta:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break

            return min_eval, best_move

    def expectimax(self, depth: int, maximizing: bool) -> Tuple[float, Optional[int]]:
        if depth == 0 or self.game.check_win(self.game.HUMAN) or \
                self.game.check_win(self.game.AI) or self.game.is_board_full():
            return self.game.evaluate_position(self.game.AI), None

        valid_moves = self.game.get_valid_moves()
        best_move = random.choice(valid_moves) if valid_moves else None

        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                board_backup = self.game.board.copy()
                self.game.make_move(move, self.game.AI)

                current_node = Node(self.game.board, move, self.root)
                eval_score, _ = self.expectimax(depth - 1, False)
                current_node.value = eval_score
                if self.root is not None:
                    self.root.add_child(current_node)

                self.game.board = board_backup

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

            return max_eval, best_move
        else:
            expected_value = 0
            move_probabilities = self._get_move_probabilities(valid_moves)

            for move, prob in move_probabilities.items():
                board_backup = self.game.board.copy()
                self.game.make_move(move, self.game.HUMAN)

                current_node = Node(self.game.board, move, self.root)
                eval_score, _ = self.expectimax(depth - 1, True)
                current_node.value = eval_score
                if self.root is not None:
                    self.root.add_child(current_node)

                self.game.board = board_backup
                expected_value += eval_score * prob

            return expected_value, best_move

    def _get_move_probabilities(self, valid_moves: list) -> Dict[int, float]:
        probabilities = {}
        for i, move in enumerate(valid_moves):
            if i > 0:
                left_move = valid_moves[i - 1]
                probabilities[left_move] = probabilities.get(left_move, 0) + 0.2

            if i < len(valid_moves) - 1:
                right_move = valid_moves[i + 1]
                probabilities[right_move] = probabilities.get(right_move, 0) + 0.2

            probabilities[move] = probabilities.get(move, 0) + 0.6

        return probabilities

    def get_best_move(self, algorithm: str) -> int:
        self.root = Node(self.game.board)

        if algorithm == 'minimax':
            _, best_move = self.minimax(self.max_depth, True, False)
        elif algorithm == 'alphabeta':
            _, best_move = self.minimax(self.max_depth, True, True)
        elif algorithm == 'expectimax':
            _, best_move = self.expectimax(self.max_depth, True)
        else:
            raise ValueError("Invalid algorithm choice")

        print("\nDecision Tree:")
        self.print_tree(self.root)

        return best_move