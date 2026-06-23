/**
 * GOMOKU AI — game.js
 * Full game logic + Canvas rendering + AI + Fireworks
 */

// ======================== CONSTANTS ========================
const BOARD_SIZE = 15;
const WIN_COUNT = 5;

// ======================== STATE ========================
let state = {
  grid: [],            // 2D array: null | 'X' | 'O'
  currentPlayer: 'X',
  gameOver: false,
  winner: null,
  winningCells: [],
  scores: { X: 0, O: 0, draw: 0 },
  totalGames: 0,
  moveHistory: [],
  mode: 'human-ai',   // 'human-ai' | 'human-human'
  difficulty: 'medium',
  playerXName: 'Người Chơi',
  playerOName: 'Gomoku AI',
  soundEnabled: true,
  effectsEnabled: true,
  aiThinking: false,
  aiThinkTimeout: null,
  gameStartTime: null,
  timerInterval: null,
  hoverCell: null,
};

// ======================== CANVAS ========================
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const CELL = 34;
const MARGIN = 22;
const BOARD_PX = MARGIN * 2 + (BOARD_SIZE - 1) * CELL;

canvas.width = BOARD_PX;
canvas.height = BOARD_PX;

// ======================== DOM ========================
const $ = id => document.getElementById(id);

const els = {
  loadingScreen:   $('loadingScreen'),
  loadingBar:      $('loadingBar'),
  app:             $('app'),
  statusDot:       $('statusDot'),
  statusText:      $('statusText'),

  playerXCard:     $('playerXCard'),
  playerOCard:     $('playerOCard'),
  playerXName:     $('playerXName'),
  playerOName:     $('playerOName'),
  playerXBadge:    $('playerXBadge'),
  playerOBadge:    $('playerOBadge'),
  turnText:        $('turnText'),

  winOverlay:      $('winOverlay'),
  winEmoji:        $('winEmoji'),
  winTitle:        $('winTitle'),
  winSub:          $('winSub'),

  historyList:     $('historyList'),
  moveCount:       $('moveCount'),

  scoreXValue:     $('scoreXValue'),
  scoreOValue:     $('scoreOValue'),
  scoreXName:      $('scoreXName'),
  scoreOName:      $('scoreOName'),
  drawValue:       $('drawValue'),
  totalGames:      $('totalGames'),

  statMoves:       $('statMoves'),
  statTime:        $('statTime'),
  statMode:        $('statMode'),

  settingsModal:   $('settingsModal'),
  inputPlayerX:    $('inputPlayerX'),
  toggleSound:     $('toggleSound'),
  toggleEffects:   $('toggleEffects'),
  modeHumanAI:     $('modeHumanAI'),
  modeHumanHuman:  $('modeHumanHuman'),

  fireworksCanvas: $('fireworksCanvas'),
  particleCanvas:  $('particleCanvas'),
};

// ======================== LOADING ========================
function runLoadingSequence() {
  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * 12 + 3;
    if (progress >= 100) {
      progress = 100;
      clearInterval(interval);
      setTimeout(revealApp, 400);
    }
    els.loadingBar.style.width = progress + '%';
  }, 60);
}

function revealApp() {
  els.loadingScreen.style.opacity = '0';
  els.loadingScreen.style.transition = 'opacity 0.6s ease';
  setTimeout(() => {
    els.loadingScreen.style.display = 'none';
    els.app.classList.remove('hidden');
    els.app.classList.add('app-enter');
    initGame();
    startParticles();
  }, 600);
}

// ======================== GAME INIT ========================
function createGrid() {
  return Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));
}

function initGame(resetScores = false) {
  state.grid = createGrid();
  state.currentPlayer = 'X';
  state.gameOver = false;
  state.winner = null;
  state.winningCells = [];
  state.moveHistory = [];
  state.aiThinking = false;
  state.hoverCell = null;
  state.gameStartTime = Date.now();

  if (resetScores) {
    state.scores = { X: 0, O: 0, draw: 0 };
    state.totalGames = 0;
  }

  if (state.aiThinkTimeout) clearTimeout(state.aiThinkTimeout);
  stopTimer(); startTimer();
  stopFireworks();
  hideWinOverlay();

  updateUI();
  drawBoard();
}

