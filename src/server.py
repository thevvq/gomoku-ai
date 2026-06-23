import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

# Ensure src/ is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from board import Board
from ai import get_ai_move

# Serve files from the project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

class GomokuServer(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/move':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                grid = data.get('grid')
                ai_player = data.get('ai_player', 'O')
                human_player = data.get('human_player', 'X')
                
                # Reconstruct the board from JS array
                board = Board()
                for r in range(board.size):
                    for c in range(board.size):
                        board.grid[r][c] = grid[r][c]
                
                # Call original Python AI
                move = get_ai_move(board, ai_player=ai_player, human_player=human_player)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {'move': move}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = 7890
    server_address = ('', port)
    httpd = HTTPServer(server_address, GomokuServer)
    print(f"=======================================")
    print(f"Gomoku Web Server running!")
    print(f"Open http://localhost:{port} in browser.")
    print(f"=======================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()
