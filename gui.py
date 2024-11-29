import tkinter as tk
from tkinter import messagebox
import random
import time
from node import Node
from alpha_beta_pruning import alpha_beta_pruning
from minimax import maximize, minimize
from expectiminimax import expectiminimax
from utils import drop_disc, get_valid_moves, is_terminal, score_position

ROWS = 6
COLS = 7
CELL_SIZE = 100
PLAYER_PIECE = 1
AI_PIECE = 2

ALGORITHM_NAMES = {
    1: "Minimax Pruning",
    2: "Alpha-Beta Pruning",
    3: "Expectiminimax"
}

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.info_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.info_label.pack()
        self.root.title("Connect Four")
        self.root.geometry("700x1000")  # Set the window size for the main menu
        self.algorithm = None
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        self.root.configure(bg="#282c34")
        label = tk.Label(self.root, text="Choose Algorithm", font=("Arial", 24, "bold"), fg="white", bg="#282c34")
        label.pack(pady=20)

        minimax_button = tk.Button(self.root, text="Minimax", font=("Arial", 18), bg="#61afef", fg="white", command=lambda: self.start_game(1))
        minimax_button.pack(pady=10)

        alpha_beta_button = tk.Button(self.root, text="Alpha-Beta Pruning", font=("Arial", 18), bg="#98c379", fg="white", command=lambda: self.start_game(2))
        alpha_beta_button.pack(pady=10)

        expectiminimax_button = tk.Button(self.root, text="Expectiminimax", font=("Arial", 18), bg="#e06c75", fg="white", command=lambda: self.start_game(3))
        expectiminimax_button.pack(pady=10)

    def start_game(self, algorithm):
        self.algorithm = algorithm
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current_turn = PLAYER_PIECE
        self.create_game_board()

    def create_game_board(self):
        self.clear_window()
        self.root.geometry(f"{COLS * CELL_SIZE + 20}x{ROWS * CELL_SIZE + 100}")  # Set the window size for the game board
        self.canvas = tk.Canvas(self.root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="#282c34", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.info_label = tk.Label(self.root, text="", font=("Arial", 14), fg="white", bg="#282c34")
        self.info_label.pack(pady=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.human_move)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = "white"
                if self.board[row][col] == PLAYER_PIECE:
                    color = "red"
                elif self.board[row][col] == AI_PIECE:
                    color = "yellow"
                self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color, outline="black")

    def human_move(self, event):
        col = event.x // CELL_SIZE
        if self.is_valid_move(col):
            self.make_move(col, PLAYER_PIECE)
            self.draw_board()
            if not self.check_game_over():
                self.root.after(500, self.ai_move)

    def ai_move(self):
        start_time = time.time()
        state = self.convert_from_grid_to_string(self.board)
        root = Node(None, state, 0, 1, 0, None)
        if self.algorithm == 1:
            best_move, _ = self.agent(root, 2, 1)
        elif self.algorithm == 2:
            best_move, _ = self.agent(root, 2, 2)
        elif self.algorithm == 3:
            best_move, _ = self.agent(root, 2, 3)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_time = execution_time * 1000  # Convert to milliseconds

        self.make_move(best_move, AI_PIECE)
        self.draw_board()
        algorithm_name = ALGORITHM_NAMES.get(self.algorithm)
        self.info_label.config(text=f"AI Best Move: {best_move + 1}, Time for AI: {execution_time:.2f} msec, Algorithm: {algorithm_name}")
        self.info_label.update_idletasks()  # Ensure the label is updated immediately
        self.check_game_over()

    def make_move(self, col, piece):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = piece
                break

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def check_game_over(self):
        if is_terminal(self.convert_from_grid_to_string(self.board)):
            self.show_winner()
            return True
        return False

    def show_winner(self):
        player_score = self.calculate_score(PLAYER_PIECE)
        ai_score = self.calculate_score(AI_PIECE)
        winner = "Draw"
        if player_score > ai_score:
            winner = "You Win!"
        elif ai_score > player_score:
            winner = "AI Wins!"
        messagebox.showinfo("Game Over", f"{winner}\nPlayer Score: {player_score}\nAI Score: {ai_score}")
        self.create_main_menu()

    def calculate_score(self, piece):
        state = self.convert_from_grid_to_string(self.board)
        return score_position(state, str(piece))

    def convert_from_grid_to_string(self, grid):
        state = ""
        for row in grid:
            state += "".join(map(str, row))
        return state

    def agent(self, root, depth, option):
        valid_moves = get_valid_moves(root.board)
        scores = {}

        for col in valid_moves:
            child_state = drop_disc(root.board, col, AI_PIECE)
            child_node = Node(root, child_state, 1, 2, (1 % 2) + 1, col)
            root.children.append(child_node)

            try:
                if option == 1:
                    score = maximize(child_node, depth, True, AI_PIECE)
                elif option == 2:
                    score = alpha_beta_pruning(child_node, depth, True, AI_PIECE)
                elif option == 3:
                    score = expectiminimax(child_node, depth, True, AI_PIECE)
                scores[col] = score
            except Exception as e:
                print(f"Error processing column {col}: {e}")
                scores[col] = float('-inf')

        max_value = max(scores.values(), default=float('-inf'))
        best_moves = [col for col, score in scores.items() if score == max_value]

        if not best_moves:
            raise ValueError("No valid moves available or all scores are invalid.")

        best_move = random.choice(best_moves)
        return best_move, root

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()