// ======================== TIMER ========================
function startTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);
  state.timerInterval = setInterval(updateTimer, 1000);
}
function stopTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);
}
function updateTimer() {
  if (!state.gameStartTime) return;
  const elapsed = Math.floor((Date.now() - state.gameStartTime) / 1000);
  const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
  const s = String(elapsed % 60).padStart(2, '0');
  els.statTime.textContent = `${m}:${s}`;
}

// ======================== CHECK WIN ========================
const DIRECTIONS = [[0,1],[1,0],[1,1],[1,-1]];

function getLine(grid, r, c, dr, dc, player) {
  const cells = [];
  for (let i = -4; i <= 4; i++) {
    const nr = r + dr * i, nc = c + dc * i;
    if (nr < 0 || nr >= BOARD_SIZE || nc < 0 || nc >= BOARD_SIZE) continue;
    if (grid[nr][nc] === player) cells.push([nr, nc]);
    else cells.length = 0;
    if (cells.length >= WIN_COUNT) return cells.slice(0, WIN_COUNT);
  }
  return null;
}

function checkWin(grid, r, c, player) {
  for (const [dr, dc] of DIRECTIONS) {
    const line = getLine(grid, r, c, dr, dc, player);
    if (line) return line;
  }
  return null;
}

function checkDraw(grid) {
  return grid.every(row => row.every(cell => cell !== null));
}

// ======================== PLACE MOVE ========================
function placeMove(r, c) {
  if (state.gameOver || state.aiThinking || state.grid[r][c] !== null) return;

  state.grid[r][c] = state.currentPlayer;
  const moveNum = state.moveHistory.length + 1;
  state.moveHistory.push({ player: state.currentPlayer, row: r, col: c, num: moveNum });
  addHistoryItem(state.currentPlayer, r, c, moveNum);
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
  drawBoard();

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
    human_player: 'X'
  };

  fetch('/api/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reqBody)
  })
  .then(res => res.json())
  .then(data => {
    state.aiThinking = false;
    if (data.move) {
      placeMove(data.move[0], data.move[1]);
    } else {
      // Bàn cờ đầy hoặc không có nước đi
    }
  })
  .catch(err => {
    console.error('Lỗi khi gọi AI Python:', err);
    state.aiThinking = false;
    setStatus('active', 'Lỗi kết nối AI!');
  });
}

// Lõi AI đã được chuyển về Python backend (xem src/server.py và src/ai.py)

// ======================== END GAME ========================
function endGame(winner, winLine) {
  state.gameOver = true;
  state.winner = winner;
  state.winningCells = winLine;
  state.totalGames++;
  stopTimer();

  if (winner !== 'draw') {
    state.scores[winner]++;
    updateScoreDisplay(winner);
  } else {
    state.scores.draw++;
    updateScoreDisplay(null);
  }

  drawBoard();
  updateUI();
  showWinOverlay(winner);

  if (winner !== 'draw' && state.effectsEnabled) {
    setTimeout(startFireworks, 300);
  }
}

