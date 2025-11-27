/** Main application logic and event handlers. */

/**
 * Main function to review code.
 */
async function reviewCode() {
    const code = DOM.codeInput.value.trim();
    const language = DOM.languageInput.value.trim() || null;
    
    if (!code) {
        showError('Please enter some code to review.');
        return;
    }
    
    if (code.length > 10000) {
        showError('Code is too long. Maximum length is 10,000 characters.');
        return;
    }
    
    setLoading(true);
    hideError();
    
    try {
        const data = await reviewCodeAPI(code, language);
        displayResults(data);
    } catch (error) {
        handleAPIError(error);
    } finally {
        setLoading(false);
    }
}

/**
 * Copy improved code to clipboard.
 */
async function copyImprovedCode() {
    const code = DOM.improvedCodeDiv.textContent;
    try {
        await navigator.clipboard.writeText(code);
        const originalText = DOM.copyBtn.textContent;
        DOM.copyBtn.textContent = '✓ Copied!';
        DOM.copyBtn.classList.add('copied');
        setTimeout(() => {
            DOM.copyBtn.textContent = originalText;
            DOM.copyBtn.classList.remove('copied');
        }, 2000);
    } catch (err) {
        showError('Failed to copy code to clipboard');
    }
}

/**
 * Initialize event listeners.
 */
function initializeEventListeners() {
    DOM.reviewBtn.addEventListener('click', reviewCode);
    
    DOM.languageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            reviewCode();
        }
    });
    
    DOM.codeInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            reviewCode();
        }
    });
    
    DOM.codeInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    DOM.copyBtn.addEventListener('click', copyImprovedCode);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEventListeners);
} else {
    initializeEventListeners();
}

