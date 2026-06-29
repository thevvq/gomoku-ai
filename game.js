/**
 * GOMOKU AI — game.js
 * Light Green Theme - HTML DOM Grid Rendering
 */

const BOARD_SIZE = 15;
const WIN_COUNT = 5;
const DEFAULT_PVP_PLAYER_X_NAME = 'Người chơi 1';
const AI_PLAYER_NAME = 'Gomoku AI';
const DEFAULT_PVP_PLAYER_O_NAME = 'Người chơi 2';

let state = {
  grid: [],
  currentPlayer: 'X',
  gameOver: false,
  winner: null,
  winningCells: [],
  scores: { X: 0, O: 0, draw: 0, score: 0 },
  moveHistory: [],
  mode: 'human-ai',
  difficulty: 'medium',
  playerXName: DEFAULT_PVP_PLAYER_X_NAME,
  playerOName: AI_PLAYER_NAME,
  playerONamePvP: DEFAULT_PVP_PLAYER_O_NAME,
  aiThinking: false,
  aiThinkTimeout: null,
  gameStartTime: null,
  timerInterval: null,
  lastMove: null,
};

const $ = id => document.getElementById(id);

const els = {
  statusDot:       document.querySelector('.status-dot'),
  statusText:      $('statusText'),

  playerXCard:     $('playerXCard'),
  playerOCard:     $('playerOCard'),
  playerXName:     $('playerXName'),
  playerOName:     $('playerOName'),
  
  winOverlay:      $('winOverlay'),
  winTitle:        $('winTitle'),
  winSub:          $('winSub'),

  scoreXValue:     $('scoreXValue'),
  scoreOValue:     $('scoreOValue'),
  drawValue:       $('drawValue'),
  totalGames:      $('totalGames'),

  statMoves:       $('statMoves'),
  statTime:        $('statTime'),
  statMode:        $('statMode'),

  boardGrid:       $('boardGrid'),
  
  btnNewGame:      $('btnNewGame'),
  btnReplay:       $('btnReplay'),
  btnSettingsAlt:  $('btnSettingsAlt'),
  btnWinNewGame:   $('btnWinNewGame'),
  
  settingsModal:   $('settingsModal'),
  closeSettings:   $('closeSettings'),
  saveSettings:    $('saveSettings'),
  inputPlayerX:    $('inputPlayerX'),
  inputPlayerO:    $('inputPlayerO'),
  modeHumanAI:     $('modeHumanAI'),
  modeHumanHuman:  $('modeHumanHuman'),
  difficultyGroup: $('difficultyGroup'),
  
  diffEasy:        $('diffEasy'),
  diffMedium:      $('diffMedium'),
  diffHard:        $('diffHard'),

  legendXText:     $('legendXText'),
  legendOText:     $('legendOText'),
};

// ======================== INITIALIZATION ========================
function initGame() {
  state.grid = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));
  state.currentPlayer = 'X';
  state.gameOver = false;
  state.winner = null;
  state.winningCells = [];
  state.moveHistory = [];
  state.aiThinking = false;
  state.lastMove = null;
  state.gameStartTime = Date.now();

  fetch('/api/stats')
    .then(r => r.json())
    .then(data => {
      state.scores.X = data.wins;
      state.scores.O = data.losses;
      state.scores.draw = data.draws;
      state.scores.score = data.score;
      updateScoreDisplay();
    })
    .catch(console.error);

  if (state.aiThinkTimeout) clearTimeout(state.aiThinkTimeout);
  stopTimer(); startTimer();
  els.winOverlay.classList.add('hidden');

  createGridDOM();
  updateUI();
}

function startTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);
  state.timerInterval = setInterval(() => {
    if (!state.gameStartTime) return;
    const elapsed = Math.floor((Date.now() - state.gameStartTime) / 1000);
    const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const s = String(elapsed % 60).padStart(2, '0');
    els.statTime.textContent = `${m}:${s}`;
  }, 1000);
}
function stopTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);
}

// ======================== DOM RENDER ========================
function createGridDOM() {
  els.boardGrid.innerHTML = '';
  
  const stars = [[3,3],[3,11],[7,7],[11,3],[11,11]];
  for(let s of stars) {
     const sp = document.createElement('div');
     sp.className = 'star-point';
     sp.style.left = (s[1] * 36 + 18) + 'px';
     sp.style.top = (s[0] * 36 + 18) + 'px';
     els.boardGrid.appendChild(sp);
  }
  
  for (let r = 0; r < BOARD_SIZE; r++) {
    for (let c = 0; c < BOARD_SIZE; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.id = `cell-${r}-${c}`;
      
      const hover = document.createElement('div');
      hover.className = 'hover-marker';
      cell.appendChild(hover);
      
      cell.addEventListener('click', () => placeMove(r, c));
      els.boardGrid.appendChild(cell);
    }
  }
}