// ======================== UI UPDATE ========================
function updateUI() {
  // Player cards active state
  els.playerXCard.classList.toggle('active', state.currentPlayer === 'X' && !state.gameOver);
  els.playerXCard.classList.remove('active-o');
  els.playerOCard.classList.toggle('active-o', state.currentPlayer === 'O' && !state.gameOver);
  els.playerOCard.classList.remove('active');

  // Badges
  els.playerXBadge.style.opacity = state.winner === 'X' ? '1' : '0';
  els.playerOBadge.style.opacity = state.winner === 'O' ? '1' : '0';

  // Turn text
  if (!state.gameOver) {
    const name = state.currentPlayer === 'X' ? state.playerXName : state.playerOName;
    const isAI = state.mode === 'human-ai' && state.currentPlayer === 'O';
    els.turnText.textContent = isAI ? 'AI ĐANG NGHĨ...' : `LƯỢT ${name.toUpperCase()}`;
    setStatus('active', isAI ? 'AI đang suy nghĩ...' : `Lượt của ${name}`);
  } else {
    setStatus('win', state.winner === 'draw' ? 'Hòa!' : `${state.winner === 'X' ? state.playerXName : state.playerOName} thắng!`);
  }

  // Names
  els.playerXName.textContent = state.playerXName;
  els.playerOName.textContent = state.playerOName;
  els.scoreXName.textContent = state.playerXName;
  els.scoreOName.textContent = state.playerOName;

  // Stats
  els.statMode.textContent = state.mode === 'human-ai' ? 'Người vs AI' : 'Người vs Người';
  els.drawValue.textContent = state.scores.draw;
  els.totalGames.textContent = state.totalGames;
}

function setStatus(type, text) {
  els.statusDot.className = 'status-dot';
  if (type === 'thinking') els.statusDot.classList.add('thinking');
  if (type === 'win') els.statusDot.classList.add('win');
  els.statusText.textContent = text;
}

function updateScoreDisplay(winner) {
  els.scoreXValue.textContent = state.scores.X;
  els.scoreOValue.textContent = state.scores.O;
  els.drawValue.textContent = state.scores.draw;
  els.totalGames.textContent = state.totalGames;

  if (winner === 'X') {
    els.scoreXValue.style.animation = 'none';
    requestAnimationFrame(() => { els.scoreXValue.style.animation = 'scoreFlash 0.5s ease'; });
  } else if (winner === 'O') {
    els.scoreOValue.style.animation = 'none';
    requestAnimationFrame(() => { els.scoreOValue.style.animation = 'scoreFlash 0.5s ease'; });
  }
}

function addHistoryItem(player, r, c, num) {
  const cols = 'ABCDEFGHIJKLMNO';
  const label = `${num}. ${player}${cols[c]}${r + 1}`;
  const div = document.createElement('div');
  div.className = `history-item ${player.toLowerCase()}`;
  div.textContent = label;
  els.historyList.appendChild(div);
  els.historyList.scrollTop = els.historyList.scrollHeight;
  els.moveCount.textContent = `${num} nước`;
}

function showWinOverlay(winner) {
  if (winner === 'draw') {
    els.winEmoji.textContent = '🤝';
    els.winTitle.textContent = 'HÒA!';
    els.winSub.textContent = 'Hai bên không phân thắng bại';
  } else {
    const name = winner === 'X' ? state.playerXName : state.playerOName;
    els.winEmoji.textContent = winner === 'X' ? '🏆' : '🤖';
    els.winTitle.textContent = 'CHIẾN THẮNG!';
    els.winSub.textContent = `${name} (Quân ${winner}) đã thắng!`;
  }
  setTimeout(() => els.winOverlay.classList.remove('hidden'), 600);
}

function hideWinOverlay() {
  els.winOverlay.classList.add('hidden');
}

// ======================== CANVAS DRAWING ========================
const COLORS = {
  bg:           '#0d1120',
  boardBg:      '#0b1327',
  line:         'rgba(60, 90, 150, 0.35)',
  lineDot:      'rgba(0, 207, 255, 0.5)',
  hover:        'rgba(0, 207, 255, 0.08)',
  hoverBorder:  'rgba(0, 207, 255, 0.25)',
  xColor:       '#00cfff',
  xGlow:        'rgba(0, 207, 255, 0.7)',
  oColor:       '#ff4d6d',
  oGlow:        'rgba(255, 77, 109, 0.7)',
  winHighlight: '#fbbf24',
  winGlow:      'rgba(251, 191, 36, 0.8)',
};

function cellToPixel(r, c) {
  return [MARGIN + c * CELL, MARGIN + r * CELL];
}

