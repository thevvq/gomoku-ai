import pygame
from config import WIDTH, HEIGHT, GAME_TITLE, TEXT_COLOR, BOARD_SIZE
from board import Board


class Game:
    def __init__(self, board):
        self.board = board
        self.game_over = False
        self.winner = None

    def check_win(self, row, col, player):
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dx, dy in directions:
            count = 1
            count += self.count_direction(row, col, dx, dy, player)
            count += self.count_direction(row, col, -dx, -dy, player)

            if count >= 5:
                self.game_over = True
                self.winner = player
                return True

        return False

    def count_direction(self, row, col, dx, dy, player):
        count = 0
        current_row = row + dx
        current_col = col + dy

        while (
            0 <= current_row < BOARD_SIZE
            and 0 <= current_col < BOARD_SIZE
            and self.board.grid[current_row][current_col] == player
        ):
            count += 1
            current_row += dx
            current_col += dy

        return count


def draw_status(screen, font, current_player, game):
    if game.game_over:
        text = f"Player {game.winner} wins!"
    else:
        text = f"Turn: {current_player}"

    surf = font.render(text, True, TEXT_COLOR)
    screen.blit(surf, (10, HEIGHT - 60))


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    board = Board()
    game = Game(board)

    font = pygame.font.SysFont(None, 28)
    title_font = pygame.font.SysFont("Arial", 36)

    current_player = 'X'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.game_over:
                    continue

                pos = pygame.mouse.get_pos()
                cell = board.pos_to_cell(*pos)

                if cell:
                    row, col = cell

                    if not board.is_occupied(row, col):
                        board.place_piece(row, col, current_player)

                        if game.check_win(row, col, current_player):
                            print(f"Player {current_player} wins!")
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'

        board.draw(screen)

        title_surf = title_font.render(GAME_TITLE, True, TEXT_COLOR)
        title_x = WIDTH // 2 - title_surf.get_width() // 2
        screen.blit(title_surf, (title_x, 15))

        draw_status(screen, font, current_player, game)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()