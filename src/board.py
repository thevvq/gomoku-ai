import pygame
from config import BOARD_SIZE, CELL_SIZE, MARGIN
from config import LINE_COLOR, BACKGROUND_COLOR


class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.cell_size = CELL_SIZE
        self.margin = MARGIN
        # grid[r][c] = None | 'X' | 'O'
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]

    def reset(self):
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.draw_grid(screen)
        self.draw_pieces(screen)

    def draw_grid(self, screen):
        for i in range(self.size):
            # horizontal line
            start_x = self.margin
            start_y = self.margin + i * self.cell_size
            end_x = self.margin + (self.size - 1) * self.cell_size
            end_y = start_y
            pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 2)

            # vertical line
            start_x = self.margin + i * self.cell_size
            start_y = self.margin
            end_x = start_x
            end_y = self.margin + (self.size - 1) * self.cell_size
            pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), 2)

    def draw_pieces(self, screen):
        for r in range(self.size):
            for c in range(self.size):
                piece = self.grid[r][c]
                if piece is None:
                    continue
                x = self.margin + c * self.cell_size
                y = self.margin + r * self.cell_size
                if piece == 'O':
                    pygame.draw.circle(screen, (20, 20, 20), (x, y), int(self.cell_size * 0.4), 3)
                else:  # 'X'
                    offset = int(self.cell_size * 0.35)
                    pygame.draw.line(screen, (20, 20, 20), (x - offset, y - offset), (x + offset, y + offset), 3)
                    pygame.draw.line(screen, (20, 20, 20), (x - offset, y + offset), (x + offset, y - offset), 3)

    def pos_to_cell(self, px, py):
        # Convert pixel position to board cell (row, col). Returns None if outside.
        dx = px - self.margin
        dy = py - self.margin
        max_span = (self.size - 1) * self.cell_size
        if dx < -self.cell_size/2 or dy < -self.cell_size/2 or dx > max_span + self.cell_size/2 or dy > max_span + self.cell_size/2:
            return None
        col = int(round(dx / self.cell_size))
        row = int(round(dy / self.cell_size))
        if 0 <= row < self.size and 0 <= col < self.size:
            return (row, col)
        return None

    def is_occupied(self, row, col):
        return self.grid[row][col] is not None

    def place_piece(self, row, col, piece):
        # piece should be 'X' or 'O'
        if self.grid[row][col] is not None:
            return False
        self.grid[row][col] = piece
        return True