function pixelToCell(px, py) {
  const c = Math.round((px - MARGIN) / CELL);
  const r = Math.round((py - MARGIN) / CELL);
  if (r < 0 || r >= BOARD_SIZE || c < 0 || c >= BOARD_SIZE) return null;
  return [r, c];
}

function drawBoard() {
  ctx.clearRect(0, 0, BOARD_PX, BOARD_PX);

  // Background
  const bg = ctx.createRadialGradient(BOARD_PX/2, BOARD_PX/2, 0, BOARD_PX/2, BOARD_PX/2, BOARD_PX/1.5);
  bg.addColorStop(0, '#0f1830');
  bg.addColorStop(1, '#080b14');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, BOARD_PX, BOARD_PX);

  drawGridLines();
  drawStarPoints();
  drawHoverEffect();
  drawPieces();
  drawWinLine();
}

function drawGridLines() {
  ctx.strokeStyle = COLORS.line;
  ctx.lineWidth = 1;

  for (let i = 0; i < BOARD_SIZE; i++) {
    const [x1, y1] = cellToPixel(i, 0);
    const [x2, y2] = cellToPixel(i, BOARD_SIZE - 1);
    ctx.beginPath();
    ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
    ctx.stroke();

    const [xa, ya] = cellToPixel(0, i);
    const [xb, yb] = cellToPixel(BOARD_SIZE - 1, i);
    ctx.beginPath();
    ctx.moveTo(xa, ya); ctx.lineTo(xb, yb);
    ctx.stroke();
  }

  // Border
  const [x0, y0] = cellToPixel(0, 0);
  const [xN, yN] = cellToPixel(BOARD_SIZE - 1, BOARD_SIZE - 1);
  ctx.strokeStyle = 'rgba(0, 207, 255, 0.2)';
  ctx.lineWidth = 1.5;
  ctx.strokeRect(x0, y0, xN - x0, yN - y0);
}

function drawStarPoints() {
  const stars = [[3,3],[3,11],[7,7],[11,3],[11,11]];
  for (const [r, c] of stars) {
    const [x, y] = cellToPixel(r, c);
    ctx.beginPath();
    ctx.arc(x, y, 3.5, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(0, 207, 255, 0.4)';
    ctx.fill();
    // glow
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(0, 207, 255, 0.08)';
    ctx.fill();
  }
}

function drawHoverEffect() {
  if (!state.hoverCell || state.gameOver || state.aiThinking) return;
  const [r, c] = state.hoverCell;
  if (state.grid[r][c] !== null) return;
  const [x, y] = cellToPixel(r, c);

  // Glowing circle preview
  ctx.beginPath();
  ctx.arc(x, y, CELL * 0.38, 0, Math.PI * 2);
  const color = state.currentPlayer === 'X' ? 'rgba(0, 207, 255, 0.08)' : 'rgba(255, 77, 109, 0.08)';
  ctx.fillStyle = color;
  ctx.fill();

  ctx.beginPath();
  ctx.arc(x, y, CELL * 0.38, 0, Math.PI * 2);
  ctx.strokeStyle = state.currentPlayer === 'X' ? 'rgba(0, 207, 255, 0.3)' : 'rgba(255, 77, 109, 0.3)';
  ctx.lineWidth = 1;
  ctx.stroke();
}

function drawPieces() {
  for (let r = 0; r < BOARD_SIZE; r++) {
    for (let c = 0; c < BOARD_SIZE; c++) {
      const piece = state.grid[r][c];
      if (!piece) continue;

      const isWin = state.winningCells.some(([wr, wc]) => wr === r && wc === c);
      const [x, y] = cellToPixel(r, c);

      if (piece === 'X') {
        drawX(x, y, isWin);
      } else {
        drawO(x, y, isWin);
      }
    }
  }
}

function drawX(x, y, isWin) {
  const off = CELL * 0.32;
  const color = isWin ? COLORS.winHighlight : COLORS.xColor;
  const glowColor = isWin ? COLORS.winGlow : COLORS.xGlow;

  // Outer glow
  ctx.save();
  ctx.shadowColor = glowColor;
  ctx.shadowBlur = isWin ? 24 : 12;

  ctx.strokeStyle = color;
  ctx.lineWidth = isWin ? 3.5 : 2.8;
  ctx.lineCap = 'round';

  ctx.beginPath();
  ctx.moveTo(x - off, y - off); ctx.lineTo(x + off, y + off);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x + off, y - off); ctx.lineTo(x - off, y + off);
  ctx.stroke();

  ctx.restore();

  // Inner bright core
  ctx.save();
  ctx.shadowColor = color;
  ctx.shadowBlur = 4;
  ctx.strokeStyle = isWin ? '#fff' : 'rgba(200, 240, 255, 0.6)';
  ctx.lineWidth = 1;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(x - off + 2, y - off + 2); ctx.lineTo(x + off - 2, y + off - 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x + off - 2, y - off + 2); ctx.lineTo(x - off + 2, y + off - 2);
  ctx.stroke();
  ctx.restore();
}

