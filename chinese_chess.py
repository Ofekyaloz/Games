import pygame as pg

# Define colors
BACKGROUND = (242, 213, 171)
EMPTY_CELL = (213, 192, 155)
SELECT = (255, 255, 255)

# Constants for board dimensions and spacing
H_MARGIN_DISTANCE = 50
V_MARGIN_DISTANCE = 20
CIRCLE_RADIUS = 15
CIRCLE_DIAMETER = 2 * CIRCLE_RADIUS
H_SPACING = 20
V_SPACING = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Define menu colors
MENU_BACKGROUND = (200, 200, 200)
MENU_TEXT_COLOR = (0, 0, 0)
MENU_BUTTON_COLOR = (100, 100, 100)
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50
MENU_BUTTON_MARGIN = 20
PLAYERS_COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255)  # Cyan
]
BASES = [
    [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3)],
    [(13, 0), (13, 1), (13, 2), (13, 3), (14, 0), (14, 1), (14, 2), (15, 0), (15, 1), (16, 0)],
    [(4, 0), (4, 1), (4, 2), (4, 3), (5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (7, 0)],
    [(9, 9), (10, 9), (10, 10), (11, 9), (11, 10), (11, 11), (12, 9), (12, 10), (12, 11), (12, 12)],
    [(4, 9), (4, 10), (4, 11), (4, 12), (5, 9), (5, 10), (5, 11), (6, 9), (6, 10), (7, 9)],
    [(9, 0), (10, 0), (10, 1), (11, 0), (11, 1), (11, 2), (12, 0), (12, 1), (12, 2), (12, 3)]
]

# Initialize the number of players
num_players = 2

# Initialize selected circle position
selected_row, selected_col = None, None


def draw_board(board, display_surface, board_pieces):
    display_surface.fill(BACKGROUND)

    y_coord = V_MARGIN_DISTANCE + CIRCLE_RADIUS

    for row_index, row in enumerate(board):
        circle_count = row
        total_circle_width = circle_count * (CIRCLE_DIAMETER + H_SPACING) - H_SPACING
        x_offset = (SCREEN_WIDTH - total_circle_width) / 2

        x_coord = H_MARGIN_DISTANCE + x_offset

        for col_index in range(circle_count):
            color = board_pieces[row_index][col_index]
            if color:
                color_circle(display_surface, color, x_coord, y_coord)
            else:
                color_circle(display_surface, EMPTY_CELL, x_coord, y_coord)
            x_coord += CIRCLE_DIAMETER + H_SPACING

        y_coord += CIRCLE_DIAMETER + V_SPACING


def color_circle(display_surface, color, x_coord, y_coord):
    pg.draw.circle(display_surface, color, (int(x_coord), int(y_coord)), CIRCLE_RADIUS, 0)


