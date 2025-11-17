# AI Code Review Bot

An AI-powered code review service that analyzes code snippets for quality issues, bugs, security vulnerabilities, and performance problems. Built with FastAPI backend and a clean, modern web frontend.

## 🎥 Project Video Tutorial

**Watch the complete tutorial and demo:**

👉 **[https://www.youtube.com/watch?v=VL9WoG0X21o](https://www.youtube.com/watch?v=VL9WoG0X21o)**

---

## Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini (FREE) for comprehensive code reviews
- 🔍 **Multi-Aspect Review**: Analyzes code quality, bugs, security, and performance
- 💡 **Actionable Suggestions**: Provides specific improvement recommendations
- ✨ **Code Improvements**: Suggests optimized versions of your code
- 🎨 **Clean UI**: Modern, responsive web interface with beautiful design
- 🚀 **Fast & Easy**: Simple setup and immediate results
- 💰 **Free**: Uses Google Gemini API (completely free)

## Project Structure

```
AI Code Review Bot/
├── backend/
│   ├── main.py              # FastAPI application (serves both API and frontend)
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── script.js            # Frontend JavaScript
│   └── style.css            # Styling
├── run.py                   # Unified launcher (run this to start everything)
└── README.md                # This file
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (FREE) - [Get free API key](https://makersuite.google.com/app/apikey)
- A modern web browser

> 💡 **Note**: This project uses Google Gemini by default. The code infrastructure supports other providers (OpenAI, Hugging Face, Groq) but they are not configured. See [GEMINI_SETUP.md](GEMINI_SETUP.md) for setup instructions.

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Google Gemini API key:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=models/gemini-2.0-flash
   ```
   
   Get your free API key at: https://makersuite.google.com/app/apikey

### 2. Running the Application

#### Unified Launcher (Recommended)

From the project root directory, simply run:

```bash
python3 run.py
```

**Note**: On macOS and some Linux systems, use `python3` instead of `python`.

This will start both the backend API and serve the frontend together at `http://localhost:8000`

**That's it!** Open `http://localhost:8000` in your browser to use the application.

#### Alternative: Run Backend Separately

If you prefer to run the backend separately:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload
```

The frontend will be automatically served at `http://localhost:8000` and the API will be available at the same address.

#### Useful URLs

- **Frontend UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## How It Works

### Backend (FastAPI)

The backend provides a REST API endpoint `/review_code` that:

1. Accepts code snippets via POST request
2. Sends the code to Google Gemini API with a carefully crafted prompt
3. Parses the AI response to extract:
   - Summary of the code
   - List of issues (bugs, security, performance, quality)
   - Improvement suggestions
   - Improved/optimized code version
4. Returns structured JSON response

**Key Features:**
- Uses Google Gemini API (free and reliable)
- Input validation (empty code, length limits)
- Error handling for API failures
- CORS enabled for frontend communication
- No data storage (privacy-focused)

### Frontend (HTML/CSS/JavaScript)

The frontend provides a user-friendly interface that:

1. Allows users to paste code into a text area
2. Optionally specify the programming language
3. Sends the code to the backend API
4. Displays results in organized sections:
   - **Summary**: Overall assessment
   - **Issues Found**: Categorized issues with severity badges
   - **Suggestions**: Actionable improvement recommendations
   - **Improved Code**: Optimized version (if available)

**Features:**
- Responsive design (works on mobile, tablet, desktop)
- Real-time loading states
- Error handling and user feedback
- Copy-to-clipboard for improved code
- Keyboard shortcuts (Ctrl/Cmd + Enter to submit)

### AI Analysis Process

Google Gemini analyzes code by:

1. **Code Quality**: Checks readability, maintainability, and style consistency
2. **Bugs & Logic**: Identifies potential runtime errors and logical flaws
3. **Security**: Detects vulnerabilities like SQL injection, XSS, insecure dependencies
4. **Performance**: Identifies bottlenecks, inefficient algorithms, memory leaks
5. **Best Practices**: Suggests modern patterns and conventions

The analysis is returned in a structured JSON format for easy parsing and display.

**AI Provider:**
- **Google Gemini**: Free, fast, and reliable. Uses `models/gemini-2.0-flash` by default.

## API Endpoints

### POST `/review_code`

Review a code snippet.

**Request Body:**
```json
{
  "code": "function example() { console.log('Hello'); }",
  "language": "javascript"  // optional
}
```

**Response:**
```json
{
  "summary": "Brief summary of the code...",
  "issues": [
    {
      "type": "quality",
      "severity": "low",
      "description": "Issue description",
      "line": "5"
    }
  ],
  "suggestions": [
    "Suggestion 1",
    "Suggestion 2"
  ],
  "improved_code": "// Improved version..."
}
```

### GET `/`

Health check endpoint.

**Response:**
```json
{
  "message": "AI Code Review Bot API",
  "status": "running",
  "endpoints": {
    "review": "/review_code",
    "docs": "/docs"
  }
}
```

## Usage Tips

1. **Language Detection**: While optional, specifying the language helps the AI provide more accurate analysis
2. **Code Length**: Keep code snippets under 10,000 characters for best results
3. **Multiple Reviews**: You can review multiple code snippets in sequence
4. **Copy Results**: Use the "Copy Code" button to quickly copy improved code versions

## Troubleshooting

### Backend Issues

- **"GEMINI_API_KEY environment variable is not set"**: Make sure you've created a `.env` file with your Gemini API key
- **Connection errors**: Ensure the backend is running on port 8000
- **API errors**: Check your Gemini API key is valid
- **Gemini errors**: Make sure `google-generativeai` package is installed (`pip install google-generativeai`)
- **Model not found**: Update the model name in `.env` (e.g., `GEMINI_MODEL=models/gemini-2.0-flash`)

### Frontend Issues

- **Cannot connect to server**: Verify the backend is running and check the `API_BASE_URL` in `script.js`
- **CORS errors**: The backend has CORS enabled for all origins. If issues persist, check browser console
- **Results not displaying**: Check browser console for JavaScript errors

## Security Notes

- The application does not store any user data
- API keys should never be committed to version control
- In production, restrict CORS origins to your frontend domain
- Consider rate limiting for production deployments

## Setup Guide

- **[GEMINI_SETUP.md](GEMINI_SETUP.md)**: Detailed setup guide for Google Gemini

## Future Enhancements

Potential improvements:
- Support for file uploads
- History of reviews (with user authentication)
- Export results as PDF
- Integration with version control systems
- Batch code review

## License

This project is open source and available for educational and personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Built with ❤️ using FastAPI, Google Gemini, and vanilla JavaScript**

**Made by malberyz7 and Lukanbaster**

