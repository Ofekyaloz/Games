import math
import pygame
import sys
import random

from pygame import K_ESCAPE

# Constants
SCREEN_WIDTH = 540
BOX_ROWS = BOX_COLS = GRID_SIZE = FULL_BOARD = 1
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 30
MAX_NUMBER = 9


def generate_sudoku_puzzle():
    def is_valid_move(board, row, col, num):
        # Check if the number is not in the same row
        if num in board[row]:
            return False

        # Check if the number is not in the same column
        if num in [board[i][col] for i in range(GRID_SIZE)]:
            return False

        start_row = BOX_ROWS * (row // BOX_ROWS) if GRID_SIZE != 3 else 0
        start_col = BOX_COLS * (col // BOX_COLS) if GRID_SIZE != 3 else 0
        end_rows = start_row + BOX_ROWS if GRID_SIZE != 3 else 3
        end_cols = start_col + BOX_COLS if GRID_SIZE != 3 else 3

        for i in range(start_row, end_rows):
            for j in range(start_col, end_cols):
                if board[i][j] == num:
                    return False

        return True

    def solve_sudoku(board):
        if GRID_SIZE == 9:
            numbers_range = range(1, GRID_SIZE + 1)
        elif GRID_SIZE == 6:
            numbers_range = range(1, GRID_SIZE + 1)
        else:
            numbers_range = range(1, 10)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 0:
                    for num in random.sample(numbers_range, len(numbers_range)):
                        if is_valid_move(board, row, col, num):
                            board[row][col] = num
                            if solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    # Start with an empty Sudoku board
    if GRID_SIZE == 3:
        puzzle_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    else:
        puzzle_board = [[0 for _ in range(BOX_COLS * BOX_ROWS)] for _ in range(BOX_ROWS * BOX_COLS)]

    # Solve the Sudoku puzzle to get a valid solution
    solve_sudoku(puzzle_board)

    # Create a copy of the solution to generate the puzzle
    puzzle_copy = [row[:] for row in puzzle_board]

    # Remove numbers to create the puzzle
    if GRID_SIZE == 3:
        low = 5
        height = 7
    elif GRID_SIZE == 6:
        low = 18
        height = 30
    else:
        low = 40
        height = 60
    to_remove = random.randint(low, height)
    for _ in range(to_remove):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while puzzle_copy[row][col] == 0:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        puzzle_copy[row][col] = 0

    # Create a boolean grid to indicate fixed cells
    fixed_cells = [[True if puzzle_copy[row][col] != 0 else False for col in range(GRID_SIZE)] for row in
                   range(GRID_SIZE)]

    return puzzle_copy, fixed_cells


# Check if the number is not in the same 3x3 grid
def collision_row(board, row, col, num):
    for i in range(GRID_SIZE):
        if num == board[row][i]:
            return row, i

    return -1, -1


# Check if the number is not in the same column
def collision_col(board, row, col, num):
    for i in range(GRID_SIZE):
        if num == board[i][col]:
            return i, col

    return -1, -1


def collision_box(board, row, col, num):
    start_row = BOX_ROWS * (row // BOX_ROWS) if GRID_SIZE != 3 else 0
    start_col = BOX_COLS * (col // BOX_COLS) if GRID_SIZE != 3 else 0
    end_rows = start_row + BOX_ROWS if GRID_SIZE != 3 else 3
    end_cols = start_col + BOX_COLS if GRID_SIZE != 3 else 3
    for i in range(start_row, end_rows):
        for j in range(start_col, end_cols):
            if board[i][j] == num:
                return i, j

    return -1, -1


def draw_grid(board, fixed_cells, violate, screen):
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
            if GRID_SIZE == 9:
                box_border_thickness = 4
                rows_per_thicker_border = 3
                cols_per_thicker_border = 3
            elif GRID_SIZE == 6:
                box_border_thickness = 4
                rows_per_thicker_border = 2
                cols_per_thicker_border = 3
            else:
                box_border_thickness = 2
                rows_per_thicker_border = 2
                cols_per_thicker_border = 2

            if i % rows_per_thicker_border == 0 and i > 0:
                pygame.draw.line(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE),
                                 ((j + GRID_SIZE // cols_per_thicker_border) * CELL_SIZE, i * CELL_SIZE),
                                 box_border_thickness)  # Top

            if j % cols_per_thicker_border == 0 and 0 < j < GRID_SIZE - 1:
                pygame.draw.line(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE),
                                 (j * CELL_SIZE, (i + GRID_SIZE // rows_per_thicker_border) * CELL_SIZE),
                                 box_border_thickness)  # Left

            # Draw thicker right border for 6x6 grid (right of col index 0, 2, and 3)
            if GRID_SIZE == 6 and j in [0, 2, 3] and j < GRID_SIZE - 1:
                pygame.draw.line(screen, BLACK, ((j + 1) * CELL_SIZE, i * CELL_SIZE),
                                 ((j + 1) * CELL_SIZE, (i + GRID_SIZE // rows_per_thicker_border) * CELL_SIZE),
                                 box_border_thickness)  # Right

            # Draw thicker bottom border for 6x6 grid (top of line 3 or 2 bottom)
            if GRID_SIZE == 6 and i % 2 == 1 and i > 0:
                pygame.draw.line(screen, BLACK, (j * CELL_SIZE, (i + 1) * CELL_SIZE),
                                 ((j + GRID_SIZE // cols_per_thicker_border) * CELL_SIZE, (i + 1) * CELL_SIZE),
                                 box_border_thickness)  # Bottom

            font = pygame.font.Font(None, 36)
            if board[i][j] != 0:
                if tuple([i, j]) in violate:
                    text_color = RED
                else:
                    text_color = BLACK
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
                if (e[0] * GRID_SIZE + e[1]) not in d:
                    violate.remove(e)
                elif tuple([row, col]) in d[(e[0] * GRID_SIZE + e[1])]:
                    d[(e[0] * GRID_SIZE + e[1])].remove(tuple([row, col]))
                    if not d[(e[0] * GRID_SIZE + e[1])]:
                        violate.remove(e)


def choose_difficulty_level():
    global GRID_SIZE, BOX_ROWS, BOX_COLS, SCREEN_HEIGHT, CELL_SIZE, MAX_NUMBER, FULL_BOARD
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.Font(None, 36)
    text = font.render("Choose Difficulty Level:", True, BLACK)
    easy_text = font.render("Easy (3x3)", True, BLACK)
    medium_text = font.render("Medium (6x6)", True, BLACK)
    hard_text = font.render("Hard (9x9)", True, BLACK)
    options = [easy_text, medium_text, hard_text]
    selected_option = 0
    chose = False

    while not chose:
        screen.fill(WHITE)
        screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, 100))

        # Draw options with highlighting on the selected option
        for i, option in enumerate(options):
            x = (SCREEN_WIDTH - option.get_width()) // 2
            y = 200 + i * (option.get_height() + 20)
            if i == selected_option:
                pygame.draw.rect(screen, BLACK, (x - 10, y - 5, option.get_width() + 20, option.get_height() + 10), 2)
            screen.blit(option, (x, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        GRID_SIZE = 3
                    elif selected_option == 1:
                        GRID_SIZE = 6
                    elif selected_option == 2:
                        GRID_SIZE = 9
                    chose = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    x = (SCREEN_WIDTH - option.get_width()) // 2
                    y = 200 + i * (option.get_height() + 20)
                    if x <= pos[0] <= x + option.get_width() and y <= pos[1] <= y + option.get_height():
                        selected_option = i
                        GRID_SIZE = [3, 6, 9][selected_option]
                        chose = True

    if GRID_SIZE == 6:
        BOX_ROWS = 2
        BOX_COLS = 3
        MAX_NUMBER = 6
    else:
        BOX_ROWS = GRID_SIZE // 3
        BOX_COLS = GRID_SIZE // 3
        MAX_NUMBER = 9

    CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
    FULL_BOARD = GRID_SIZE * GRID_SIZE
    SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE


def main():
    pygame.font.init()

    # Initialize Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    sudoku_board, fixed_cells = generate_sudoku_puzzle()
    selected = -math.inf, -math.inf
    violate = set()
    d = {}
    counter = 0
    for row in fixed_cells:
        for cell in row:
            if cell:
                counter += 1
    while True:
        screen.fill(WHITE)
        draw_grid(sudoku_board, fixed_cells, violate, screen)

        if counter == FULL_BOARD and not violate:
            font = pygame.font.Font(None, 48)
            win_text1 = font.render("Well Done!", True, RED)
            win_text2 = font.render("Puzzle Completed!", True, RED)
            play_again_text = font.render("Press Enter to Play Again", True, BLUE)

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
            text1_y = (
                              SCREEN_HEIGHT - border_win_text1.get_height() - border_win_text2.get_height() - border_play_again_text.get_height() - 40) // 2
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
                        choose_difficulty_level()
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        sudoku_board, fixed_cells = generate_sudoku_puzzle()
                        selected = -math.inf, -math.inf
                        violate = set()
                        d = {}
                        counter = 0
                        for row in fixed_cells:
                            for cell in row:
                                if cell:
                                    counter += 1

                    if event.key == pygame.K_RETURN:
                        sudoku_board, fixed_cells = generate_sudoku_puzzle()
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
                    choose_difficulty_level()
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    sudoku_board, fixed_cells = generate_sudoku_puzzle()
                    selected = -math.inf, -math.inf
                    violate = set()
                    d = {}
                    counter = 0
                    for row in fixed_cells:
                        for cell in row:
                            if cell:
                                counter += 1

                row, col = selected
                if event.key == pygame.K_UP and row > 0:
                    selected = (row - 1, col)
                elif event.key == pygame.K_DOWN and row < GRID_SIZE - 1:
                    selected = (row + 1, col)
                elif event.key == pygame.K_LEFT and col > 0:
                    selected = (row, col - 1)
                elif event.key == pygame.K_RIGHT and col < GRID_SIZE - 1:
                    selected = (row, col + 1)
                elif event.unicode.isdigit() and 1 <= int(event.unicode) <= MAX_NUMBER and row >= 0 and not \
                        fixed_cells[row][col]:
                    number = int(event.unicode)
                    if number == sudoku_board[row][col]:
                        continue
                    if sudoku_board[row][col] == 0:
                        counter += 1
                    x1, y1 = collision_row(sudoku_board, row, col, number)
                    x2, y2 = collision_col(sudoku_board, row, col, number)
                    x3, y3 = collision_box(sudoku_board, row, col, number)

                    loc = row * GRID_SIZE + col
                    if loc not in d:
                        d[loc] = set()

                    copy = d[loc].copy()
                    remove(loc, d, violate, copy, row, col)

                    if x1 >= 0:
                        violate.add(tuple([x1, y1]))
                        d[loc].add(tuple([x1, y1]))
                        if (x1 * GRID_SIZE + y1) in d:
                            d[(x1 * GRID_SIZE + y1)].add(tuple([row, col]))
                    if x2 >= 0:
                        violate.add(tuple([x2, y2]))
                        d[loc].add(tuple([x2, y2]))
                        if (x2 * GRID_SIZE + y2) in d:
                            d[(x2 * GRID_SIZE + y2)].add(tuple([row, col]))
                    if x3 >= 0:
                        violate.add(tuple([x3, y3]))
                        d[loc].add(tuple([x3, y3]))
                        if (x3 * GRID_SIZE + y3) in d:
                            d[(x3 * GRID_SIZE + y3)].add(tuple([row, col]))
                    if x1 >= 0 or x2 >= 0 or x3 >= 0:
                        violate.add(tuple([row, col]))

                    e = tuple([row, col])
                    if not d[loc] and e in violate:
                        violate.remove(e)

                    sudoku_board[row][col] = number

                elif event.key == pygame.K_BACKSPACE and not fixed_cells[row][col]:
                    loc = row * GRID_SIZE + col
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
    pygame.display.set_caption("Sudoku by Ofek Yaloz")
    choose_difficulty_level()
    main()
