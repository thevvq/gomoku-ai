import pygame
from board import Board
from config import WIDTH, HEIGHT, GAME_TITLE, TEXT_COLOR


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)

    font = pygame.font.SysFont("Arial", 36)
    board = Board()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board.draw(screen)

        title = font.render(GAME_TITLE, True, TEXT_COLOR)
        title_x = WIDTH // 2 - title.get_width() // 2
        screen.blit(title, (title_x, 15))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()