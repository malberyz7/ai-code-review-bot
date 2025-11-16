# Quick Fix: Switch to Groq (Recommended)

Hugging Face endpoints are currently deprecated/unstable. **Groq is FREE, fast, and reliable!**

## Quick Setup (2 minutes):

1. **Get free API key:**
   - Go to: https://console.groq.com
   - Sign up (free, no credit card)
   - Go to: https://console.groq.com/keys
   - Click "Create API Key"
   - Copy the key

2. **Update backend/.env:**
   ```bash
   cd backend
   nano .env
   ```
   
   Change these lines:
   ```
   AI_PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Restart server:**
   ```bash
   python3 run.py
   ```

**That's it!** Groq is:
- ✅ FREE
- ✅ Very fast (faster than Hugging Face)
- ✅ Reliable (no endpoint issues)
- ✅ No credit card required

