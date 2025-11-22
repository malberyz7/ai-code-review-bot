#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

project_root = Path(__file__).parent
backend_dir = project_root / "backend"
venv_python = backend_dir / "venv" / "bin" / "python"

if not venv_python.exists():
    print("❌ Virtual environment not found!")
    print("\nPlease set up the backend first:")
    print("  cd backend")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")
    print("  cd ..")
    print("\nThen run: python3 run.py")
    sys.exit(1)

os.chdir(backend_dir)

if __name__ == "__main__":
    print("🚀 Starting AI Code Review Bot...")
    print("📡 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n✨ Open http://localhost:8000 in your browser to use the app!")
    print("Press Ctrl+C to stop the server\n")
    
    subprocess.run([
        str(venv_python),
        "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

