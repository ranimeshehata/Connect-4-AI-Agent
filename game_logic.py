import numpy as np
from typing import List, Tuple, Optional


class GameLogic:
    def __init__(self, rows: int = 6, cols: int = 7):
        self.ROWS = rows
        self.COLS = cols
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.HUMAN = 1
        self.AI = 2

    def is_valid_move(self, col: int) -> bool:
        return self.board[0][col] == 0

    def get_valid_moves(self) -> List[int]:
        return [col for col in range(self.COLS) if self.is_valid_move(col)]

    def make_move(self, col: int, player: int) -> bool:
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False

    def check_win(self, player: int) -> bool:
        # Check horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Check diagonal (positive slope)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        # Check diagonal (negative slope)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        return False

    def is_board_full(self) -> bool:
        return len(self.get_valid_moves()) == 0

    def evaluate_window(self, window: List[int], player: int) -> int:
        opponent = self.HUMAN if player == self.AI else self.AI
        score = 0

        player_count = np.count_nonzero(window == player)
        empty_count = np.count_nonzero(window == 0)
        opponent_count = np.count_nonzero(window == opponent)

        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 5
        elif player_count == 2 and empty_count == 2:
            score += 2

        if opponent_count == 3 and empty_count == 1:
            score -= 4

        return score

    def evaluate_position(self, player: int) -> int:
        score = 0

        # Center column preference
        center_array = self.board[:, self.COLS // 2]
        center_count = np.count_nonzero(center_array == player)
        score += center_count * 3

        # Horizontal windows
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                window = list(self.board[row, col:col + 4])
                score += self.evaluate_window(window, player)

        # Vertical windows
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                window = list(self.board[row:row + 4, col])
                score += self.evaluate_window(window, player)

        # Diagonal windows (positive slope)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                window = [self.board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Diagonal windows (negative slope)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                window = [self.board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score