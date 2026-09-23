// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const SCORES_KEY = 'sudokuScores';
const THEME_KEY = 'sudokuTheme';
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let hintsUsed = 0;
let gameCompleted = false;

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('theme-dark', isDark);
  const themeToggle = document.getElementById('theme-toggle');
  themeToggle.ariaPressed = String(isDark);
  themeToggle.setAttribute('aria-pressed', String(isDark));
  themeToggle.textContent = isDark ? 'Dark mode' : 'Light mode';
}

function toggleTheme() {
  const nextTheme = document.body.classList.contains('theme-dark') ? 'light' : 'dark';
  localStorage.setItem('sudokuTheme', nextTheme);
  applyTheme(nextTheme);
}

function loadTheme() {
  const savedTheme = localStorage.getItem('sudokuTheme');
  applyTheme(savedTheme === 'dark' ? 'dark' : 'light');
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainingSeconds = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainingSeconds}`;
}

function updateTimer() {
  document.getElementById('timer').textContent = formatTime(elapsedSeconds);
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimer();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimer();
  }, 1000);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function updateHintsUsed() {
  document.getElementById('hints-used').textContent = `Hints used: ${hintsUsed}`;
}

function readScores() {
  try {
    const scores = JSON.parse(localStorage.getItem('sudokuScores') || '[]');
    return Array.isArray(scores) ? scores : [];
  } catch (error) {
    return [];
  }
}

function renderScores(scores = readScores()) {
  const scoresList = document.getElementById('scores-list');
  scoresList.innerHTML = '';
  scores.forEach((score) => {
    const li = document.createElement('li');
    li.textContent = `${score.name} - ${formatTime(score.timeSeconds)} - ${score.difficulty} - ${score.hintsUsed} hints`;
    scoresList.appendChild(li);
  });
}

function saveScore() {
  const playerName = document.getElementById('player-name').value.trim();
  const message = document.getElementById('message');
  if (!playerName) {
    message.style.color = 'var(--message-error)';
    message.textContent = 'Enter your name to save your score.';
    return;
  }
  const difficulty = document.getElementById('difficulty').value;
  const scores = readScores();
  scores.push({name: playerName, timeSeconds: elapsedSeconds, difficulty, hintsUsed});
  scores.sort((first, second) => first.timeSeconds - second.timeSeconds);
  const fastestScores = scores.slice(0, 10);
  localStorage.setItem('sudokuScores', JSON.stringify(fastestScores));
  renderScores(fastestScores);
  document.getElementById('completion-panel').hidden = true;
  message.style.color = 'var(--message-success)';
  message.textContent = 'Score saved!';
}

function getBoardFromInputs() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const value = inputs[i * SIZE + j].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return {board, inputs};
}

function highlightConflicts() {
  const {board, inputs} = getBoardFromInputs();
  const conflicts = new Set();
  const groups = [];
  for (let row = 0; row < SIZE; row++) {
    groups.push(Array.from({length: SIZE}, (_, col) => row * SIZE + col));
  }
  for (let col = 0; col < SIZE; col++) {
    groups.push(Array.from({length: SIZE}, (_, row) => row * SIZE + col));
  }
  for (let boxRow = 0; boxRow < SIZE; boxRow += 3) {
    for (let boxCol = 0; boxCol < SIZE; boxCol += 3) {
      groups.push(Array.from({length: 9}, (_, index) => {
        const row = boxRow + Math.floor(index / 3);
        const col = boxCol + index % 3;
        return row * SIZE + col;
      }));
    }
  }
  for (const group of groups) {
    const seen = new Map();
    for (const index of group) {
      const value = board[Math.floor(index / SIZE)][index % SIZE];
      if (!value) continue;
      if (seen.has(value)) {
        conflicts.add(index);
        conflicts.add(seen.get(value));
      } else {
        seen.set(value, index);
      }
    }
  }
  for (let index = 0; index < inputs.length; index++) {
    inputs[index].classList.toggle('conflict', conflicts.has(index));
  }
}

function handleInput(event) {
  event.target.value = event.target.value.replace(/[^1-9]/g, '');
  highlightConflicts();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', handleInput);
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  hintsUsed = 0;
  updateHintsUsed();
  gameCompleted = false;
  document.getElementById('completion-panel').hidden = true;
  const difficultyLabel = difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
  document.getElementById('difficulty-status').innerText = `Selected difficulty: ${difficultyLabel}`;
  document.getElementById('message').innerText = '';
  startTimer();
}

async function checkSolution() {
  const {board, inputs} = getBoardFromInputs();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (data.complete) {
    if (gameCompleted) return;
    gameCompleted = true;
    stopTimer();
    msg.style.color = 'var(--message-success)';
    msg.innerText = 'Congratulations! You solved it!';
    document.getElementById('completion-panel').hidden = false;
  } else if (incorrect.size > 0) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = 'Some cells are incorrect.';
  } else {
    msg.style.color = 'var(--message-error)';
    msg.innerText = 'The puzzle is incomplete. Fill every empty cell to finish.';
  }
}

async function hint() {
  const {board, inputs} = getBoardFromInputs();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }
  const hintInput = inputs[data.row * SIZE + data.col];
  hintInput.value = data.value;
  hintInput.disabled = true;
  hintInput.className += ' hinted';
  puzzle[data.row][data.col] = data.value;
  hintsUsed += 1;
  updateHintsUsed();
  highlightConflicts();
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', hint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('save-score').addEventListener('click', saveScore);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  loadTheme();
  renderScores();
  // initialize
  newGame();
});