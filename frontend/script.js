const API_BASE_URL = '';
const REVIEW_ENDPOINT = `${API_BASE_URL}/review_code`;

const codeInput = document.getElementById('code-input');
const languageInput = document.getElementById('language-input');
const reviewBtn = document.getElementById('review-btn');
const resultsSection = document.getElementById('results-section');
const summaryDiv = document.getElementById('summary');
const issuesDiv = document.getElementById('issues');
const suggestionsDiv = document.getElementById('suggestions');
const improvedCodeDiv = document.getElementById('improved-code');
const improvedCodeCard = document.getElementById('improved-code-card');
const errorMessage = document.getElementById('error-message');
const copyBtn = document.getElementById('copy-btn');

function setLoading(isLoading) {
    const btnText = reviewBtn.querySelector('.btn-text');
    const btnLoader = reviewBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        reviewBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        reviewBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function showError(message) {
    errorMessage.textContent = `❌ Error: ${message}`;
    errorMessage.style.display = 'block';
    resultsSection.style.display = 'none';
    
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
}

function getSeverityBadge(severity) {
    const badges = {
        'critical': '<span class="badge badge-critical">CRITICAL</span>',
        'high': '<span class="badge badge-high">HIGH</span>',
        'medium': '<span class="badge badge-medium">MEDIUM</span>',
        'low': '<span class="badge badge-low">LOW</span>'
    };
    return badges[severity?.toLowerCase()] || '<span class="badge">UNKNOWN</span>';
}

function getIssueTypeIcon(type) {
    const icons = {
        'bug': '🐛',
        'security': '🔒',
        'performance': '⚡',
        'quality': '📝',
        'error': '❌'
    };
    return icons[type?.toLowerCase()] || '⚠️';
}

function displayResults(data) {
    hideError();
    
    summaryDiv.textContent = data.summary || 'No summary available.';
    
    if (data.issues && data.issues.length > 0) {
        issuesDiv.innerHTML = data.issues.map(issue => `
            <div class="issue-item">
                <div class="issue-header">
                    ${getIssueTypeIcon(issue.type)} 
                    <strong>${issue.type || 'Issue'}</strong>
                    ${getSeverityBadge(issue.severity)}
                    ${issue.line ? `<span class="line-number">Line ${issue.line}</span>` : ''}
                </div>
                <div class="issue-description">${issue.description || 'No description available.'}</div>
            </div>
        `).join('');
    } else {
        issuesDiv.innerHTML = '<p class="no-issues">No issues found! 🎉</p>';
    }
    
    if (data.suggestions && data.suggestions.length > 0) {
        suggestionsDiv.innerHTML = `
            <ul class="suggestions-list">
                ${data.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
            </ul>
        `;
    } else {
        suggestionsDiv.innerHTML = '<p class="no-suggestions">No suggestions at this time.</p>';
    }
    
    if (data.improved_code && data.improved_code.trim()) {
        improvedCodeDiv.textContent = data.improved_code;
        improvedCodeCard.style.display = 'block';
        
        const codeBlock = improvedCodeDiv.parentElement;
        codeBlock.className = 'code-block';
    } else {
        improvedCodeCard.style.display = 'none';
    }
    
    resultsSection.style.display = 'block';
    
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

copyBtn.addEventListener('click', async () => {
    const code = improvedCodeDiv.textContent;
    try {
        await navigator.clipboard.writeText(code);
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.classList.add('copied');
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.classList.remove('copied');
        }, 2000);
    } catch (err) {
        showError('Failed to copy code to clipboard');
    }
});

async function reviewCode() {
    const code = codeInput.value.trim();
    const language = languageInput.value.trim() || null;
    
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
            const error = new Error(errorData.detail?.message || errorData.detail || `HTTP error! status: ${response.status}`);
            error.response = response;
            throw error;
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error reviewing code:', error);
        
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            showError('Cannot connect to the server. Make sure the backend is running on http://localhost:8000');
        } else if (error.message.includes('quota') || error.message.includes('billing')) {
            showError('❌ OpenAI API Quota Exceeded. Please check your billing at https://platform.openai.com/account/billing');
        } else if (error.message.includes('401') || error.message.includes('Authentication')) {
            showError('❌ Invalid API Key. Please check your OPENAI_API_KEY in the backend/.env file');
        } else {
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
                }
            }
            showError(errorMsg);
        }
    } finally {
        setLoading(false);
    }
}

reviewBtn.addEventListener('click', reviewCode);

languageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        reviewCode();
    }
});

codeInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        reviewCode();
    }
});

codeInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