function drawO(x, y, isWin) {
  const r = CELL * 0.34;
  const color = isWin ? COLORS.winHighlight : COLORS.oColor;
  const glowColor = isWin ? COLORS.winGlow : COLORS.oGlow;

  ctx.save();
  ctx.shadowColor = glowColor;
  ctx.shadowBlur = isWin ? 24 : 12;

  ctx.strokeStyle = color;
  ctx.lineWidth = isWin ? 3.5 : 2.8;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.stroke();

  ctx.restore();

  // Inner highlight
  ctx.save();
  ctx.strokeStyle = isWin ? 'rgba(255,255,200,0.6)' : 'rgba(255,160,180,0.3)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(x - r * 0.25, y - r * 0.25, r * 0.5, -Math.PI * 0.75, -Math.PI * 0.1);
  ctx.stroke();
  ctx.restore();
}

function drawWinLine() {
  if (!state.winningCells || state.winningCells.length < 2) return;
  const first = state.winningCells[0];
  const last = state.winningCells[state.winningCells.length - 1];
  const [x1, y1] = cellToPixel(first[0], first[1]);
  const [x2, y2] = cellToPixel(last[0], last[1]);

  ctx.save();
  ctx.shadowColor = COLORS.winGlow;
  ctx.shadowBlur = 20;
  ctx.strokeStyle = COLORS.winHighlight;
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';
  ctx.globalAlpha = 0.6;
  ctx.beginPath();
  ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
  ctx.stroke();
  ctx.restore();
}

// ======================== CANVAS EVENTS ========================
canvas.addEventListener('mousemove', e => {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const px = (e.clientX - rect.left) * scaleX;
  const py = (e.clientY - rect.top) * scaleY;
  const cell = pixelToCell(px, py);
  const prev = state.hoverCell;

  state.hoverCell = (cell && state.grid[cell[0]][cell[1]] === null) ? cell : null;

  if (JSON.stringify(prev) !== JSON.stringify(state.hoverCell)) drawBoard();
});

canvas.addEventListener('mouseleave', () => {
  state.hoverCell = null;
  drawBoard();
});

canvas.addEventListener('click', e => {
  if (state.gameOver || state.aiThinking) return;
  if (state.mode === 'human-ai' && state.currentPlayer === 'O') return;

  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const px = (e.clientX - rect.left) * scaleX;
  const py = (e.clientY - rect.top) * scaleY;
  const cell = pixelToCell(px, py);
  if (!cell) return;

  const [r, c] = cell;
  if (state.grid[r][c] !== null) return;

  playSound('place');
  placeMove(r, c);
});

