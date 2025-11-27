/** UI rendering functions. */

/**
 * Display code review results.
 * @param {Object} data - Review data from API
 */
function displayResults(data) {
    hideError();
    
    DOM.summaryDiv.textContent = data.summary || 'No summary available.';
    
    displayIssues(data.issues);
    displaySuggestions(data.suggestions);
    displayImprovedCode(data.improved_code);
    
    DOM.resultsSection.style.display = 'block';
    DOM.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display issues.
 * @param {Array} issues - Array of issue objects
 */
function displayIssues(issues) {
    if (issues && issues.length > 0) {
        DOM.issuesDiv.innerHTML = issues.map(issue => `
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
        DOM.issuesDiv.innerHTML = '<p class="no-issues">No issues found! 🎉</p>';
    }
}

/**
 * Display suggestions.
 * @param {Array} suggestions - Array of suggestion strings
 */
function displaySuggestions(suggestions) {
    if (suggestions && suggestions.length > 0) {
        DOM.suggestionsDiv.innerHTML = `
            <ul class="suggestions-list">
                ${suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
            </ul>
        `;
    } else {
        DOM.suggestionsDiv.innerHTML = '<p class="no-suggestions">No suggestions at this time.</p>';
    }
}

/**
 * Display improved code.
 * @param {string|null} improvedCode - Improved code or null
 */
function displayImprovedCode(improvedCode) {
    if (improvedCode && improvedCode.trim()) {
        DOM.improvedCodeDiv.textContent = improvedCode;
        DOM.improvedCodeCard.style.display = 'block';
        
        const codeBlock = DOM.improvedCodeDiv.parentElement;
        codeBlock.className = 'code-block';
    } else {
        DOM.improvedCodeCard.style.display = 'none';
    }
}

