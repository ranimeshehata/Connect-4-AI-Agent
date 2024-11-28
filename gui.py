# import pygame
# import sys

# # Constants for the game
# BLUE = (0, 0, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)

# SQUARE_SIZE = 100
# RADIUS = SQUARE_SIZE // 2 - 5
# WIDTH = 7  # Minimum width
# HEIGHT = 6  # Minimum height
# SCREEN_WIDTH = WIDTH * SQUARE_SIZE
# SCREEN_HEIGHT = (HEIGHT + 1) * SQUARE_SIZE

# def draw_board(board):
#     for row in range(HEIGHT):
#         for col in range(WIDTH):
#             pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
#             pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + SQUARE_SIZE), RADIUS)

#     for row in range(HEIGHT):
#         for col in range(WIDTH):
#             if board[row][col] == 1:
#                 pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, SCREEN_HEIGHT - row * SQUARE_SIZE - SQUARE_SIZE // 2), RADIUS)
#             elif board[row][col] == 2:
#                 pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, SCREEN_HEIGHT - row * SQUARE_SIZE - SQUARE_SIZE // 2), RADIUS)
#     pygame.display.update()

# # Initialize the screen
# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Connect Four")
