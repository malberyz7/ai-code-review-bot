# AI Code Review Bot

An AI-powered code review service that analyzes code snippets for quality issues, bugs, security vulnerabilities, and performance problems. Built with FastAPI backend and a clean, modern web frontend.

## Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT-4 to provide comprehensive code reviews
- 🔍 **Multi-Aspect Review**: Analyzes code quality, bugs, security, and performance
- 💡 **Actionable Suggestions**: Provides specific improvement recommendations
- ✨ **Code Improvements**: Suggests optimized versions of your code
- 🎨 **Clean UI**: Modern, responsive web interface
- 🚀 **Fast & Easy**: Simple setup and immediate results

## Project Structure

```
AI Code Review Bot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── script.js            # Frontend JavaScript
│   └── style.css            # Styling
└── README.md                # This file
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- A modern web browser

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
   
   Then edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

### 2. Running the Application

#### Start the Backend Server

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

You can also access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Open the Frontend

Simply open `frontend/index.html` in your web browser, or use a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8080
```

Then navigate to `http://localhost:8080` in your browser.

**Note**: If you use a different port for the frontend, make sure to update the `API_BASE_URL` in `frontend/script.js` accordingly.

## How It Works

### Backend (FastAPI)

The backend provides a REST API endpoint `/review_code` that:

1. Accepts code snippets via POST request
2. Sends the code to OpenAI's GPT-4 model with a carefully crafted prompt
3. Parses the AI response to extract:
   - Summary of the code
   - List of issues (bugs, security, performance, quality)
   - Improvement suggestions
   - Improved/optimized code version
4. Returns structured JSON response

**Key Features:**
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

The AI model analyzes code by:

1. **Code Quality**: Checks readability, maintainability, and style consistency
2. **Bugs & Logic**: Identifies potential runtime errors and logical flaws
3. **Security**: Detects vulnerabilities like SQL injection, XSS, insecure dependencies
4. **Performance**: Identifies bottlenecks, inefficient algorithms, memory leaks
5. **Best Practices**: Suggests modern patterns and conventions

The analysis is returned in a structured JSON format for easy parsing and display.

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

- **"OPENAI_API_KEY environment variable is not set"**: Make sure you've created a `.env` file with your API key
- **Connection errors**: Ensure the backend is running on port 8000
- **API errors**: Check your OpenAI API key is valid and you have sufficient credits

### Frontend Issues

- **Cannot connect to server**: Verify the backend is running and check the `API_BASE_URL` in `script.js`
- **CORS errors**: The backend has CORS enabled for all origins. If issues persist, check browser console
- **Results not displaying**: Check browser console for JavaScript errors

## Security Notes

- The application does not store any user data
- API keys should never be committed to version control
- In production, restrict CORS origins to your frontend domain
- Consider rate limiting for production deployments

## Future Enhancements

Potential improvements:
- Support for file uploads
- History of reviews (with user authentication)
- Multiple AI model options
- Export results as PDF
- Integration with version control systems
- Batch code review

## License

This project is open source and available for educational and personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Built with ❤️ using FastAPI, OpenAI GPT-4, and vanilla JavaScript**

