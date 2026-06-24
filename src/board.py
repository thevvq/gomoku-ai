from config import BOARD_SIZE

class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        # grid[r][c] = None | 'X' | 'O'
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]

    def reset(self):
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]

    def is_occupied(self, row, col):
        return self.grid[row][col] is not None

    def place_piece(self, row, col, piece):
        # piece should be 'X' or 'O'
        if self.grid[row][col] is not None:
            return False
        self.grid[row][col] = piece
        return True