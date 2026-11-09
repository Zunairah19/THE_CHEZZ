import math
import pygame
import chess
from computer_player import choose_move
from menu import show_menu

pygame.init()

WIDTH, HEIGHT = 900, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE CHEZZ")
clock = pygame.time.Clock()

# Pale pink gingham background
wallpaper = (255, 250, 252)
gingham_pink = (255, 230, 239)

# Chessboard and frame colors
cream_square = (255, 251, 248)
pink_square = (232, 183, 202)
deep_rose = (158, 83, 112)
frame_light = (224, 159, 184)

# Background bows and hearts
bow_outline = (238, 112, 157)
bow_fill = (255, 216, 230)
bow_shade = (246, 173, 201)
bow_highlight = (255, 241, 246)
heart_color = (242, 162, 191)

# Fonts
piece_font = pygame.font.SysFont("segoeuisymbol", 58)
title_font = pygame.font.SysFont("segoescript", 52)
subtitle_font = pygame.font.SysFont("segoescript", 21)
pixel_font = pygame.font.SysFont("consolas", 19, bold=True)
small_pixel_font = pygame.font.SysFont("consolas", 14, bold=True)
win_font = pygame.font.SysFont("segoescript", 76)

# Chessboard layout
board_size = 576
square_size = board_size // 8
board_x = (WIDTH - board_size) // 2
board_y = 138

# Game state
game = chess.Board()
selected_square = None
capture_aura_square = None
capture_aura_start = 0
AURA_DURATION = 2200


