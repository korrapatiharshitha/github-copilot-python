# Refactor a Sudoku Game written in Python Flask

Use this simple Sudoku game as a starting point to practice your skills with GitHub Copilot. The goal is to refactor the code to use modern technologies, while also adding new features and improving the overall user experience.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Dependencies

```
- Modern web browser (Chrome, Firefox, Edge, etc.)
- Python 3
```

### Installation

1. Fork this repository to your GitHub account. (You can use the "Fork" button on the top right corner of the repository page.)

2. Clone your forked repository to your local machine.

3. Open a terminal window and navigate to the "github-copilot-python/starter" directory.

4. Create a Python virtual environment and activate it (optional but highly recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Install required Python packages.

```bash
pip install -r requirements.txt
```

6. Run the Flask app.

```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

### Run Tests

From the repository root, run:

```bash
cd starter
python -m pytest
```

## How Copilot Instructions Shape Contributions

The repository file `.github/copilot-instructions.md` gives GitHub Copilot context and
constraints for work in this project. Copilot uses those instructions alongside the
code and the current request when it suggests code, answers questions, or edits files.
They do not execute the application and they do not replace tests, code review, or
runtime validation, but they help keep generated work consistent with the project.

For this Sudoku project, the instructions tell Copilot to:

- keep Sudoku generation and validation separate from Flask routes;
- preserve existing behavior while refactoring;
- add tests before changing game logic and run them after each feature;
- handle invalid input consistently; and
- keep the interface responsive, keyboard-friendly, and readable in light and dark modes.

For example, a request to change solution checking should lead Copilot toward tests in
`starter/tests/`, reusable logic in `starter/sudoku_logic.py` where appropriate, and a
small Flask route or frontend change rather than moving all game rules into a route.
A request to adjust the interface should account for `starter/static/styles.css`,
keyboard focus, and both theme variants. These instructions are project guidance, so
developers should still verify the result with the full test suite and by using the app.

### Project Examples and Best Practices

- Run `python -m pytest` from `starter/` after changes. Keep tests focused on observable
	behavior, such as puzzle uniqueness, difficulty clue counts, API responses, and UI
	contracts.
- Keep generated puzzles and solution data separate. The Flask app stores the current
	puzzle and solution, while the Sudoku module owns board generation, safety checks, and
	solution counting.
- Preserve user-facing behavior when adding features. Difficulty selection, unique
	solutions, hints, conflict highlighting, timers, scoring, themes, and responsive
	layout are existing contracts.
- Treat empty cells, invalid entries, and incorrect entries as distinct states. Return
	clear API results and show messages that tell the player what remains to be done.
- Prefer small named functions and existing patterns over broad refactors. Check the
	rendered keyboard and focus behavior when changing the board controls.

## Comments and Documentation

Comments in the Python and JavaScript files are intentionally limited to useful
orientation, such as identifying the in-memory current-game store or grouping the
button wiring. The function names and tests document most of the behavior directly,
which keeps comments from becoming stale descriptions of implementation details.

The README documents setup, commands, project behavior, and the role of Copilot
instructions so a future developer can get started without reverse-engineering the
repository. Tests provide executable documentation for important contracts, including
unique puzzle generation, difficulty levels, hints, completion checking, themes,
timers, scores, and responsive/accessibility-related UI hooks. When behavior changes,
update the nearest test and the relevant README section together.

## Official GitHub Copilot Documentation

- [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- [About custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/concepts/prompting/response-customization)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot)

## Project Instructions

Use GitHub Copilot to refactor the code for this game to add more advanced features. The goal is to create a more modern and maintainable codebase and add additional functionality to the final product. You can use any combination of code completion and chat features, like Ask, Edit, or Agent modes.

- Errors should be handled gracefully with appropriate messages to the user.
- Implement a Sudoku board generator that creates a valid Sudoku puzzle with a unique solution.
- Add a timer to track how long it takes to solve the puzzle.
- Implement a solution checker that verifies if the user's solution is correct using event delegation.
- Add a difficulty selector to allow users to choose between easy, medium, and hard puzzles.
- Add a hint feature that provides clues for the user that are noted with unique colors.
- Add a check puzzle button that checks the current state of the board against the solution.
- User should get immediate feedback on their input, such as highlighting invalid entries.
- Top 10 scores should be saved in local storage and displayed on the page with the user's name, time taken, hints used, and difficulty level.
- The game should be responsive and work well on both desktop and mobile devices.
- UI colors should be visually appealing and accessible.
- Completed and correct puzzles should display a congratulatory message with the time taken and hints used and ask for the user's name for Top 10 times.
