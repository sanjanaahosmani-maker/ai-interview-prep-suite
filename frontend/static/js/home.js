/**
 * Home page functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    // Load saved API provider
    const savedProvider = localStorage.getItem('llmProvider') || 'groq';
    const apiKeyInput = document.getElementById('apiKey');
    
    // Load API key from session if available
    if (sessionStorage.getItem('apiKey')) {
        apiKeyInput.value = '••••••••••••••••';
        apiKeyInput.disabled = true;
        
        // Add button to change API key
        const container = apiKeyInput.parentElement;
        const changeBtn = document.createElement('button');
        changeBtn.type = 'button';
        changeBtn.className = 'btn btn-sm btn-secondary mt-2';
        changeBtn.textContent = 'Change API Key';
        changeBtn.onclick = () => {
            sessionStorage.removeItem('apiKey');
            apiKeyInput.value = '';
            apiKeyInput.disabled = false;
            changeBtn.remove();
        };
        container.appendChild(changeBtn);
    }
});

/**
 * Save API key and provider
 */
function saveApiKey() {
    const provider = document.getElementById('llmProvider').value;
    const apiKey = document.getElementById('apiKey').value.trim();
    
    if (!apiKey) {
        showAlert('Please enter an API key', 'warning');
        return;
    }
    
    if (apiKey.length < 10) {
        showAlert('API key seems too short', 'warning');
        return;
    }
    
    // Save to localStorage and sessionStorage
    localStorage.setItem('llmProvider', provider);
    sessionStorage.setItem('apiKey', apiKey);
    
    // Update global config
    API_CONFIG.provider = provider;
    API_CONFIG.apiKey = apiKey;
    
    showAlert(
        `✓ API key configured successfully!\nProvider: ${provider}\nYou can now use all features.`,
        'success',
        4000
    );
    
    // Update the input display
    setTimeout(() => {
        document.getElementById('apiKey').value = '••••••••••••••••';
        document.getElementById('apiKey').disabled = true;
        
        const container = document.getElementById('apiKey').parentElement;
        if (!container.querySelector('.btn-secondary')) {
            const changeBtn = document.createElement('button');
            changeBtn.type = 'button';
            changeBtn.className = 'btn btn-sm btn-secondary mt-2';
            changeBtn.textContent = 'Change API Key';
            changeBtn.onclick = () => {
                sessionStorage.removeItem('apiKey');
                document.getElementById('apiKey').value = '';
                document.getElementById('apiKey').disabled = false;
                changeBtn.remove();
            };
            container.appendChild(changeBtn);
        }
    }, 500);
}
