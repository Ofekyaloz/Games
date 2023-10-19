import math
import pygame
import sys
import random

from pygame import K_ESCAPE

# Constants
SCREEN_WIDTH = 540
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 30


def is_valid_move(board, row, col, num):
    # Check if the number is not in the same row
    if num in board[row]:
        return False

    # Check if the number is not in the same column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check if the number is not in the same 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def generate_sudoku_puzzle():
    def solve_sudoku(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in random.sample(range(1, 10), 9):
                        if is_valid_move(board, row, col, num):
                            board[row][col] = num
                            if solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    # Start with an empty Sudoku board
    puzzle_board = [[0 for _ in range(9)] for _ in range(9)]

    # Solve the Sudoku puzzle to get a valid solution
    solve_sudoku(puzzle_board)

    # Create a copy of the solution to generate the puzzle
    puzzle_copy = [row[:] for row in puzzle_board]

    # Remove numbers to create the puzzle
    for _ in range(40):  # Adjust the number of iterations to control the puzzle difficulty
        row, col = random.randint(0, 8), random.randint(0, 8)
        while puzzle_copy[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle_copy[row][col] = 0

    # Create a boolean grid to indicate fixed cells
    fixed_cells = [[True if puzzle_copy[row][col] != 0 else False for col in range(9)] for row in range(9)]

    return puzzle_copy, fixed_cells


# Check if the number is not in the same 3x3 grid
def collision_row(board, row, col, num):
    for i in range(9):
        if num == board[row][i]:
            return row, i

    return -1, -1


# Check if the number is not in the same column
def collision_col(board, row, col, num):
    for i in range(9):
        if num == board[i][col]:
            return i, col

    return -1, -1


# Check if the number is not in the same 3x3 grid
def collision_box(board, row, col, num):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return i, j

    return -1, -1


def draw_grid(board, fixed_cells, violate):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if fixed_cells[i][j]:
                # Set the background color of fixed cells to grey
                pygame.draw.rect(screen, (192, 192, 192), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw thin borders between individual cells
            pygame.draw.line(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE), ((j + 1) * CELL_SIZE, i * CELL_SIZE),
                             2)  # Horizontal line
            pygame.draw.line(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE), (j * CELL_SIZE, (i + 1) * CELL_SIZE),
                             2)  # Vertical line

            # Draw thicker borders for each 3x3 box (left, right, top, bottom edges only)
            if i % 3 == 0:
                pygame.draw.line(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE), ((j + 3) * CELL_SIZE, i * CELL_SIZE),
                                 4)  # Top
            if j % 3 == 0:
                pygame.draw.line(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE), (j * CELL_SIZE, (i + 3) * CELL_SIZE),
                                 4)  # Left

            font = pygame.font.Font(None, 36)
            if board[i][j] != 0:
                if tuple([i, j]) in violate:
                    text_color = RED
                else:
                    text_color = BLACK
                # elif fixed_cells[i][j]:
                #     text_color = BLACK
                # else:
                #     text_color = (128, 128, 128)
                text = font.render(str(board[i][j]), True, text_color)
                screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2,
                                   i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2))


def remove(loc, d, violate, copy, row, col):
    for e in copy:
        d[loc].remove(e)
        if e in violate:
            found = False
            for v in d.values():
                if e in v:
                    found = True
                    break

            if not found:
                if (e[0] * 9 + e[1]) not in d:
                    violate.remove(e)
                elif tuple([row, col]) in d[(e[0] * 9 + e[1])]:
                    d[(e[0] * 9 + e[1])].remove(tuple([row, col]))
                    if not d[(e[0] * 9 + e[1])]:
                        violate.remove(e)


pygame.font.init()

# Initialize Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()


