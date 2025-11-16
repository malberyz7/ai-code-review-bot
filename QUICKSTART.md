# Quick Start Guide

## One Command to Run Everything

From the project root directory:

```bash
python3 run.py
```

**Note**: On macOS, use `python3` instead of `python`.

That's it! The application will start and you can access it at:

**🌐 http://localhost:8000**

## What Happens

- ✅ Backend API starts on port 8000
- ✅ Frontend is automatically served
- ✅ Everything works together seamlessly
- ✅ No need to run separate servers

## First Time Setup

If you haven't set up the environment yet:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
cd ..
python run.py
```

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

