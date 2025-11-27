/** API communication functions. */

/**
 * Review code by sending request to API.
 * @param {string} code - Code to review
 * @param {string|null} language - Optional programming language
 * @returns {Promise<Object>} Review data
 */
async function reviewCodeAPI(code, language) {
    const response = await fetch(REVIEW_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: code,
            language: language
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        const error = new Error(
            errorData.detail?.message || errorData.detail || `HTTP error! status: ${response.status}`
        );
        error.response = response;
        throw error;
    }
    
    return await response.json();
}

/**
 * Handle API errors and show appropriate messages.
 * @param {Error} error - Error object
 */
async function handleAPIError(error) {
    console.error('Error reviewing code:', error);
    
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        showError('Cannot connect to the server. Make sure the backend is running on http://localhost:8001');
        return;
    }
    
    if (error.message.includes('quota') || error.message.includes('billing')) {
        showError('❌ OpenAI API Quota Exceeded. Please check your billing at https://platform.openai.com/account/billing');
        return;
    }
    
    if (error.message.includes('401') || error.message.includes('Authentication')) {
        showError('❌ Invalid API Key. Please check your OPENAI_API_KEY in the backend/.env file');
        return;
    }
    
    let errorMsg = error.message || 'An unexpected error occurred. Please try again.';
    if (error.response) {
        try {
            const errorData = await error.response.json();
            if (errorData.detail && typeof errorData.detail === 'object') {
                errorMsg = errorData.detail.message || errorData.detail.error || errorMsg;
            } else if (errorData.detail) {
                errorMsg = errorData.detail;
            }
        } catch (e) {
            // Use default error message if JSON parsing fails
        }
    }
    
    showError(errorMsg);
}

