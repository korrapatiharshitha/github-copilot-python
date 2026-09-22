import sudoku_logic


VALID_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def test_create_empty_board_returns_nine_by_nine_zero_board():
    board = sudoku_logic.create_empty_board()

    assert board == [[0] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]


def test_deep_copy_does_not_share_nested_rows():
    copied = sudoku_logic.deep_copy(VALID_BOARD)
    copied[0][0] = 0

    assert VALID_BOARD[0][0] == 5


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert not sudoku_logic.is_safe(board, 0, 1, 5)
    assert not sudoku_logic.is_safe(board, 1, 0, 5)
    assert not sudoku_logic.is_safe(board, 1, 1, 5)
    assert sudoku_logic.is_safe(board, 0, 1, 3)


def test_fill_board_creates_a_valid_solution():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board)
    assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in board)
    assert all(
        sudoku_logic.is_safe(
            [row[:] for row in board[:row_index]] + [[0] * sudoku_logic.SIZE] + board[row_index + 1 :],
            row_index,
            col_index,
            board[row_index][col_index],
        )
        for row_index in range(sudoku_logic.SIZE)
        for col_index in range(sudoku_logic.SIZE)
    )


def test_generate_puzzle_returns_requested_number_of_clues_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=40)

    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 40
    assert solution != puzzle
    assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in solution)
    assert all(
        puzzle[row][col] == solution[row][col]
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
        if puzzle[row][col] != sudoku_logic.EMPTY
    )


def test_count_solutions_returns_one_for_a_completed_board():
    assert sudoku_logic.count_solutions(VALID_BOARD) == 1


def test_count_solutions_stops_at_the_requested_limit():
    assert sudoku_logic.count_solutions(sudoku_logic.create_empty_board(), limit=2) == 2


def test_each_difficulty_generates_a_unique_puzzle_with_expected_clues():
    expected_clues = {'easy': 40, 'medium': 35, 'hard': 30}

    for difficulty, clues in expected_clues.items():
        puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)

        assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == clues
        assert sudoku_logic.count_solutions(puzzle) == 1
        assert all(
            puzzle[row][col] == solution[row][col]
            for row in range(sudoku_logic.SIZE)
            for col in range(sudoku_logic.SIZE)
            if puzzle[row][col] != sudoku_logic.EMPTY
        )


def test_generate_puzzle_rejects_invalid_difficulty():
    import pytest

    with pytest.raises(ValueError, match='Invalid difficulty'):
        sudoku_logic.generate_puzzle(difficulty='impossible')
