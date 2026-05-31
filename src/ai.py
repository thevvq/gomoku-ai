import random


def get_random_move(board):
    """
    Find all empty cells on the board and return one chosen randomly.
    Returns:
        (row, col) tuple of the selected move, or None if the board is full.
    """
    empty_cells = []
    for r in range(board.size):
        for c in range(board.size):
            if not board.is_occupied(r, c):
                empty_cells.append((r, c))

    if not empty_cells:
        return None

    return random.choice(empty_cells)
