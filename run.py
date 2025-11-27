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
    PORT = 8001
    print("🚀 Starting AI Code Review Bot...")
    print(f"📡 Backend API: http://localhost:{PORT}")
    print(f"🌐 Frontend UI: http://localhost:{PORT}")
    print(f"📚 API Docs: http://localhost:{PORT}/docs")
    print(f"\n✨ Open http://localhost:{PORT} in your browser to use the app!")
    print("Press Ctrl+C to stop the server\n")
    
    subprocess.run([
        str(venv_python),
        "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", str(PORT),
        "--reload"
    ])