# Main game loop
def main():
    sudoku_board, fixed_cells = generate_sudoku_puzzle()

    SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE  # Update SCREEN_HEIGHT based on GRID_SIZE and CELL_SIZE

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    selected = -math.inf, -math.inf
    violate = set()
    d = {}
    counter = 0
    for row in fixed_cells:
        for cell in row:
            if cell:
                counter += 1
    while running:
        screen.fill(WHITE)
        draw_grid(sudoku_board, fixed_cells, violate)

        if counter == 81 and not violate:
            font = pygame.font.Font(None, 48)
            win_text1 = font.render("You Win!", True, RED)
            win_text2 = font.render("Puzzle Completed!", True, RED)
            play_again_text = font.render("Press Enter to Play Again", True, (0, 0, 255))  # Set text color to blue

            border_width = 2
            border_color = BLACK

            border_win_text1 = pygame.Surface(
                (win_text1.get_width() + 2 * border_width, win_text1.get_height() + 2 * border_width))
            border_win_text1.fill(border_color)
            border_win_text1.blit(win_text1, (border_width, border_width))

            border_win_text2 = pygame.Surface(
                (win_text2.get_width() + 2 * border_width, win_text2.get_height() + 2 * border_width))
            border_win_text2.fill(border_color)
            border_win_text2.blit(win_text2, (border_width, border_width))

            border_play_again_text = pygame.Surface(
                (play_again_text.get_width() + 2 * border_width, play_again_text.get_height() + 2 * border_width))
            border_play_again_text.fill(border_color)
            border_play_again_text.blit(play_again_text, (border_width, border_width))

            # Calculate vertical positions for text
            text1_y = (SCREEN_HEIGHT - border_win_text1.get_height() - border_win_text2.get_height() - border_play_again_text.get_height() - 40) // 2
            text2_y = text1_y + border_win_text1.get_height()
            play_again_text_y = text2_y + border_win_text2.get_height() + 20  # Moved down by 20 pixels

            # Blit the bordered text on the screen
            screen.blit(border_win_text1, ((SCREEN_WIDTH - border_win_text1.get_width()) // 2, text1_y))
            screen.blit(border_win_text2, ((SCREEN_WIDTH - border_win_text2.get_width()) // 2, text2_y))
            screen.blit(border_play_again_text,
                        ((SCREEN_WIDTH - border_play_again_text.get_width()) // 2, play_again_text_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        sudoku_board, fixed_cells = generate_sudoku_puzzle()
                        running = True
                        selected = -math.inf, -math.inf
                        violate = set()
                        d = {}
                        counter = 0
                        for row in fixed_cells:
                            for cell in row:
                                if cell:
                                    counter += 1

            pygame.display.flip()
            clock.tick(FPS)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                row, col = selected
                if event.key == pygame.K_UP and row > 0:
                    selected = (row - 1, col)
                elif event.key == pygame.K_DOWN and row < GRID_SIZE - 1:
                    selected = (row + 1, col)
                elif event.key == pygame.K_LEFT and col > 0:
                    selected = (row, col - 1)
                elif event.key == pygame.K_RIGHT and col < GRID_SIZE - 1:
                    selected = (row, col + 1)
                elif event.unicode.isdigit() and 1 <= int(event.unicode) <= 9 and not fixed_cells[row][col]:
                    number = int(event.unicode)
                    if number == sudoku_board[row][col]:
                        continue
                    if sudoku_board[row][col] == 0:
                        counter += 1
                    x1, y1 = collision_row(sudoku_board, row, col, number)
                    x2, y2 = collision_col(sudoku_board, row, col, number)
                    x3, y3 = collision_box(sudoku_board, row, col, number)

                    loc = row * 9 + col
                    if loc not in d:
                        d[loc] = set()

                    copy = d[loc].copy()
                    remove(loc, d, violate, copy, row, col)

                    if x1 >= 0:
                        violate.add(tuple([x1, y1]))
                        d[loc].add(tuple([x1, y1]))
                        if (x1 * 9 + y1) in d:
                            d[(x1 * 9 + y1)].add(tuple([row, col]))
                    if x2 >= 0:
                        violate.add(tuple([x2, y2]))
                        d[loc].add(tuple([x2, y2]))
                        if (x2 * 9 + y2) in d:
                            d[(x2 * 9 + y2)].add(tuple([row, col]))
                    if x3 >= 0:
                        violate.add(tuple([x3, y3]))
                        d[loc].add(tuple([x3, y3]))
                        if (x3 * 9 + y3) in d:
                            d[(x3 * 9 + y3)].add(tuple([row, col]))
                    if x1 >= 0 or x2 >= 0 or x3 >= 0:
                        violate.add(tuple([row, col]))

                    e = tuple([row, col])
                    if not d[loc] and e in violate:
                        violate.remove(e)

                    sudoku_board[row][col] = number

                elif event.key == pygame.K_BACKSPACE and not fixed_cells[row][col]:
                    loc = row * 9 + col
                    if loc in d:
                        copy = d[loc].copy()
                        remove(loc, d, violate, copy, row, col)

                    e = tuple([row, col])
                    if not d[loc] and e in violate:
                        violate.remove(e)
                        for key, value in d.items():
                            if e in value:
                                d[key].remove(e)

                    sudoku_board[row][col] = 0
                    counter -= 1

        if selected:
            pygame.draw.rect(screen, (0, 128, 255),
                             (selected[1] * CELL_SIZE, selected[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
