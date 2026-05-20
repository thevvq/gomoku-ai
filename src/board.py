import pygame
from config import BOARD_SIZE, CELL_SIZE, MARGIN
from config import LINE_COLOR, BACKGROUND_COLOR


class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.cell_size = CELL_SIZE
        self.margin = MARGIN

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.draw_grid(screen)

    def draw_grid(self, screen):
        for i in range(self.size):

            # Đường ngang
            start_x = self.margin
            start_y = self.margin + i * self.cell_size

            end_x = self.margin + (self.size - 1) * self.cell_size
            end_y = start_y

            pygame.draw.line(
                screen,
                LINE_COLOR,
                (start_x, start_y),
                (end_x, end_y),
                2
            )

            # Đường dọc
            start_x = self.margin + i * self.cell_size
            start_y = self.margin

            end_x = start_x
            end_y = self.margin + (self.size - 1) * self.cell_size

            pygame.draw.line(
                screen,
                LINE_COLOR,
                (start_x, start_y),
                (end_x, end_y),
                2
            )