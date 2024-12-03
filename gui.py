import tkinter as tk
from tkinter import messagebox, Canvas, Toplevel, Scrollbar
import time
from node import Node
from alpha_beta_pruning import alpha_beta_pruning
from minimax import maximize, minimize
from expectiminimax import expectiminimax
from utils import drop_disc, get_valid_moves, is_terminal, score_position, is_valid_move
from game import convert_from_string_to_grid, agent, count_connected_fours

ROWS = 6
COLS = 7
CELL_SIZE = 120
CELL_SIZE_TREE = 15
PLAYER_PIECE = 2
AI_PIECE = 1

ALGORITHM_NAMES = {
    1: "Minimax without Pruning",
    2: "Alpha-Beta Pruning",
    3: "Expectiminimax"
}

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        # Set the window size for the main menu
        self.root.geometry("1200x1000")  
        self.root.configure(bg="lightgrey")

        self.algorithm = None
        self.board = ["0"] * (ROWS * COLS)  # Initialize an empty board
        self.player1_is_ai = tk.BooleanVar(value=True)  # Default to AI as Player 1

        self.main_frame = tk.Frame(self.root, bg="lightgrey")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_main_menu()
        self.create_board_canvas()

        self.info_label = tk.Label(self.main_frame, text="", font=("Helvetica", 12), bg="lightblue", relief="solid", bd=2)
        self.info_label.grid(row=1, column=1, pady=10)

    def create_board_canvas(self):
        self.canvas = Canvas(self.main_frame, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
        self.canvas.grid(row=0, column=1, padx=20, pady=20)
        self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE)
    
    def assign_piece_values(self):
        global AI_PIECE, PLAYER_PIECE
        if self.player1_is_ai.get():
            AI_PIECE, PLAYER_PIECE = 1, 2
        else:
            AI_PIECE, PLAYER_PIECE = 2, 1


    def draw_board(self, canvas, board, x, y, cell_size):
        
        for row in range(ROWS):
            for col in range(COLS):
                x1 = x + col * cell_size
                y1 = y + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                piece = board[row * COLS + col]
                color = "white"
                if AI_PIECE == 1:
                    if piece == "2":
                        color = "yellow"
                    elif piece == "1":
                        color = "red"
                elif AI_PIECE == 2:
                    if piece == "2":
                        color = "red"
                    elif piece == "1":
                        color = "yellow"
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color, outline="black")
        # Draw a frame around the board
        canvas.create_rectangle(x, y, x + COLS * cell_size, y + ROWS * cell_size, outline="black", width=2)

    def set_initial_state(self, state):
        self.assign_piece_values()
        self.board = state
        self.info_label.config(text="Initial state set.")
        self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE)

    def calculate_next_move(self):
        self.assign_piece_values()
        self.algorithm = self.algorithm_var.get()
        if self.algorithm == 0:
            messagebox.showerror("Error", "Please select an algorithm first.")
            return

        grid = convert_from_string_to_grid("".join(self.board))
        depth = 8  # k
        option = self.algorithm
        player1_is_ai = self.player1_is_ai.get()

        try:
            start_time = time.time()
            best_move, root = agent(grid, depth, option, player1_is_ai)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.board = drop_disc("".join(self.board), best_move, AI_PIECE)
            self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE)
            
            # Count connected fours
            grid = convert_from_string_to_grid("".join(self.board))
            ai_connected_fours = count_connected_fours(grid, AI_PIECE)
            player_connected_fours = count_connected_fours(grid, PLAYER_PIECE)
            
            self.info_label.config(text=f"Next best move: {best_move} using {ALGORITHM_NAMES[option]}. \nTime taken: {elapsed_time:.4f} seconds.\nAI Score: {ai_connected_fours}\nHuman Score: {player_connected_fours}")
            self.root_node = root  # Save the root node for tree trace
            self.root.after(1000, self.human_turn)  # Allow human to play after AI move
        except Exception as e:
            messagebox.showerror("Error", "Board is full, Game over.")

    def human_turn(self):
        self.info_label.config(text=self.info_label.cget("text") + "\nHuman's turn. Click on a column to drop your disc.")
        self.canvas.bind("<Button-1>", self.human_move)

    def human_move(self, event):
        col = event.x // CELL_SIZE
        if col < 0 or col >= COLS:
            return
        if not is_valid_move("".join(self.board), col):
            messagebox.showerror("Error", "Invalid move, choose another column.")
            return
        self.board = drop_disc("".join(self.board), col, PLAYER_PIECE)
        self.draw_board(self.canvas, self.board, 0, 0, CELL_SIZE)
        self.canvas.unbind("<Button-1>")
        self.root.after(1000, self.calculate_next_move)  # AI plays after human move

    def create_main_menu(self):
        self.main_menu_frame = tk.Frame(self.main_frame, bg="lightgrey", padx=20, pady=20, relief="solid", bd=2)
        self.main_menu_frame.grid(row=0, column=0, rowspan=2, sticky="ns")

        tk.Label(self.main_menu_frame, text="Select Algorithm:", font=("Helvetica", 14, "bold"), bg="lightgrey").pack(pady=10)
        self.algorithm_var = tk.IntVar(value=0)
        for key, value in ALGORITHM_NAMES.items():
            tk.Radiobutton(self.main_menu_frame, text=value, variable=self.algorithm_var, value=key, font=("Helvetica", 12), bg="lightgrey").pack(anchor=tk.W)

        tk.Label(self.main_menu_frame, text="Who is Player 1?", font=("Helvetica", 14, "bold"), bg="lightgrey").pack(pady=10)
        tk.Radiobutton(self.main_menu_frame, text="AI", variable=self.player1_is_ai, value=True, font=("Helvetica", 12), bg="lightgrey").pack(anchor=tk.W)
        tk.Radiobutton(self.main_menu_frame, text="Human", variable=self.player1_is_ai, value=False, font=("Helvetica", 12), bg="lightgrey").pack(anchor=tk.W)

        tk.Button(self.main_menu_frame, text="Set Initial State", command=self.show_initial_state_input, font=("Helvetica", 12), bg="lightblue", relief="raised", bd=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Calculate Next Move", command=self.calculate_next_move, font=("Helvetica", 12), bg="lightblue", relief="raised", bd=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="View Tree Trace", command=self.view_tree_trace, font=("Helvetica", 12), bg="lightblue", relief="raised", bd=2).pack(pady=10)

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
        if root is None:
            messagebox.showerror("Error", "Tree trace is unavailable. Please run an algorithm first.")
            return

        # Create a new window for the tree structure
        tree_window = Toplevel(self.root)
        tree_window.title("Tree Structure")
        tree_window.geometry("1200x1000")
        tree_window.configure(bg="lightgrey")

        # Add canvas with scrollbars
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

        # Calculate canvas dimensions dynamically based on tree depth and width
        max_depth = self.get_tree_depth(root)
        max_width = 2 ** max_depth  # Maximum number of nodes at the deepest level
        node_spacing = 200  # Horizontal space between nodes (adjust as needed)
        width = max(1200, max_width * node_spacing)
        height = 300 * (max_depth + 1)

        # Set the scrollable region
        canvas.config(scrollregion=(0, 0, width, height))

        # Draw the tree starting at the top-middle of the canvas
        x_start = width // 2
        y_start = 50
        x_offset = node_spacing // 2  # Horizontal offset for children nodes

        self.draw_tree(canvas, root, x_start, y_start, x_offset)

        # Adjust scrollregion dynamically after drawing
        canvas.config(scrollregion=(0, 0, width + x_offset * 2, height))

    def draw_tree(self, canvas, node, x, y, x_offset):
        # Draw the current node's board
        self.draw_board(canvas, node.board, x, y, CELL_SIZE_TREE)

        # Improved text clarity
        score_x = x + CELL_SIZE_TREE * COLS / 2
        score_y = y + CELL_SIZE_TREE * ROWS + 20

        # Add more padding to the background rectangle
        padding_x = 60  # Horizontal padding
        padding_y = 15  # Vertical padding

        canvas.create_rectangle(
            score_x - padding_x,  # Left
            score_y - padding_y,  # Top
            score_x + padding_x,  # Right
            score_y + padding_y,  # Bottom
            fill="white", outline="black"
        )

        # Draw the text with bold font
        canvas.create_text(
            score_x,
            score_y,
            text=f"Score: {node.value}",
            fill="black",
            font=("Arial", 12, "bold")
        )

        if node.children:
            num_children = len(node.children)
            total_width = x_offset * 2
            child_spacing = max(200, total_width // max(num_children - 1, 1))  # Minimum spacing
            child_y = y + 350  # More vertical spacing

            for i, child in enumerate(node.children):
                # Calculate the position for each child node
                child_x = x - x_offset + i * child_spacing

                # Draw line from parent to child
                canvas.create_line(
                    x + CELL_SIZE_TREE * COLS / 2,
                    y + CELL_SIZE_TREE * ROWS,
                    child_x + CELL_SIZE_TREE * COLS / 2,
                    child_y,
                    fill="black"
                )

                # Recursively draw child nodes
                self.draw_tree(canvas, child, child_x, child_y, x_offset // 2)

    def get_tree_depth(self, node):
        if not node.children:
            return 1
        return 1 + max(self.get_tree_depth(child) for child in node.children)

    def view_tree_trace(self):
        self.show_tree(self.root_node)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFour(root)
    root.mainloop()