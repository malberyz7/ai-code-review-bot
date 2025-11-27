/** Utility functions for UI and formatting. */

/**
 * Set loading state for review button.
 * @param {boolean} isLoading - Whether to show loading state
 */
function setLoading(isLoading) {
    const btnText = DOM.reviewBtn.querySelector('.btn-text');
    const btnLoader = DOM.reviewBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        DOM.reviewBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
    } else {
        DOM.reviewBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * Show error message.
 * @param {string} message - Error message to display
 */
function showError(message) {
    DOM.errorMessage.textContent = `❌ Error: ${message}`;
    DOM.errorMessage.style.display = 'block';
    DOM.resultsSection.style.display = 'none';
    
    setTimeout(() => {
        DOM.errorMessage.style.display = 'none';
    }, 5000);
}

/**
 * Hide error message.
 */
function hideError() {
    DOM.errorMessage.style.display = 'none';
}

/**
 * Get severity badge HTML.
 * @param {string} severity - Severity level
 * @returns {string} Badge HTML
 */
function getSeverityBadge(severity) {
    const badges = {
        'critical': '<span class="badge badge-critical">CRITICAL</span>',
        'high': '<span class="badge badge-high">HIGH</span>',
        'medium': '<span class="badge badge-medium">MEDIUM</span>',
        'low': '<span class="badge badge-low">LOW</span>'
    };
    return badges[severity?.toLowerCase()] || '<span class="badge">UNKNOWN</span>';
}

/**
 * Get issue type icon.
 * @param {string} type - Issue type
 * @returns {string} Icon emoji
 */
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