function updateBoardDOM() {
  document.querySelectorAll('.piece').forEach(p => p.remove());
  document.querySelectorAll('.win-line').forEach(w => w.remove());

  for (let r = 0; r < BOARD_SIZE; r++) {
    for (let c = 0; c < BOARD_SIZE; c++) {
      const pieceStr = state.grid[r][c];
      if (pieceStr) {
        const cell = $(`cell-${r}-${c}`);
        const p = document.createElement('div');
        p.className = 'piece piece-' + pieceStr.toLowerCase();
        if (state.lastMove && state.lastMove[0] === r && state.lastMove[1] === c) {
           p.classList.add('last-move-highlight');
        }
        cell.appendChild(p);
      }
    }
  }
  if (state.winningCells && state.winningCells.length > 0) {
      drawWinLineDOM();
  }
}

function drawWinLineDOM() {
  const first = state.winningCells[0];
  const last = state.winningCells[state.winningCells.length - 1];
  const x1 = first[1] * 36 + 18;
  const y1 = first[0] * 36 + 18;
  const x2 = last[1] * 36 + 18;
  const y2 = last[0] * 36 + 18;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.sqrt(dx*dx + dy*dy);
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;

  const wl = document.createElement('div');
  wl.className = 'win-line';
  wl.style.width = len + 'px';
  wl.style.left = x1 + 'px';
  wl.style.top = y1 + 'px';
  wl.style.transform = `translateY(-50%) rotate(${angle}deg)`;
  els.boardGrid.appendChild(wl);
}

// ======================== LOGIC ========================
function checkWin(grid, r, c, player) {
  const DIRECTIONS = [[0,1],[1,0],[1,1],[1,-1]];
  for (const [dr, dc] of DIRECTIONS) {
    const cells = [];
    for (let i = -4; i <= 4; i++) {
      const nr = r + dr * i, nc = c + dc * i;
      if (nr >= 0 && nr < BOARD_SIZE && nc >= 0 && nc < BOARD_SIZE && grid[nr][nc] === player) {
        cells.push([nr, nc]);
        if (cells.length >= WIN_COUNT) return cells.slice(0, WIN_COUNT);
      } else {
        cells.length = 0;
      }
    }
  }
  return null;
}

function checkDraw(grid) {
  return grid.every(row => row.every(cell => cell !== null));
}

function placeMove(r, c) {
  if (state.gameOver || state.aiThinking || state.grid[r][c] !== null) return;

  state.grid[r][c] = state.currentPlayer;
  state.lastMove = [r, c];
  const moveNum = state.moveHistory.length + 1;
  state.moveHistory.push({ player: state.currentPlayer, row: r, col: c, num: moveNum });
  els.statMoves.textContent = state.moveHistory.length;

  const winLine = checkWin(state.grid, r, c, state.currentPlayer);
  if (winLine) {
    endGame(state.currentPlayer, winLine);
    return;
  }
  if (checkDraw(state.grid)) {
    endGame('draw', []);
    return;
  }

  state.currentPlayer = state.currentPlayer === 'X' ? 'O' : 'X';
  updateUI();
  updateBoardDOM();

  if (state.mode === 'human-ai' && state.currentPlayer === 'O' && !state.gameOver) {
    triggerAI();
  }
}

// ======================== AI ========================
function triggerAI() {
  state.aiThinking = true;
  setStatus('thinking', 'AI đang suy nghĩ...');

  const reqBody = {
    grid: state.grid,
    ai_player: 'O',
    human_player: 'X',
    difficulty: state.difficulty
  };

  fetch('/api/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqBody)
  })
  .then(res => res.json())
  .then(data => {
    setTimeout(() => {
      state.aiThinking = false;
      if (data.move) {
        placeMove(data.move[0], data.move[1]);
      }
    }, 500);
  })
  .catch(err => {
    console.error('Lỗi API AI:', err);
    state.aiThinking = false;
    setStatus('ready', 'Lỗi AI!');
  });
}

// ======================== END GAME ========================
function endGame(winner, winLine) {
  state.gameOver = true;
  state.winner = winner;
  state.winningCells = winLine;
  stopTimer();

  let apiResult = 'draw';
  if (winner === 'X') apiResult = 'win';
  else if (winner === 'O') apiResult = 'loss';
  
  fetch('/api/match_end', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ result: apiResult })
  })
  .then(r => r.json())
  .then(data => {
    state.scores.X = data.wins;
    state.scores.O = data.losses;
    state.scores.draw = data.draws;
    state.scores.score = data.score;
    updateScoreDisplay();
  })
  .catch(console.error);

  updateBoardDOM();
  updateUI();
  
  if (winner === 'draw') {
    els.winTitle.textContent = 'HÒA';
    els.winTitle.style.color = 'var(--text-main)';
    els.winSub.textContent = 'Bất phân thắng bại';
  } else {
    els.winTitle.textContent = 'WIN';
    els.winTitle.style.color = '#8B0000';
    const name = winner === 'X' ? state.playerXName : state.playerOName;
    els.winSub.textContent = `${name} đã chiến thắng!`;
    if (typeof confetti === 'function') {
      fireConfetti();
    }
  }
  els.winOverlay.classList.remove('hidden');
}

