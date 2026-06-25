import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gomoku_scores.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            draws INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0
        )
    ''')
    # Insert default row if not exists
    cursor.execute('SELECT COUNT(*) FROM user_stats WHERE id = 1')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO user_stats (id, wins, losses, draws, score) VALUES (1, 0, 0, 0, 0)')
    
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT wins, losses, draws, score FROM user_stats WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"wins": row[0], "losses": row[1], "draws": row[2], "score": row[3]}
    return {"wins": 0, "losses": 0, "draws": 0, "score": 0}

def update_match_result(result: str):
    """
    result: 'win', 'loss', 'draw'
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if result == 'win':
        cursor.execute('UPDATE user_stats SET wins = wins + 1, score = score + 2 WHERE id = 1')
    elif result == 'loss':
        cursor.execute('UPDATE user_stats SET losses = losses + 1, score = score - 1 WHERE id = 1')
    elif result == 'draw':
        cursor.execute('UPDATE user_stats SET draws = draws + 1 WHERE id = 1') # Score +0
        
    conn.commit()
    conn.close()
    return get_stats()