canvas.addEventListener('touchstart', e => {
  e.preventDefault();
  const touch = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const px = (touch.clientX - rect.left) * scaleX;
  const py = (touch.clientY - rect.top) * scaleY;
  const cell = pixelToCell(px, py);
  if (!cell || state.grid[cell[0]][cell[1]] !== null || state.gameOver || state.aiThinking) return;
  if (state.mode === 'human-ai' && state.currentPlayer === 'O') return;
  placeMove(cell[0], cell[1]);
}, { passive: false });

// ======================== SOUND ========================
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function getAudioCtx() {
  if (!audioCtx) audioCtx = new AudioCtx();
  return audioCtx;
}

function playSound(type) {
  if (!state.soundEnabled) return;
  try {
    const ctx2 = getAudioCtx();
    const osc = ctx2.createOscillator();
    const gain = ctx2.createGain();
    osc.connect(gain); gain.connect(ctx2.destination);

    if (type === 'place') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, ctx2.currentTime);
      osc.frequency.exponentialRampToValueAtTime(440, ctx2.currentTime + 0.1);
      gain.gain.setValueAtTime(0.15, ctx2.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx2.currentTime + 0.2);
      osc.start(); osc.stop(ctx2.currentTime + 0.2);
    } else if (type === 'win') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(523, ctx2.currentTime);
      osc.frequency.setValueAtTime(659, ctx2.currentTime + 0.1);
      osc.frequency.setValueAtTime(784, ctx2.currentTime + 0.2);
      gain.gain.setValueAtTime(0.2, ctx2.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx2.currentTime + 0.5);
      osc.start(); osc.stop(ctx2.currentTime + 0.5);
    }
  } catch {}
}

// ======================== FIREWORKS ========================
const fwCanvas = els.fireworksCanvas;
const fwCtx = fwCanvas.getContext('2d');
let fwAnimId = null;
let particles = [];

function resizeFireworks() {
  fwCanvas.width = window.innerWidth;
  fwCanvas.height = window.innerHeight;
}

class Particle {
  constructor(x, y, color) {
    this.x = x; this.y = y;
    const angle = Math.random() * Math.PI * 2;
    const speed = 2 + Math.random() * 6;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed - 3;
    this.alpha = 1;
    this.color = color;
    this.size = 2 + Math.random() * 3;
    this.decay = 0.015 + Math.random() * 0.015;
    this.gravity = 0.12;
  }
  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.vy += this.gravity;
    this.vx *= 0.99;
    this.alpha -= this.decay;
  }
  draw(ctx) {
    ctx.save();
    ctx.globalAlpha = Math.max(0, this.alpha);
    ctx.shadowColor = this.color;
    ctx.shadowBlur = 6;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
}

const FW_COLORS = ['#00cfff','#a855f7','#fbbf24','#10b981','#ec4899','#f97316','#fff'];

function launchBurst() {
  const x = Math.random() * fwCanvas.width;
  const y = Math.random() * fwCanvas.height * 0.6;
  const color = FW_COLORS[Math.floor(Math.random() * FW_COLORS.length)];
  for (let i = 0; i < 60; i++) particles.push(new Particle(x, y, color));
}

function animateFireworks() {
  fwCtx.clearRect(0, 0, fwCanvas.width, fwCanvas.height);
  particles = particles.filter(p => p.alpha > 0);
  particles.forEach(p => { p.update(); p.draw(fwCtx); });
  fwAnimId = requestAnimationFrame(animateFireworks);
}

function startFireworks() {
  resizeFireworks();
  fwCanvas.style.display = 'block';
  particles = [];
  playSound('win');

  // Launch multiple bursts
  for (let i = 0; i < 4; i++) setTimeout(launchBurst, i * 400);
  const interval = setInterval(launchBurst, 1200);
  setTimeout(() => clearInterval(interval), 5000);

  if (fwAnimId) cancelAnimationFrame(fwAnimId);
  animateFireworks();
}

function stopFireworks() {
  if (fwAnimId) { cancelAnimationFrame(fwAnimId); fwAnimId = null; }
  particles = [];
  fwCanvas.style.display = 'none';
  fwCtx.clearRect(0, 0, fwCanvas.width, fwCanvas.height);
}

