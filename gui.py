import tkinter as tk
from tkinter import messagebox, Canvas, Toplevel, Scrollbar
import time
from node import Node
from alpha_beta_pruning import alpha_beta_pruning
from minimax import maximize, minimize
from expectiminimax import expectiminimax
from utils import drop_disc, get_valid_moves, is_terminal, score_position
from game import convert_from_string_to_grid, agent

ROWS = 6
COLS = 7
CELL_SIZE = 20  # Reduced cell size for tree display
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
        self.root.title("Connect Four")
        self.root.geometry("2200x1200")  # Set the window size for the main menu
        self.root.configure(bg="lightgrey")

        self.info_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="lightblue", relief="solid", bd=2)
        self.info_label.pack(pady=10)

        self.algorithm = None
        self.board = ["0"] * (ROWS * COLS)  # Initialize an empty board
        self.create_main_menu()
        self.create_board_canvas()

    def create_board_canvas(self):
        self.canvas = Canvas(self.root, width=COLS * CELL_SIZE * 5, height=ROWS * CELL_SIZE * 5, bg="blue")
        self.canvas.pack(pady=20)
        self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE * 5)

    def draw_board(self, canvas, board, x, y, cell_size):
        for row in range(ROWS):
            for col in range(COLS):
                x1 = x + col * cell_size
                y1 = y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                piece = board[row * COLS + col]
                color = "white"
                if piece == "1":
                    color = "red"
                elif piece == "2":
                    color = "yellow"
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color, outline="black")
        # Draw a frame around the board
        canvas.create_rectangle(x, y, x + COLS * cell_size, y + ROWS * cell_size, outline="black", width=2)

    def set_initial_state(self, state):
        self.board = state
        self.info_label.config(text="Initial state set.")
        self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE * 5)

    def calculate_next_move(self):
        self.algorithm = self.algorithm_var.get()
        if self.algorithm == 0:
            messagebox.showerror("Error", "Please select an algorithm first.")
            return

        grid = convert_from_string_to_grid("".join(self.board))
        depth = 6  # You can set this to any depth you want
        option = self.algorithm

        try:
            start_time = time.time()
            best_move, root = agent(grid, depth, option)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.board = drop_disc("".join(self.board), best_move, AI_PIECE)
            self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE * 5)
            self.info_label.config(text=f"Next best move: {best_move} using {ALGORITHM_NAMES[option]}. \n Time taken: {elapsed_time:.4f} seconds.")
            self.show_tree(root)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.root, bg="lightgrey", padx=20, pady=20, relief="solid", bd=2)
        self.main_menu_frame.pack(pady=20)

        tk.Label(self.main_menu_frame, text="Select Algorithm:", font=("Helvetica", 14, "bold"), bg="lightgrey").pack(pady=10)
        self.algorithm_var = tk.IntVar(value=0)
        for key, value in ALGORITHM_NAMES.items():
            tk.Radiobutton(self.main_menu_frame, text=value, variable=self.algorithm_var, value=key, font=("Helvetica", 12), bg="lightgrey").pack(anchor=tk.W)

        tk.Button(self.main_menu_frame, text="Set Initial State", command=self.show_initial_state_input, font=("Helvetica", 12), bg="lightblue", relief="raised", bd=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Calculate Next Move", command=self.calculate_next_move, font=("Helvetica", 12), bg="lightblue", relief="raised", bd=2).pack(pady=10)

    def show_initial_state_input(self):
        self.initial_state_window = tk.Toplevel(self.root)
        self.initial_state_window.title("Set Initial State")
        self.initial_state_window.configure(bg="lightgrey")

        tk.Label(self.initial_state_window, text="Enter initial state as a string (42 characters):", font=("Helvetica", 12), bg="lightgrey").pack(pady=10)
        self.initial_state_entry = tk.Entry(self.initial_state_window, width=50, font=("Helvetica", 12), relief="solid", bd=2)
        self.initial_state_entry.pack(pady=10)

        tk.Button(self.initial_state_window, text="Set", command=self.set_initial_state_from_input, font=("Helvetica", 12), bg="lightblue", relief="raised", bd=2).pack(pady=10)

    def set_initial_state_from_input(self):
        state = self.initial_state_entry.get()
        if len(state) != ROWS * COLS:
            messagebox.showerror("Error", "Invalid state length. Must be 42 characters.")
            return

        self.set_initial_state(state)
        self.initial_state_window.destroy()

    def show_tree(self, root):
        # Create a new window for the tree structure
        tree_window = Toplevel(self.root)
        tree_window.title("Tree Structure")
        tree_window.geometry("1000x1000")
        tree_window.configure(bg="lightgrey")

        # Add a canvas with scrollbars
        canvas_frame = tk.Frame(tree_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        h_scroll = Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        v_scroll = Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = Canvas(canvas_frame, bg="white", xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scroll.config(command=canvas.xview)
        v_scroll.config(command=canvas.yview)

        # Set the scrollable area of the canvas
        canvas.config(scrollregion=(0, 0, 5000, 5000))

        # Draw the tree on the canvas
        self.draw_tree(canvas, root, 2500, 50, 500)

    def draw_tree(self, canvas, node, x, y, x_offset):
        """
        Draw the tree structure with improved spacing and prevent overlap of nodes.
        """
        # Draw the node's board
        self.draw_board(canvas, node.board, x, y, CELL_SIZE)

        # Draw the node's score below the board
        canvas.create_text(x + CELL_SIZE * COLS / 2, y + CELL_SIZE * ROWS + 20, text=str(node.value), fill="black")

        if node.children:
            num_children = len(node.children)
            # Calculate spacing dynamically based on the number of children
            child_spacing = max(x_offset // num_children, CELL_SIZE * 2 * COLS)

            for i, child in enumerate(node.children):
                # Calculate child node position
                child_x = x - (child_spacing * (num_children - 1) / 2) + i * child_spacing
                child_y = y + 300

                # Draw a line to the child node
                canvas.create_line(
                    x + CELL_SIZE * COLS / 2,
                    y + CELL_SIZE * ROWS,
                    child_x + CELL_SIZE * COLS / 2,
                    child_y,
                    fill="black",
                )

                # Recursively draw the child nodes with reduced spacing
                self.draw_tree(canvas, child, child_x, child_y, x_offset // 2)


if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFour(root)
    root.mainloop()