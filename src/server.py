import os
import sys
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

# Ensure src/ is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from board import Board
from ai import get_ai_move
from database import init_db, get_stats, update_match_result

# The frontend code is at the project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Khởi tạo DB khi load server
init_db()

app = FastAPI(title="Gomoku AI API")

class MoveRequest(BaseModel):
    grid: List[List[Optional[str]]]
    ai_player: str = 'O'
    human_player: str = 'X'
    difficulty: str = 'medium'

@app.post("/api/move")
def get_move(req: MoveRequest):
    try:
        board = Board()
        for r in range(board.size):
            for c in range(board.size):
                board.grid[r][c] = req.grid[r][c]
        
        # Call original Python AI
        move = get_ai_move(
            board,
            ai_player=req.ai_player,
            human_player=req.human_player,
            difficulty=req.difficulty,
        )
        return {"move": move}
    except Exception as e:
        return {"error": str(e)}

class MatchResultRequest(BaseModel):
    result: str # 'win', 'loss', 'draw'

@app.get("/api/stats")
def fetch_stats():
    return get_stats()

@app.post("/api/match_end")
def match_end(req: MatchResultRequest):
    return update_match_result(req.result)


# Serve static files from the project root (index.html, game.js, style.css)
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    print("=======================================")
    print("Gomoku Web Server running with FastAPI!")
    print("Open http://localhost:7891 in browser.")
    print("=======================================")
    uvicorn.run("server:app", host="0.0.0.0", port=7891, reload=True)
