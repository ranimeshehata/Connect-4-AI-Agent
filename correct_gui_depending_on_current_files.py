import tkinter as tk
from tkinter import ttk
import numpy as np
from game import agent, ROWS, COLS

class GameLogic:
    HUMAN = 1
    AI = 2

    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, col, player):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                break

    def is_board_full(self):
        return all(self.board[0][col] != 0 for col in range(COLS))

class ConnectFourGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four with AI")

        # Game settings
        self.game = GameLogic()
        self.cell_size = 60
        self.padding = 10

        # Configuration frame
        self.config_frame = ttk.Frame(self.root, padding="10")
        self.config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Algorithm selection
        ttk.Label(self.config_frame, text="Algorithm:").grid(row=0, column=0, padx=5)
        self.algorithm = tk.StringVar(value="minimax")
        algorithms = ["minimax", "alphabeta", "expectiminimax"]
        self.algo_menu = ttk.OptionMenu(self.config_frame, self.algorithm, "minimax", *algorithms)
        self.algo_menu.grid(row=0, column=1, padx=5)

        # Depth selection
        ttk.Label(self.config_frame, text="Depth:").grid(row=0, column=2, padx=5)
        self.depth = tk.StringVar(value="4")
        self.depth_entry = ttk.Entry(self.config_frame, textvariable=self.depth, width=5)
        self.depth_entry.grid(row=0, column=3, padx=5)

        # Start button
        self.start_button = ttk.Button(self.config_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=4, padx=5)

        # Game canvas
        canvas_width = COLS * self.cell_size + 2 * self.padding
        canvas_height = ROWS * self.cell_size + 2 * self.padding
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg='blue')
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        # Status label
        self.status_var = tk.StringVar(value="Select algorithm and depth to start")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, pady=5)

        self.game_active = False

        self.canvas.bind('<Button-1>', self.handle_click)
        self.draw_board()

        self.root.mainloop()

    def start_game(self):
        try:
            depth = int(self.depth.get())
            if depth <= 0:
                raise ValueError("Depth must be positive")

            self.game = GameLogic()
            self.game_active = True
            self.status_var.set("Game started - Your turn!")
            self.draw_board()

        except ValueError as e:
            self.status_var.set(f"Error: {str(e)}")

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLS):
                x = col * self.cell_size + self.padding
                y = row * self.cell_size + self.padding

                # Draw cell background
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                             fill='blue', outline='blue')

                # Draw piece
                piece_padding = 5
                piece_color = 'white'
                if self.game.board[row][col] == self.game.HUMAN:
                    piece_color = 'red'
                elif self.game.board[row][col] == self.game.AI:
                    piece_color = 'yellow'

                self.canvas.create_oval(x + piece_padding, y + piece_padding,
                                        x + self.cell_size - piece_padding,
                                        y + self.cell_size - piece_padding,
                                        fill=piece_color, outline='black')

    def handle_click(self, event):
        if not self.game_active:
            return

        # Convert click coordinates to column
        col = (event.x - self.padding) // self.cell_size

        if 0 <= col < COLS and self.game.is_valid_move(col):
            # Human move
            self.game.make_move(col, self.game.HUMAN)
            self.draw_board()

            if self.game.is_board_full():
                self.game_active = False
                self.status_var.set("It's a draw!")
                return

            # AI move
            self.status_var.set("AI is thinking...")
            self.root.update()

            ai_move, _ = agent(self.game.board.tolist(), int(self.depth.get()), self.algorithm.get())
            self.game.make_move(ai_move, self.game.AI)
            self.draw_board()

            if self.game.is_board_full():
                self.game_active = False
                self.status_var.set("It's a draw!")
                return

            self.status_var.set("Your turn!")

if __name__ == "__main__":
    ConnectFourGUI()