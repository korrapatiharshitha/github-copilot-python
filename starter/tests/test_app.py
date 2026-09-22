from pathlib import Path

import app


STARTER_DIR = Path(__file__).parents[1]


SOLUTION = [
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
PUZZLE = [row[:] for row in SOLUTION]
PUZZLE[0][0] = 0


def setup_function():
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None


def test_index_renders_successfully():
    response = app.app.test_client().get('/')

    assert response.status_code == 200
    assert b"Sudoku" in response.data


def test_index_contains_difficulty_selector_with_all_options():
    response = app.app.test_client().get('/')

    assert b'<select id="difficulty"' in response.data
    assert b'<option value="easy">Easy</option>' in response.data
    assert b'<option value="medium" selected>Medium</option>' in response.data
    assert b'<option value="hard">Hard</option>' in response.data


def test_new_game_javascript_uses_selected_difficulty_and_updates_status():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert "document.getElementById('difficulty').value" in javascript
    assert "`/new?difficulty=${encodeURIComponent(difficulty)}`" in javascript
    assert "selected difficulty" in javascript.lower()


def test_new_game_javascript_locks_prefilled_cells():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert 'inp.disabled = true;' in javascript
    assert "inp.className += ' prefilled';" in javascript


def test_new_game_returns_puzzle_and_stores_solution(monkeypatch):
    calls = []

    def fake_generate_puzzle(*, difficulty):
        calls.append(difficulty)
        return PUZZLE, SOLUTION

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = app.app.test_client().get('/new?difficulty=hard')

    assert response.status_code == 200
    assert response.get_json() == {'puzzle': PUZZLE}
    assert calls == ['hard']
    assert app.CURRENT == {'puzzle': PUZZLE, 'solution': SOLUTION}


def test_check_solution_rejects_request_without_game():
    response = app.app.test_client().post('/check', json={'board': SOLUTION})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_returns_incorrect_cells():
    app.CURRENT['solution'] = SOLUTION
    board = [row[:] for row in SOLUTION]
    board[0][0] = 0
    board[4][4] = 1

    response = app.app.test_client().post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[0, 0], [4, 4]]}


def test_check_solution_returns_no_incorrect_cells_for_matching_board():
    app.CURRENT['solution'] = SOLUTION

    response = app.app.test_client().post('/check', json={'board': SOLUTION})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_hint_rejects_request_without_game():
    response = app.app.test_client().post('/hint', json={'board': PUZZLE})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_hint_returns_a_correct_empty_cell():
    app.CURRENT['puzzle'] = PUZZLE
    app.CURRENT['solution'] = SOLUTION

    response = app.app.test_client().post('/hint', json={'board': PUZZLE})

    assert response.status_code == 200
    assert response.get_json() == {'row': 0, 'col': 0, 'value': 5}


def test_hint_rejects_a_completed_board():
    app.CURRENT['puzzle'] = SOLUTION
    app.CURRENT['solution'] = SOLUTION

    response = app.app.test_client().post('/hint', json={'board': SOLUTION})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No empty cells available'}


def test_hint_javascript_wires_button_and_locks_returned_cell():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert "document.getElementById('hint').addEventListener('click', hint)" in javascript
    assert "fetch('/hint'" in javascript
    assert 'hintInput.value = data.value;' in javascript
    assert 'hintInput.disabled = true;' in javascript
    assert "hintInput.className += ' hinted';" in javascript


def test_javascript_contracts_cover_conflicts_checking_and_completion():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert 'highlightConflicts' in javascript
    assert "input.addEventListener('input', handleInput)" in javascript
    assert "'conflict'" in javascript
    assert 'incorrect' in javascript
    assert 'Congratulations! You solved it!' in javascript


def test_index_contains_timer_hint_counter_completion_form_and_scores_list():
    response = app.app.test_client().get('/')

    assert b'id="timer">00:00</strong>' in response.data
    assert b'id="hints-used">Hints used: 0</span>' in response.data
    assert b'id="completion-panel"' in response.data
    assert b'id="player-name"' in response.data
    assert b'id="save-score"' in response.data
    assert b'id="scores-list"' in response.data


def test_javascript_contracts_cover_timer_and_hint_tracking():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert 'startTimer()' in javascript
    assert 'stopTimer()' in javascript
    assert 'setInterval' in javascript
    assert 'clearInterval' in javascript
    assert 'hintsUsed = 0' in javascript
    assert 'hintsUsed += 1' in javascript
    assert "getElementById('hints-used')" in javascript


def test_javascript_contracts_cover_score_storage_and_leaderboard():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert "localStorage.getItem('sudokuScores')" in javascript
    assert "localStorage.setItem('sudokuScores'" in javascript
    assert 'timeSeconds' in javascript
    assert 'difficulty' in javascript
    assert 'hintsUsed' in javascript
    assert '.sort(' in javascript
    assert '.slice(0, 10)' in javascript
    assert "getElementById('scores-list')" in javascript
    assert 'li.textContent' in javascript


def test_javascript_contracts_cover_accessible_name_submission():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert "getElementById('player-name')" in javascript
    assert "getElementById('completion-panel')" in javascript
    assert "getElementById('save-score').addEventListener('click', saveScore)" in javascript
    assert '.trim()' in javascript
    assert 'name: playerName' in javascript


def test_index_contains_accessible_theme_toggle():
    response = app.app.test_client().get('/')

    assert b'id="theme-toggle"' in response.data
    assert b'aria-pressed="false"' in response.data
    assert b'Light mode' in response.data


def test_javascript_contracts_cover_persistent_theme_toggle():
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert "localStorage.getItem('sudokuTheme')" in javascript
    assert "localStorage.setItem('sudokuTheme'" in javascript
    assert 'theme-dark' in javascript
    assert "getElementById('theme-toggle')" in javascript
    assert 'ariaPressed' in javascript


def test_stylesheet_uses_css_selectors_for_alternating_sudoku_boxes():
    stylesheet = (STARTER_DIR / 'static' / 'styles.css').read_text()

    assert '.sudoku-row:nth-child(-n+3) .sudoku-cell:nth-child(-n+3)' in stylesheet
    assert '.sudoku-row:nth-child(n+4):nth-child(-n+6) .sudoku-cell:nth-child(-n+3)' in stylesheet
    assert '.sudoku-row:nth-child(n+7):nth-child(-n+9) .sudoku-cell:nth-child(-n+3)' in stylesheet
    assert '.box-tone-a' not in stylesheet
    assert '.box-tone-b' not in stylesheet


def test_stylesheet_contracts_cover_themes_focus_contrast_and_responsive_layout():
    stylesheet = (STARTER_DIR / 'static' / 'styles.css').read_text()
    javascript = (STARTER_DIR / 'static' / 'main.js').read_text()

    assert ':root' in stylesheet
    assert 'body.theme-dark' in stylesheet
    assert '--focus-outline' in stylesheet
    assert '.sudoku-cell:focus-visible' in stylesheet
    assert '.sudoku-cell.conflict' in stylesheet
    assert '.sudoku-cell.hinted' in stylesheet
    assert '#scores-list' in stylesheet
    assert '@media (max-width: 430px)' in stylesheet
    assert '--message-error' in stylesheet
    assert '--message-success' in stylesheet
    assert '#message' in stylesheet
    assert 'color: var(--message-error)' in stylesheet
    assert "msg.style.color = 'var(--message-error)'" in javascript
    assert "msg.style.color = 'var(--message-success)'" in javascript