function fireConfetti() {
  var duration = 3 * 1000;
  var animationEnd = Date.now() + duration;
  var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 10000 };

  function randomInRange(min, max) {
    return Math.random() * (max - min) + min;
  }

  var interval = setInterval(function() {
    var timeLeft = animationEnd - Date.now();
    if (timeLeft <= 0) {
      return clearInterval(interval);
    }
    var particleCount = 50 * (timeLeft / duration);
    confetti(Object.assign({}, defaults, { particleCount,
      origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 }
    }));
    confetti(Object.assign({}, defaults, { particleCount,
      origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 }
    }));
  }, 250);
}

// ======================== UI UPDATE ========================
function updateUI() {
  els.playerXCard.classList.toggle('active', state.currentPlayer === 'X' && !state.gameOver);
  els.playerOCard.classList.toggle('active', state.currentPlayer === 'O' && !state.gameOver);
  
  if (!state.gameOver) {
    const name = state.currentPlayer === 'X' ? state.playerXName : state.playerOName;
    const isAI = state.mode === 'human-ai' && state.currentPlayer === 'O';
    setStatus(isAI ? 'thinking' : 'ready', isAI ? 'AI đang suy nghĩ...' : `Lượt của ${name}`);
  } else {
    setStatus('ready', 'Kết thúc');
  }

  els.playerXName.textContent = state.playerXName;
  els.playerOName.textContent = state.playerOName;
  els.legendXText.textContent = state.playerXName;
  els.legendOText.textContent = state.mode === 'human-ai' ? 'AI' : state.playerOName;
  
  const difficultyLabel = { easy: 'Dễ', medium: 'Vừa', hard: 'Khó' }[state.difficulty] || 'Vừa';
  els.statMode.textContent = state.mode === 'human-ai' ? `Người vs AI • ${difficultyLabel}` : 'Người vs Người • Local PvP';
}

function setStatus(type, text) {
  if (type === 'thinking') {
    els.statusDot.classList.add('thinking');
  } else {
    els.statusDot.classList.remove('thinking');
  }
  els.statusText.textContent = text;
}

function updateScoreDisplay() {
  els.scoreXValue.textContent = state.scores.X;
  els.scoreOValue.textContent = state.scores.O;
  els.drawValue.textContent = state.scores.draw;
  els.totalGames.textContent = state.scores.score;
}

// ======================== EVENTS ========================
els.btnNewGame.addEventListener('click', initGame);
els.btnReplay.addEventListener('click', initGame);
els.btnWinNewGame.addEventListener('click', initGame);

els.btnSettingsAlt.addEventListener('click', () => els.settingsModal.classList.remove('hidden'));
els.closeSettings.addEventListener('click', () => els.settingsModal.classList.add('hidden'));

els.saveSettings.addEventListener('click', () => {
  state.playerXName = els.inputPlayerX.value || DEFAULT_PVP_PLAYER_X_NAME;
  if (state.mode === 'human-human') {
    state.playerONamePvP = els.inputPlayerO.value || DEFAULT_PVP_PLAYER_O_NAME;
    state.playerOName = state.playerONamePvP;
  } else {
    state.playerOName = AI_PLAYER_NAME;
  }
  els.settingsModal.classList.add('hidden');
  updateUI();
});

function syncModeControls() {
  const isPvP = state.mode === 'human-human';
  els.difficultyGroup.classList.toggle('is-disabled', isPvP);
  [els.diffEasy, els.diffMedium, els.diffHard].forEach(btn => {
    btn.disabled = isPvP;
  });

  els.inputPlayerO.disabled = !isPvP;
  if (isPvP) {
    if (!state.playerONamePvP || state.playerONamePvP === AI_PLAYER_NAME) {
      state.playerONamePvP = DEFAULT_PVP_PLAYER_O_NAME;
    }
    els.inputPlayerO.value = state.playerONamePvP;
    state.playerOName = state.playerONamePvP;
  } else {
    els.inputPlayerO.value = AI_PLAYER_NAME;
    state.playerOName = AI_PLAYER_NAME;
  }
}

function updateMode(mode) {
  state.mode = mode;
  els.modeHumanAI.classList.toggle('active', mode === 'human-ai');
  els.modeHumanHuman.classList.toggle('active', mode === 'human-human');
  syncModeControls();
  updateUI();
}
els.modeHumanAI.addEventListener('click', () => updateMode('human-ai'));
els.modeHumanHuman.addEventListener('click', () => updateMode('human-human'));

function updateDiff(diff) {
  if (state.mode === 'human-human') return;
  state.difficulty = diff;
  els.diffEasy.classList.toggle('active', diff === 'easy');
  els.diffMedium.classList.toggle('active', diff === 'medium');
  els.diffHard.classList.toggle('active', diff === 'hard');
  updateUI();
}
els.diffEasy.addEventListener('click', () => updateDiff('easy'));
els.diffMedium.addEventListener('click', () => updateDiff('medium'));
els.diffHard.addEventListener('click', () => updateDiff('hard'));

// Khởi chạy khi load
window.addEventListener('DOMContentLoaded', () => {
  syncModeControls();
  initGame();
});
