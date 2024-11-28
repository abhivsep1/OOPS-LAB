import pygame
import sys
from random import sample

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
font = pygame.font.Font(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Generate a simple Sudoku board (hardcoded for simplicity)
def generate_board():
    base = 3
    side = base * base

    # Pattern for a baseline solution
    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    # Shuffle rows, columns, and numbers
    def shuffle(s): return sample(s, len(s))

    rows = [g * base + r for g in shuffle(range(base)) for r in shuffle(range(base))]
    cols = [g * base + c for g in shuffle(range(base)) for c in shuffle(range(base))]
    nums = shuffle(range(1, side + 1))

    # Produce board using the pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Remove random numbers to create a puzzle
    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

# Initial board setup
sudoku_board = generate_board()
original_board = [row[:] for row in sudoku_board]

# Draw the grid
def draw_grid():
    screen.fill(WHITE)
    for i in range(10):
        thickness = 2 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * WIDTH // 9, 0), (i * WIDTH // 9, HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * HEIGHT // 9), (WIDTH, i * HEIGHT // 9), thickness)

# Draw numbers on the grid
def draw_numbers(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                color = BLACK if original_board[row][col] != 0 else BLUE
                text = font.render(str(num), True, color)
                x = col * WIDTH // 9 + WIDTH // 18
                y = row * HEIGHT // 9 + HEIGHT // 18
                screen.blit(text, text.get_rect(center=(x, y)))

# Highlight the selected cell
def highlight_cell(row, col):
    x = col * WIDTH // 9
    y = row * HEIGHT // 9
    pygame.draw.rect(screen, GRAY, (x, y, WIDTH // 9, HEIGHT // 9))

# Validate the number placement
def is_valid(board, row, col, num):
    # Check row and column
    if num in board[row] or num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 grid
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False
    return True

# Main game loop
running = True
selected_row, selected_col = None, None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            selected_row, selected_col = y // (HEIGHT // 9), x // (WIDTH // 9)

        if event.type == pygame.KEYDOWN:
            if selected_row is not None and selected_col is not None:
                if original_board[selected_row][selected_col] == 0:  # Allow only for editable cells
                    if event.key == pygame.K_1:
                        sudoku_board[selected_row][selected_col] = 1
                    elif event.key == pygame.K_2:
                        sudoku_board[selected_row][selected_col] = 2
                    elif event.key == pygame.K_3:
                        sudoku_board[selected_row][selected_col] = 3
                    elif event.key == pygame.K_4:
                        sudoku_board[selected_row][selected_col] = 4
                    elif event.key == pygame.K_5:
                        sudoku_board[selected_row][selected_col] = 5
                    elif event.key == pygame.K_6:
                        sudoku_board[selected_row][selected_col] = 6
                    elif event.key == pygame.K_7:
                        sudoku_board[selected_row][selected_col] = 7
                    elif event.key == pygame.K_8:
                        sudoku_board[selected_row][selected_col] = 8
                    elif event.key == pygame.K_9:
                        sudoku_board[selected_row][selected_col] = 9
                    elif event.key == pygame.K_BACKSPACE:
                        sudoku_board[selected_row][selected_col] = 0

    # Draw everything
    draw_grid()
    if selected_row is not None and selected_col is not None:
        highlight_cell(selected_row, selected_col)
    draw_numbers(sudoku_board)

    pygame.display.flip()

pygame.quit()
sys.exit()