def draw_menu(display_surface, start_y):
    display_surface.fill(MENU_BACKGROUND)

    font = pg.font.Font(None, 36)
    text = font.render("Select Number of Players:", True, MENU_TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Title at the top
    display_surface.blit(text, text_rect)

    # Calculate the total height of the buttons
    options = [2, 3, 4, 6]  # Define options list
    for i, num in enumerate(options):
        button_rect = pg.Rect(
            (SCREEN_WIDTH - MENU_BUTTON_WIDTH) // 2,
            start_y + i * (MENU_BUTTON_HEIGHT + MENU_BUTTON_MARGIN),  # Adjusted position calculation
            MENU_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT
        )
        button_color = MENU_BUTTON_COLOR
        pg.draw.rect(display_surface, button_color, button_rect)

        font = pg.font.Font(None, 30)
        text = font.render(f"{num} Players", True, MENU_TEXT_COLOR)
        text_rect = text.get_rect(center=button_rect.center)
        display_surface.blit(text, text_rect)


def main_menu():
    global num_players
    total_buttons_height = (MENU_BUTTON_HEIGHT + MENU_BUTTON_MARGIN) * 5
    start_y = (SCREEN_HEIGHT - total_buttons_height) // 2  # Calculate start_y
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            elif event.type == pg.MOUSEBUTTONUP:
                options = [2, 3, 4, 6]
                mouse_pos = pg.mouse.get_pos()
                for i in range(len(options)):
                    button_rect = pg.Rect(
                        (SCREEN_WIDTH - MENU_BUTTON_WIDTH) // 2,
                        start_y + i * (MENU_BUTTON_HEIGHT + MENU_BUTTON_MARGIN),
                        MENU_BUTTON_WIDTH,
                        MENU_BUTTON_HEIGHT
                    )
                    if button_rect.collidepoint(mouse_pos):
                        num_players = options[i]
                        running = False

        draw_menu(screen, start_y)
        pg.display.flip()

    # Close the main menu and show the board
    screen.fill(BACKGROUND)  # Clear the screen
    # Proceed to draw the board and continue the game
    # (code to draw the board and start the game would go here)


def get_clicked_circle(mouse_pos):
    """
    Returns the row, column, and color of the clicked circle on the board.
    """
    y_coord = V_MARGIN_DISTANCE + CIRCLE_RADIUS
    for row_index, row in enumerate(board):
        circle_count = row
        total_circle_width = circle_count * (CIRCLE_DIAMETER + H_SPACING) - H_SPACING
        x_offset = (SCREEN_WIDTH - total_circle_width) / 2
        x_coord = H_MARGIN_DISTANCE + x_offset

        for col_index in range(circle_count):
            if pg.Rect(x_coord - CIRCLE_RADIUS, y_coord - CIRCLE_RADIUS,
                       CIRCLE_DIAMETER, CIRCLE_DIAMETER).collidepoint(mouse_pos):
                return row_index, col_index, board_pieces[row_index][col_index]
            x_coord += CIRCLE_DIAMETER + H_SPACING

        y_coord += CIRCLE_DIAMETER + V_SPACING

    return None, None, None


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Chinese Checkers')
    main_menu()

    # Create a Pygame window

    # Define the star-shaped board
    board = [1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1]
    board_pieces = [[EMPTY_CELL] * i for i in board]

    for player in range(num_players):
        for i, j in BASES[player]:
            board_pieces[i][j] = PLAYERS_COLORS[player]

    clock = pg.time.Clock()
    turn = 0  # Initialize the turn counter
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

            elif event.type == pg.MOUSEBUTTONDOWN and selected_row is not None and selected_col is not None:
                mouse_pos = pg.mouse.get_pos()
                new_row, new_col, color = get_clicked_circle(mouse_pos)
                if new_row is not None and new_col is not None:
                    if board_pieces[new_row][new_col] == SELECT:
                        board_pieces[new_row][new_col] = PLAYERS_COLORS[turn]
                        selected_row, selected_col = None, None

                    elif abs(new_row - selected_row) <= 1:  # Check if the new position is adjacent
                        if board_pieces[new_row][new_col] == EMPTY_CELL:  # Check if the new position is empty
                            board_pieces[new_row][new_col] = PLAYERS_COLORS[turn]  # Move the white circle
                            board_pieces[selected_row][selected_col] = EMPTY_CELL  # Empty the previous position
                            turn = (turn + 1) % num_players  # Increment turn
                            selected_row, selected_col = None, None  # Reset the selected position
            elif event.type == pg.MOUSEBUTTONDOWN:  # Check for mouse click
                mouse_pos = pg.mouse.get_pos()
                row, col, color = get_clicked_circle(mouse_pos)
                if row is not None and col is not None:
                    if color == PLAYERS_COLORS[turn]:  # Check if it's the current player's color
                        print("Clicked Circle:", row, col)
                        selected_row, selected_col = row, col  # Store the position of the selected circle
                        board_pieces[row][col] = SELECT  # Change the color to white
                        # turn = (turn + 1) % num_players  # Increment turn
        # Draw the board
        draw_board(board, screen, board_pieces)

        # Display the turn ID on the top left of the screen
        font = pg.font.Font(None, 36)
        text = font.render(f"Turn: {turn + 1}", True, (0, 0, 0))
        screen.blit(text, (20, 20))

        # Update the display
        pg.display.flip()
        clock.tick(30)

    # Quit Pygame
    pg.quit()
