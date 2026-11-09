import math
import pygame


def draw_bow(surface, x, y):
    outline = (198, 83, 124)
    fill = (255, 216, 230)
    highlight = (255, 241, 246)

    pygame.draw.ellipse(surface, outline, (x - 64, y - 18, 62, 34), 4)
    pygame.draw.ellipse(surface, outline, (x + 2, y - 18, 62, 34), 4)

    pygame.draw.ellipse(surface, fill, (x - 58, y - 13, 49, 24))
    pygame.draw.ellipse(surface, fill, (x + 9, y - 13, 49, 24))

    pygame.draw.ellipse(surface, highlight, (x - 51, y - 10, 22, 5))
    pygame.draw.ellipse(surface, highlight, (x + 29, y - 10, 22, 5))

    pygame.draw.circle(surface, outline, (x, y), 9)
    pygame.draw.circle(surface, fill, (x, y), 6)

    pygame.draw.lines(
        surface,
        outline,
        False,
        [(x - 3, y + 6), (x - 16, y + 24), (x - 28, y + 42)],
        5,
    )
    pygame.draw.lines(
        surface,
        outline,
        False,
        [(x + 3, y + 6), (x + 16, y + 24), (x + 28, y + 42)],
        5,
    )


def draw_menu_frame(surface):
    color = (198, 83, 124)
    left, right = 150, 750
    top, bottom = 95, 700

    left_points = []
    right_points = []
    for y in range(top + 20, bottom - 15, 4):
        wave = int(6 * math.sin((y - top) / 42))
        left_points.append((left + wave, y))
        right_points.append((right - wave, y))

    bottom_points = []
    for x in range(left + 20, right - 20, 4):
        wave = int(5 * math.sin((x - left) / 42))
        bottom_points.append((x, bottom + wave))

    pygame.draw.lines(surface, color, False, left_points, 3)
    pygame.draw.lines(surface, color, False, right_points, 3)
    pygame.draw.lines(surface, color, False, bottom_points, 3)

    top_left = [
        (x, top + int(4 * math.sin(x / 30)))
        for x in range(left + 20, 385, 4)
    ]
    top_right = [
        (x, top + int(4 * math.sin(x / 30)))
        for x in range(515, right - 20, 4)
    ]
    pygame.draw.lines(surface, color, False, top_left, 3)
    pygame.draw.lines(surface, color, False, top_right, 3)

    for x, y in [
        (left + 7, top + 12),
        (right - 7, top + 12),
        (left + 7, 350),
        (right - 7, 350),
        (left + 35, bottom - 5),
        (right - 35, bottom - 5),
    ]:
        pygame.draw.circle(surface, color, (x, y), 6, width=3)
        pygame.draw.circle(surface, color, (x, y), 2)

    draw_bow(surface, surface.get_width() // 2, top)


def draw_pixel_button(surface, rect, label, font, mouse_pos):
    outline = (145, 52, 92)
    face = (239, 139, 179)
    highlight = (255, 205, 224)
    shadow = (187, 80, 126)

    if rect.collidepoint(mouse_pos):
        face = (248, 159, 194)

    pygame.draw.rect(surface, (133, 57, 91), rect.move(6, 7))
    pygame.draw.rect(surface, outline, rect)

    inner = rect.inflate(-8, -8)
    pygame.draw.rect(surface, face, inner)
    pygame.draw.rect(
        surface,
        highlight,
        (inner.x + 4, inner.y + 4, inner.width - 8, 6),
    )
    pygame.draw.rect(
        surface,
        shadow,
        (inner.x + 4, inner.bottom - 10, inner.width - 8, 6),
    )
    pygame.draw.rect(surface, outline, inner, width=2)

    text = font.render(label, True, (255, 250, 252))
    surface.blit(text, text.get_rect(center=rect.center))


def draw_pixel_rose(surface, center_x, center_y):
    cell = 6
    pattern = [
        "0011100",
        "0122210",
        "1223221",
        "1233321",
        "0122210",
        "0011100",
    ]
    colors = {
        "1": (174, 53, 98),
        "2": (235, 111, 157),
        "3": (250, 157, 190),
    }

    start_x = center_x - (len(pattern[0]) * cell) // 2
    start_y = center_y - 36

    for row, line in enumerate(pattern):
        for col, pixel in enumerate(line):
            if pixel != "0":
                pygame.draw.rect(
                    surface,
                    colors[pixel],
                    (start_x + col * cell, start_y + row * cell, cell, cell),
                )

    pygame.draw.rect(surface, (76, 133, 91), (center_x - 3, center_y, 7, 29))
    pygame.draw.rect(surface, (133, 181, 123), (center_x - 1, center_y + 2, 3, 24))

    pygame.draw.rect(surface, (76, 133, 91), (center_x - 20, center_y + 8, 18, 7))
    pygame.draw.rect(surface, (132, 181, 123), (center_x - 17, center_y + 10, 13, 3))
    pygame.draw.rect(surface, (76, 133, 91), (center_x + 2, center_y + 15, 18, 7))
    pygame.draw.rect(surface, (132, 181, 123), (center_x + 5, center_y + 17, 13, 3))


def draw_gingham(surface):
    background = (255, 250, 252)
    gingham = (255, 230, 239)
    width, height = surface.get_size()

    surface.fill(background)
    tile_size = 12

    for row in range((height // tile_size) + 1):
        for col in range((width // tile_size) + 1):
            if (row + col) % 2 == 0:
                pygame.draw.rect(
                    surface,
                    gingham,
                    (col * tile_size, row * tile_size, tile_size, tile_size),
                )


def show_menu(screen):
    """Return 'two_player' or a computer difficulty selection."""
    width, height = screen.get_size()
    clock = pygame.time.Clock()

    rose = (158, 83, 112)
    title_font = pygame.font.SysFont("segoescript", 58)
    prompt_font = pygame.font.SysFont("segoescript", 25)
    button_font = pygame.font.SysFont("consolas", 24, bold=True)
    small_font = pygame.font.SysFont("consolas", 15, bold=True)

    two_player_button = pygame.Rect(width // 2 - 150, 345, 300, 70)
    computer_button = pygame.Rect(width // 2 - 150, 455, 300, 70)

    easy_button = pygame.Rect(width // 2 - 150, 325, 300, 62)
    medium_button = pygame.Rect(width // 2 - 150, 415, 300, 62)
    hard_button = pygame.Rect(width // 2 - 150, 505, 300, 62)
    back_button = pygame.Rect(width // 2 - 100, 595, 200, 48)

    page = "mode"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if page == "difficulty":
                    page = "mode"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if page == "mode":
                    if two_player_button.collidepoint(event.pos):
                        return "two_player"
                    if computer_button.collidepoint(event.pos):
                        page = "difficulty"

                elif page == "difficulty":
                    if easy_button.collidepoint(event.pos):
                        return "vs_computer_easy"
                    if medium_button.collidepoint(event.pos):
                        return "vs_computer_medium"
                    if hard_button.collidepoint(event.pos):
                        return "vs_computer_hard"
                    if back_button.collidepoint(event.pos):
                        page = "mode"

        draw_gingham(screen)
        draw_menu_frame(screen)

        title = title_font.render("The Chezz", True, rose)
        screen.blit(title, title.get_rect(center=(width // 2, 205)))

        mouse_pos = pygame.mouse.get_pos()

        if page == "mode":
            prompt = prompt_font.render("choose how to play", True, rose)
            screen.blit(prompt, prompt.get_rect(center=(width // 2, 285)))

            draw_pixel_button(
                screen,
                two_player_button,
                "TWO PLAYER",
                button_font,
                mouse_pos,
            )
            draw_pixel_button(
                screen,
                computer_button,
                "VS COMPUTER",
                button_font,
                mouse_pos,
            )

            draw_pixel_rose(screen, width // 2, 575)

        else:
            prompt = prompt_font.render("choose a difficulty", True, rose)
            screen.blit(prompt, prompt.get_rect(center=(width // 2, 270)))

            draw_pixel_button(screen, easy_button, "EASY", button_font, mouse_pos)
            draw_pixel_button(screen, medium_button, "MEDIUM", button_font, mouse_pos)
            draw_pixel_button(screen, hard_button, "HARD", button_font, mouse_pos)
            draw_pixel_button(screen, back_button, "BACK", small_font, mouse_pos)

        pygame.display.flip()
        clock.tick(60)