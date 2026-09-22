import copy
import random

SIZE = 9
EMPTY = 0
DIFFICULTY_CLUES = {
    'easy': 40,
    'medium': 35,
    'hard': 30,
}

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board, limit=2):
    working_board = deep_copy(board)

    def count_remaining():
        best_cell = None
        best_candidates = None

        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] == EMPTY:
                    candidates = [
                        number
                        for number in range(1, SIZE + 1)
                        if is_safe(working_board, row, col, number)
                    ]
                    if not candidates:
                        return 0
                    if best_candidates is None or len(candidates) < len(best_candidates):
                        best_cell = (row, col)
                        best_candidates = candidates

        if best_cell is None:
            return 1

        row, col = best_cell
        solutions = 0
        for candidate in best_candidates:
            working_board[row][col] = candidate
            solutions += count_remaining()
            working_board[row][col] = EMPTY
            if solutions >= limit:
                return limit
        return solutions

    return count_remaining()

def remove_cells(board, clues):
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)
    target_empty = SIZE * SIZE - clues

    for row, col in positions:
        if target_empty == 0:
            return True
        original = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board) == 1:
            target_empty -= 1
        else:
            board[row][col] = original

    return target_empty == 0

def generate_puzzle(clues=None, difficulty='medium'):
    if clues is None:
        try:
            clues = DIFFICULTY_CLUES[difficulty.lower()]
        except (AttributeError, KeyError):
            raise ValueError(f'Invalid difficulty: {difficulty}')

    if not 0 <= clues <= SIZE * SIZE:
        raise ValueError(f'Clues must be between 0 and {SIZE * SIZE}')

    for _ in range(100):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        if remove_cells(board, clues):
            return deep_copy(board), solution

    raise RuntimeError('Unable to generate a unique puzzle with the requested clues')
