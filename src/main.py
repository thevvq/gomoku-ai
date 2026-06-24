import sys
import os

# Ensure src/ is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    print("=======================================")
    print("Starting Gomoku Web Server with FastAPI...")
    print("Open http://localhost:7891 in your browser.")
    print("=======================================")
    # Run the FastAPI app located in src.server
    uvicorn.run("server:app", host="0.0.0.0", port=7891, reload=True)