        self.clear_window()
        extra_width = 100
        extra_height = 100
        self.root.geometry(f"{COLS * CELL_SIZE + 20 + extra_width}x{ROWS * CELL_SIZE + 100 + extra_height}")  # Increase the window size
        self.canvas = tk.Canvas(self.root, width=COLS * CELL_SIZE + extra_width, height=ROWS * CELL_SIZE + extra_height, bg="#282c34", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.info_label = tk.Label(self.root, text="", font=("Arial", 14), fg="white", bg="#282c34")
        self.info_label.pack(pady=10)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.human_move)