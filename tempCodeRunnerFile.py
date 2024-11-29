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

        self.make_move(best_move, AI_PIECE)
        self.draw_board()
        algorithm_name = ALGORITHM_NAMES.get(self.algorithm, "Unknown Algorithm")
        self.info_label.config(text=f"AI Move: {best_move + 1}, Time: {execution_time:.2f} seconds, Algorithm: {algorithm_name}")
        self.check_game_over()