def draw_heart(surface, x, y, size, color):
    radius = max(2, size // 3)
    pygame.draw.circle(surface, color, (x - radius, y - radius // 2), radius)
    pygame.draw.circle(surface, color, (x + radius, y - radius // 2), radius)
    pygame.draw.polygon(
        surface,
        color,
        [
            (x - size // 2, y),
            (x + size // 2, y),
            (x, y + size // 2),
        ],
    )


def draw_round_line(surface, color, points, width):
    """Draw a ribbon line with rounded joins and ends."""
    pygame.draw.lines(surface, color, False, points, width)
    radius = max(2, width // 2)
    for point in points:
        pygame.draw.circle(surface, color, point, radius)


def draw_bow(surface, x, y, size=20):
    """Draw a rounded bow on the gingham background."""
    loop_width = size
    loop_height = max(10, int(size * 0.68))

    left_loop = pygame.Rect(
        x - size - 3,
        y - loop_height // 2,
        loop_width,
        loop_height,
    )
    right_loop = pygame.Rect(
        x + 3,
        y - loop_height // 2,
        loop_width,
        loop_height,
    )

    left_tail = [
        (x - 2, y + 3),
        (x - size // 4, y + size // 2),
        (x - size // 2, y + size),
    ]
    right_tail = [
        (x + 2, y + 3),
        (x + size // 4, y + size // 2),
        (x + size // 2, y + size),
    ]

    tail_width = max(5, size // 4)
    draw_round_line(surface, bow_outline, left_tail, tail_width)
    draw_round_line(surface, bow_outline, right_tail, tail_width)
    draw_round_line(surface, bow_fill, left_tail, max(2, tail_width - 3))
    draw_round_line(surface, bow_fill, right_tail, max(2, tail_width - 3))

    for loop in (left_loop, right_loop):
        pygame.draw.ellipse(surface, bow_outline, loop)
        pygame.draw.ellipse(surface, bow_fill, loop.inflate(-3, -3))

    pygame.draw.ellipse(
        surface,
        bow_shade,
        (x - size // 2 - 2, y - loop_height // 3, size // 3, loop_height // 2),
    )
    pygame.draw.ellipse(
        surface,
        bow_shade,
        (x + size // 6, y - loop_height // 3, size // 3, loop_height // 2),
    )
    pygame.draw.ellipse(
        surface,
        bow_highlight,
        (x - size + 3, y - loop_height // 2 + 3, size // 2, 3),
    )
    pygame.draw.ellipse(
        surface,
        bow_highlight,
        (x + 5, y - loop_height // 2 + 3, size // 2, 3),
    )

    pygame.draw.circle(surface, bow_outline, (x, y), max(4, size // 5))
    pygame.draw.circle(surface, bow_fill, (x, y), max(3, size // 6))
    pygame.draw.circle(surface, bow_highlight, (x - 1, y - 2), 2)


def draw_wallpaper(surface):
    """Draw the small gingham, bow, and heart background."""
    surface.fill(wallpaper)

    tile_size = 12
    for row in range((HEIGHT // tile_size) + 1):
        for col in range((WIDTH // tile_size) + 1):
            if (row + col) % 2 == 0:
                pygame.draw.rect(
                    surface,
                    gingham_pink,
                    (
                        col * tile_size,
                        row * tile_size,
                        tile_size,
                        tile_size,
                    ),
                )

    row_number = 0
    for y in range(28, HEIGHT, 118):
        offset = 64 if row_number % 2 else 0
        for x in range(30 + offset, WIDTH, 132):
            draw_bow(surface, x, y, 20)
        row_number += 1

    heart_positions = [
        (88, 78, 10),
        (810, 76, 9),
        (70, 320, 9),
        (830, 330, 10),
        (73, 540, 9),
        (820, 555, 10),
    ]
    for x, y, size in heart_positions:
        draw_heart(surface, x, y, size, heart_color)


wallpaper_surface = pygame.Surface((WIDTH, HEIGHT))
draw_wallpaper(wallpaper_surface)


def draw_board():
    """Draw board squares and soft box highlights."""
    for row in range(8):
        for col in range(8):
            square_rect = pygame.Rect(
                board_x + col * square_size,
                board_y + row * square_size,
                square_size,
                square_size,
            )
            color = cream_square if (row + col) % 2 == 0 else pink_square
            pygame.draw.rect(screen, color, square_rect)

            chess_square = chess.square(col, 7 - row)

            if selected_square == chess_square:
                tint = pygame.Surface(
                    (square_size, square_size),
                    pygame.SRCALPHA,
                )
                tint.fill((255, 220, 234, 75))
                screen.blit(tint, square_rect)
                pygame.draw.rect(
                    screen,
                    frame_light,
                    square_rect,
                    width=3,
                )

    if selected_square is not None:
        destinations = {
            move.to_square
            for move in game.legal_moves
            if move.from_square == selected_square
        }

        for destination in destinations:
            col = chess.square_file(destination)
            row = 7 - chess.square_rank(destination)
            square_rect = pygame.Rect(
                board_x + col * square_size,
                board_y + row * square_size,
                square_size,
                square_size,
            )

            tint = pygame.Surface(
                (square_size, square_size),
                pygame.SRCALPHA,
            )
            tint.fill((255, 235, 243, 100))
            screen.blit(tint, square_rect)
            pygame.draw.rect(
                screen,
                (236, 170, 196),
                square_rect,
                width=2,
            )


def draw_capture_aura():
    """Show a brief pink ring around the piece that captured."""
    if capture_aura_square is None:
        return

    elapsed = pygame.time.get_ticks() - capture_aura_start
    if elapsed >= AURA_DURATION:
        return

    pulse = (math.sin(elapsed / 120) + 1) / 2
    fade = 1 - elapsed / AURA_DURATION
    radius = int(28 + pulse * 4)
    alpha = int(135 * fade)

    col = chess.square_file(capture_aura_square)
    row = 7 - chess.square_rank(capture_aura_square)

    aura = pygame.Surface(
        (square_size, square_size),
        pygame.SRCALPHA,
    )
    center = (square_size // 2, square_size // 2)

    pygame.draw.circle(
        aura,
        (255, 196, 220, int(alpha * 0.18)),
        center,
        radius - 3,
    )
    pygame.draw.circle(
        aura,
        (255, 226, 238, alpha),
        center,
        radius,
        width=3,
    )
    pygame.draw.circle(
        aura,
        (239, 151, 187, int(alpha * 0.7)),
        center,
        radius - 6,
        width=1,
    )

    screen.blit(
        aura,
        (
            board_x + col * square_size,
            board_y + row * square_size,
        ),
    )


def draw_check_highlight():
    """Pulse a red tint over the checked king's full square."""
    if not game.is_check():
        return

    king_square = game.king(game.turn)
    if king_square is None:
        return

    col = chess.square_file(king_square)
    row = 7 - chess.square_rank(king_square)
    square_rect = pygame.Rect(
        board_x + col * square_size,
        board_y + row * square_size,
        square_size,
        square_size,
    )

    pulse = (math.sin(pygame.time.get_ticks() / 180) + 1) / 2
    alpha = int(45 + pulse * 75)

    highlight = pygame.Surface(
        (square_size, square_size),
        pygame.SRCALPHA,
    )
    highlight.fill((235, 45, 75, alpha))
    pygame.draw.rect(
        highlight,
        (210, 35, 65, min(220, alpha + 70)),
        highlight.get_rect(),
        width=4,
        border_radius=5,
    )
    screen.blit(highlight, square_rect)


def draw_pieces():
    """Draw classic pink-and-white chess symbols."""
    symbols = {
        (chess.PAWN, chess.WHITE): "♙",
        (chess.KNIGHT, chess.WHITE): "♘",
        (chess.BISHOP, chess.WHITE): "♗",
        (chess.ROOK, chess.WHITE): "♖",
        (chess.QUEEN, chess.WHITE): "♕",
        (chess.KING, chess.WHITE): "♔",
        (chess.PAWN, chess.BLACK): "♟",
        (chess.KNIGHT, chess.BLACK): "♞",
        (chess.BISHOP, chess.BLACK): "♝",
        (chess.ROOK, chess.BLACK): "♜",
        (chess.QUEEN, chess.BLACK): "♛",
        (chess.KING, chess.BLACK): "♚",
    }

    outline_offsets = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, -1), (-1, 1), (1, 1),
    ]

    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            chess_piece = game.piece_at(square)
            if chess_piece is None:
                continue

            symbol = symbols[(chess_piece.piece_type, chess_piece.color)]

            if chess_piece.color == chess.WHITE:
                piece_color = cream_square
                outline_color = deep_rose
            else:
                piece_color = deep_rose
                outline_color = cream_square

            center = (
                board_x + col * square_size + square_size // 2,
                board_y + row * square_size + square_size // 2,
            )

            piece_image = piece_font.render(symbol, True, piece_color)
            outline_image = piece_font.render(symbol, True, outline_color)
            piece_rect = piece_image.get_rect(center=center)
            outline_rect = outline_image.get_rect(center=center)

            if square == selected_square:
                glow_image = piece_font.render(
                    symbol,
                    True,
                    (255, 204, 224),
                )
                glow_rect = glow_image.get_rect(center=center)

                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if 2 <= max(abs(dx), abs(dy)) <= 3:
                            screen.blit(glow_image, glow_rect.move(dx, dy))

            for dx, dy in outline_offsets:
                screen.blit(
                    outline_image,
                    outline_rect.move(dx, dy),
                )

            screen.blit(piece_image, piece_rect)


def draw_game(mode, difficulty=None):
    screen.blit(wallpaper_surface, (0, 0))

    title = title_font.render("The Chezz", True, deep_rose)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 48)))

    if mode == "two_player":
        label = "TWO PLAYER"
    else:
        label = f"VS COMPUTER - {difficulty.upper()}"

    mode_label = pixel_font.render(label, True, deep_rose)
    screen.blit(mode_label, mode_label.get_rect(center=(WIDTH // 2, 104)))

    esc_hint = small_pixel_font.render("ESC: MAIN MENU", True, deep_rose)
    screen.blit(esc_hint, (WIDTH - esc_hint.get_width() - 22, 18))

    draw_board()
    draw_capture_aura()
    draw_check_highlight()
    draw_pieces()

    pygame.draw.rect(
        screen,
        deep_rose,
        (board_x - 4, board_y - 4, board_size + 8, board_size + 8),
        width=2,
        border_radius=8,
    )
    pygame.draw.rect(
        screen,
        frame_light,
        (board_x - 8, board_y - 8, board_size + 16, board_size + 16),
        width=1,
        border_radius=11,
    )


def draw_pixel_rose(surface, center_x, center_y, pale=False):
    """Draw a pixel rose with leaves for the winner screen."""
    cell = 7
    pattern = [
        "0011100",
        "0122210",
        "1233321",
        "1233321",
        "0122210",
        "0011100",
    ]

    if pale:
        colors = {
            "1": (255, 247, 250),
            "2": (255, 222, 233),
            "3": (255, 194, 215),
        }
        leaf_outline = (112, 79, 92)
        leaf_fill = (160, 207, 156)
    else:
        colors = {
            "1": (174, 53, 98),
            "2": (235, 111, 157),
            "3": (250, 157, 190),
        }
        leaf_outline = (76, 133, 91)
        leaf_fill = (132, 181, 123)

    start_x = center_x - (len(pattern[0]) * cell) // 2
    start_y = center_y - 42

    for row, line in enumerate(pattern):
        for col, pixel in enumerate(line):
            if pixel != "0":
                pygame.draw.rect(
                    surface,
                    colors[pixel],
                    (
                        start_x + col * cell,
                        start_y + row * cell,
                        cell,
                        cell,
                    ),
                )

    pygame.draw.rect(
        surface,
        leaf_outline,
        (center_x - 3, center_y, 7, 34),
    )
    pygame.draw.rect(
        surface,
        leaf_fill,
        (center_x - 1, center_y + 2, 3, 29),
    )
    pygame.draw.rect(
        surface,
        leaf_outline,
        (center_x - 23, center_y + 9, 21, 8),
    )
    pygame.draw.rect(
        surface,
        leaf_fill,
        (center_x - 20, center_y + 11, 15, 4),
    )
    pygame.draw.rect(
        surface,
        leaf_outline,
        (center_x + 2, center_y + 17, 21, 8),
    )
    pygame.draw.rect(
        surface,
        leaf_fill,
        (center_x + 5, center_y + 19, 15, 4),
    )


def draw_game_over():
    """Show the winning player's color and message after checkmate."""
    if game.is_checkmate():
        winner = not game.turn
        white_won = winner == chess.WHITE
        message = "WHITE WINS" if white_won else "PINK WINS"

        if white_won:
            background = (255, 251, 253)
            text_color = deep_rose
            border_color = frame_light
        else:
            background = (237, 132, 172)
            text_color = (255, 250, 252)
            border_color = (170, 55, 103)
    else:
        white_won = False
        message = "DRAW"
        background = (255, 241, 246)
        text_color = deep_rose
        border_color = frame_light

    screen.fill(background)

    # Small menu hint in the upper-right corner
    esc_hint = small_pixel_font.render("ESC: MAIN MENU", True, text_color)
    screen.blit(
        esc_hint,
        (WIDTH - esc_hint.get_width() - 22, 18),
    )

    pygame.draw.rect(
        screen,
        border_color,
        (100, 90, WIDTH - 200, HEIGHT - 180),
        width=7,
    )
    pygame.draw.rect(
        screen,
        border_color,
        (115, 105, WIDTH - 230, HEIGHT - 210),
        width=2,
    )

    heading = win_font.render(message, True, text_color)
    screen.blit(heading, heading.get_rect(center=(WIDTH // 2, 250)))

    # Pixel roses below the winner message
    draw_pixel_rose(
        screen,
        WIDTH // 2 - 60,
        385,
        pale=not white_won,
    )
    draw_pixel_rose(
        screen,
        WIDTH // 2 + 60,
        385,
        pale=not white_won,
    )

    replay_text = pixel_font.render("R: PLAY AGAIN", True, text_color)
    screen.blit(
        replay_text,
        replay_text.get_rect(center=(WIDTH // 2, 550)),
    )





def play_game(mode, difficulty=None):
    """Run one chess game. Return to the menu when Escape is pressed."""
    global game, selected_square, capture_aura_square, capture_aura_start

    game = chess.Board()
    selected_square = None
    capture_aura_square = None
    capture_aura_start = 0
    ai_move_at = None
    running = True

    while running:
        now = pygame.time.get_ticks()

        # The computer always plays Black. Give the board a brief moment to
        # show the human's move before the computer responds.
        if (
            mode == "vs_computer"
            and game.turn == chess.BLACK
            and not game.is_game_over()
        ):
            if ai_move_at is None:
                ai_move_at = now + 350
            elif now >= ai_move_at:
                computer_move = choose_move(game, difficulty)
                if computer_move is not None and computer_move in game.legal_moves:
                    was_capture = game.is_capture(computer_move)
                    game.push(computer_move)
                    if was_capture:
                        capture_aura_square = computer_move.to_square
                        capture_aura_start = pygame.time.get_ticks()
                ai_move_at = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if game.is_game_over() and event.key == pygame.K_r:
                    game = chess.Board()
                    selected_square = None
                    capture_aura_square = None
                    ai_move_at = None

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and not game.is_game_over()
            ):
                # In computer mode, the player controls White; Black is the AI.
                human_turn = mode == "two_player" or game.turn == chess.WHITE
                if not human_turn:
                    continue

                mouse_x, mouse_y = event.pos
                if not (
                    board_x <= mouse_x < board_x + board_size
                    and board_y <= mouse_y < board_y + board_size
                ):
                    continue

                col = (mouse_x - board_x) // square_size
                row = (mouse_y - board_y) // square_size
                clicked_square = chess.square(col, 7 - row)
                clicked_piece = game.piece_at(clicked_square)

                if selected_square is None:
                    if clicked_piece and clicked_piece.color == game.turn:
                        selected_square = clicked_square
                else:
                    moving_piece = game.piece_at(selected_square)
                    move = chess.Move(selected_square, clicked_square)

                    # Promote a pawn to a queen automatically.
                    if (
                        moving_piece
                        and moving_piece.piece_type == chess.PAWN
                        and chess.square_rank(clicked_square) in (0, 7)
                    ):
                        move = chess.Move(
                            selected_square,
                            clicked_square,
                            promotion=chess.QUEEN,
                        )

                    if move in game.legal_moves:
                        was_capture = game.is_capture(move)
                        game.push(move)
                        selected_square = None
                        if was_capture:
                            capture_aura_square = move.to_square
                            capture_aura_start = pygame.time.get_ticks()
                        if mode == "vs_computer" and not game.is_game_over():
                            ai_move_at = pygame.time.get_ticks() + 350
                    elif clicked_piece and clicked_piece.color == game.turn:
                        selected_square = clicked_square
                    else:
                        selected_square = None

        if game.is_game_over():
            draw_game_over()
        else:
            draw_game(mode, difficulty)

        pygame.display.flip()
        clock.tick(60)

    return "menu"


def main():
    """Show the menu first, then open the selected chess game."""
    app_running = True

    while app_running:
        choice = show_menu(screen)

        if choice is None or choice == "quit":
            break

        if choice == "two_player":
            result = play_game("two_player")
        elif isinstance(choice, str) and choice.startswith("vs_computer_"):
            difficulty = choice.removeprefix("vs_computer_").lower()
            if difficulty not in ("easy", "medium", "hard"):
                difficulty = "easy"
            result = play_game("vs_computer", difficulty)
        else:
            # An unrecognized menu result should return safely to the menu.
            continue

        if result == "quit":
            app_running = False

    pygame.quit()


if __name__ == "__main__":
    main()
