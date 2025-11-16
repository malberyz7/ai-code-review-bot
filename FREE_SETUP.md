# Free AI Provider Setup Guide

Since you don't have a budget for OpenAI, here are **FREE alternatives** that work great!

## Option 1: Hugging Face (Recommended - Completely Free)

Hugging Face offers free API access with generous limits.

### Setup Steps:

1. **Create a free account** at https://huggingface.co
2. **Get your API token**:
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Name it "code-review-bot"
   - **IMPORTANT**: Make sure to select **"Inference API"** permission (not just "Read")
   - Copy the token

3. **Update your `.env` file** in the `backend` directory:
   ```bash
   cd backend
   nano .env  # or use any text editor
   ```

4. **Add these lines**:
   ```
   AI_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=your_token_here
   HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
   ```

5. **Restart the server**:
   ```bash
   python3 run.py
   ```

**That's it!** No credit card required, completely free!

---

## Option 2: Groq (Free & Very Fast)

Groq offers free API access with very fast inference.

### Setup Steps:

1. **Create a free account** at https://console.groq.com
2. **Get your API key**:
   - Go to https://console.groq.com/keys
   - Click "Create API Key"
   - Copy the key

3. **Update your `.env` file**:
   ```
   AI_PROVIDER=groq
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL=llama-3.1-8b-instant
   ```

4. **Restart the server**

---

## Option 3: Use Hugging Face Without API Key (Slower)

You can use Hugging Face's public API without an API key, but it's slower and has rate limits.

Just set:
```
AI_PROVIDER=huggingface
HUGGINGFACE_API_KEY=
```

---

## Comparison

| Provider | Cost | Speed | Quality | Setup Difficulty |
|----------|------|-------|---------|------------------|
| Hugging Face | FREE | Medium | Good | Easy ⭐ |
| Groq | FREE | Very Fast | Good | Easy ⭐ |
| OpenAI | Paid | Fast | Excellent | Easy ⭐ |

---

## Troubleshooting

### "Model is loading" error (Hugging Face)
- Wait 30-60 seconds and try again
- The model needs to load on first use
- Consider using Groq for faster responses

### Rate limit errors
- Hugging Face free tier has rate limits
- Wait a few seconds between requests
- Groq has higher rate limits

### API key errors
- Make sure there are no extra spaces in your `.env` file
- Restart the server after changing `.env`
- Check that the API key is correct

---

## Need Help?

1. Check your `.env` file is in the `backend/` directory
2. Make sure `AI_PROVIDER` is set correctly
3. Restart the server after making changes
4. Check the server logs for error messages

**Happy coding! 🚀**

