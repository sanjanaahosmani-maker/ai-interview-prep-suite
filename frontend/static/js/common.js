/**
 * Common JavaScript utilities for AI Interview Prep Suite
 */

// API Base URL
const API_BASE = '/api';

// Session storage for API configuration
const API_CONFIG = {
    provider: localStorage.getItem('llmProvider') || 'groq',
    apiKey: sessionStorage.getItem('apiKey') || ''
};

/**
 * Show loading spinner
 */
function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.add('show');
    }
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.remove('show');
    }
}

/**
 * Make API request
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise} - API response
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_CONFIG.apiKey
        },
        credentials: 'include'
    };

    const mergedOptions = { ...defaultOptions, ...options };
    
    console.log('API Request:', { url, method: mergedOptions.method });
    
    try {
        const response = await fetch(url, mergedOptions);
        
        console.log('API Response Status:', response.status);
        
        if (!response.ok) {
            let errorData = {};
            try {
                errorData = await response.json();
            } catch (e) {
                errorData = { error: `HTTP ${response.status}` };
            }
            console.error('API Error Response:', errorData);
            throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('API Response Data:', data);
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Show alert notification
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, danger, warning, info)
 * @param {number} duration - Duration in ms (0 = persistent)
 */
function showAlert(message, type = 'info', duration = 5000) {
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show position-fixed" 
             role="alert" style="top: 20px; right: 20px; z-index: 1000; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', alertHTML);
    
    if (duration > 0) {
        setTimeout(() => {
            const element = document.getElementById(alertId);
            if (element) element.remove();
        }, duration);
    }
}

/**
 * Save API configuration
 */
function saveApiKey() {
    const provider = document.getElementById('llmProvider')?.value || 'groq';
    const apiKey = document.getElementById('apiKey')?.value || '';
    
    if (!apiKey) {
        showAlert('Please enter an API key', 'warning');
        return;
    }
    
    localStorage.setItem('llmProvider', provider);
    sessionStorage.setItem('apiKey', apiKey);
    
    // Update global config
    API_CONFIG.provider = provider;
    API_CONFIG.apiKey = apiKey;
    
    showAlert(`API key saved (${provider})`, 'success');
}

/**
 * Check if API key is configured
 */
function checkApiKey() {
    // API Key is managed in the backend .env file, so we bypass frontend checks to make it easier to test.
    return true;
}

/**
 * Format date
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Escape HTML
 * @param {string} text - Text to escape
 * @returns {string} - Escaped text
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success', 2000);
    }).catch(err => {
        showAlert('Failed to copy', 'danger');
    });
}

/**
 * Download text as file
 * @param {string} text - Text content
 * @param {string} filename - Output filename
 * @param {string} type - MIME type
 */
function downloadAsFile(text, filename, type = 'text/plain') {
    const element = document.createElement('a');
    element.setAttribute('href', `data:${type};charset=utf-8,${encodeURIComponent(text)}`);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/**
 * Convert markdown to HTML (basic)
 * @param {string} markdown - Markdown text
 * @returns {string} - HTML text
 */
function markdownToHtml(markdown) {
    let html = markdown
        .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
        .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
        .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^- (.*?)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        .replace(/\n/g, '<br>');
    
    return html;
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Get form data as object
 * @param {HTMLFormElement} form - Form element
 * @returns {object} - Form data
 */
function getFormData(form) {
    const data = {};
    new FormData(form).forEach((value, key) => {
        data[key] = value;
    });
    return data;
}

/**
 * Validate email
 * @param {string} email - Email to validate
 * @returns {boolean}
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Get roles list
 */
async function getRoles() {
    try {
        const data = await apiRequest('/roles');
        return data.roles || [];
    } catch (error) {
        console.error('Failed to get roles:', error);
        return [];
    }
}

/**
 * Get experience levels
 */
async function getExperienceLevels() {
    try {
        const data = await apiRequest('/experience-levels');
        return data.levels || ['junior', 'mid', 'senior'];
    } catch (error) {
        console.error('Failed to get levels:', error);
        return ['junior', 'mid', 'senior'];
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTooltips();
    
    // Load API configuration from localStorage
    const savedProvider = localStorage.getItem('llmProvider');
    if (document.getElementById('llmProvider')) {
        document.getElementById('llmProvider').value = savedProvider || 'groq';
    }
});
