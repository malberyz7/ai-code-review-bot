# Google Gemini Setup (FREE & Reliable!)

Google Gemini is **FREE**, reliable, and works great for code review!

## Quick Setup (2 minutes):

1. **Get free API key:**
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with your Google account (free!)
   - Click "Create API Key"
   - Copy the key

2. **Update backend/.env:**
   ```bash
   cd backend
   nano .env
   ```
   
   Add or update these lines:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Restart server:**
   ```bash
   python3 run.py
   ```

**That's it!** Gemini is:
- ✅ FREE (generous free tier)
- ✅ Reliable (no endpoint issues)
- ✅ Fast
- ✅ No credit card required
- ✅ Works great for code review

## Benefits over Hugging Face:
- No deprecated endpoints
- More reliable
- Better code understanding
- Faster responses