// ======================== BACKGROUND PARTICLES ========================
const bgCanvas = els.particleCanvas;
const bgCtx = bgCanvas.getContext('2d');
let bgParticles = [];
let bgAnimId = null;

class BgParticle {
  constructor() { this.reset(); }
  reset() {
    this.x = Math.random() * bgCanvas.width;
    this.y = Math.random() * bgCanvas.height;
    this.r = Math.random() * 1.5 + 0.3;
    this.vx = (Math.random() - 0.5) * 0.3;
    this.vy = (Math.random() - 0.5) * 0.3;
    this.alpha = Math.random() * 0.5 + 0.1;
    const hue = Math.random() > 0.5 ? 195 : 280;
    this.color = `hsla(${hue}, 90%, 65%, ${this.alpha})`;
  }
  update() {
    this.x += this.vx; this.y += this.vy;
    if (this.x < 0 || this.x > bgCanvas.width || this.y < 0 || this.y > bgCanvas.height) this.reset();
  }
  draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
  }
}

function resizeBgCanvas() {
  bgCanvas.width = window.innerWidth;
  bgCanvas.height = window.innerHeight;
}

function startParticles() {
  resizeBgCanvas();
  bgParticles = Array.from({ length: 80 }, () => new BgParticle());

  function tick() {
    bgCtx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);
    bgParticles.forEach(p => { p.update(); p.draw(bgCtx); });
    bgAnimId = requestAnimationFrame(tick);
  }
  tick();
}

window.addEventListener('resize', () => {
  resizeBgCanvas();
  resizeFireworks();
});

// ======================== BUTTON EVENTS ========================
function newGame() {
  stopFireworks();
  initGame(false);
}

function replayGame() {
  stopFireworks();
  initGame(true);
}

$('btnNewGame').addEventListener('click', newGame);
$('btnReplay').addEventListener('click', replayGame);
$('btnWinNewGame').addEventListener('click', newGame);
$('btnWinReplay').addEventListener('click', replayGame);

// Settings
[$('btnSettings'), $('btnSettingsAlt')].forEach(btn => {
  btn.addEventListener('click', () => {
    els.inputPlayerX.value = state.playerXName;
    els.toggleSound.checked = state.soundEnabled;
    els.toggleEffects.checked = state.effectsEnabled;
    els.modeHumanAI.classList.toggle('active', state.mode === 'human-ai');
    els.modeHumanHuman.classList.toggle('active', state.mode === 'human-human');
    els.settingsModal.classList.remove('hidden');
  });
});

$('closeSettings').addEventListener('click', () => els.settingsModal.classList.add('hidden'));
els.settingsModal.addEventListener('click', e => {
  if (e.target === els.settingsModal) els.settingsModal.classList.add('hidden');
});

$('saveSettings').addEventListener('click', () => {
  const name = els.inputPlayerX.value.trim();
  if (name) state.playerXName = name;
  state.soundEnabled = els.toggleSound.checked;
  state.effectsEnabled = els.toggleEffects.checked;
  els.settingsModal.classList.add('hidden');
  updateUI();
});

// Mode buttons
els.modeHumanAI.addEventListener('click', () => {
  state.mode = 'human-ai';
  els.modeHumanAI.classList.add('active');
  els.modeHumanHuman.classList.remove('active');
  state.playerOName = 'Gomoku AI';
  updateUI();
});

els.modeHumanHuman.addEventListener('click', () => {
  state.mode = 'human-human';
  els.modeHumanHuman.classList.add('active');
  els.modeHumanAI.classList.remove('active');
  state.playerOName = 'Người Chơi 2';
  updateUI();
});

// Difficulty buttons
document.querySelectorAll('.diff-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.difficulty = btn.dataset.diff;
  });
});

// Canvas resize handled by CSS

// ======================== START ========================
// Script is deferred to end of <body>, so DOM is already ready — call directly.
runLoadingSequence();
