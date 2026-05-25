import pygame
from config import WIDTH, HEIGHT, GAME_TITLE, TEXT_COLOR
from board import Board


def draw_status(screen, font, current_player):
    text = f"Turn: {current_player}"
    surf = font.render(text, True, TEXT_COLOR)
    screen.blit(surf, (10, HEIGHT - 60))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    board = Board()
    font = pygame.font.SysFont(None, 28)
    title_font = pygame.font.SysFont("Arial", 36)

    current_player = 'X'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                cell = board.pos_to_cell(*pos)
                if cell:
                    row, col = cell
                    if not board.is_occupied(row, col):
                        board.place_piece(row, col, current_player)
                        # switch player
                        current_player = 'O' if current_player == 'X' else 'X'

        board.draw(screen)
        # Draw title centered at the top
        title_surf = title_font.render(GAME_TITLE, True, TEXT_COLOR)
        title_x = WIDTH // 2 - title_surf.get_width() // 2
        screen.blit(title_surf, (title_x, 15))

        draw_status(screen, font, current_player)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
