/**
 * Study Concepts functionality
 */

let currentConcepts = {};

document.addEventListener('DOMContentLoaded', () => {
    initializeStudyConcepts();
});

function initializeStudyConcepts() {
    // Setup event listeners if needed
}

/**
 * Load study concepts
 */
async function loadConcepts() {
    if (!checkApiKey()) return;
    
    const role = document.getElementById('studyRole').value;
    const level = document.getElementById('studyLevel').value;
    
    if (!role) {
        showAlert('Please select a target role', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        const response = await apiRequest('/study/concepts', {
            method: 'POST',
            body: JSON.stringify({
                role,
                experience_level: level
            })
        });
        
        if (response.success) {
            currentConcepts = response.concepts || {};
            displayConcepts(currentConcepts, role);
            showAlert(`✓ Loaded study path for ${role}!`, 'success', 3000);
        } else {
            showAlert('Failed to load concepts', 'danger');
        }
    } catch (error) {
        console.error('Error loading concepts:', error);
        showAlert('Error loading concepts. Please try again.', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Display concepts
 */
function displayConcepts(concepts, role) {
    const container = document.getElementById('conceptsContainer');
    const emptyState = document.getElementById('emptyStudyState');
    
    if (!container) return;
    
    if (!concepts || Object.keys(concepts).length === 0) {
        container.innerHTML = '';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }
    
    let html = '';
    let topicIndex = 0;
    
    // Handle if concepts is an object with difficulty levels
    for (const [level, topics] of Object.entries(concepts)) {
        if (!Array.isArray(topics) || topics.length === 0) continue;
        
        html += `
            <div class="mb-4">
                <h5 class="text-capitalize mb-3">
                    <span class="badge bg-primary">${escapeHtml(level)}</span>
                </h5>
        `;
        
        topics.forEach(topic => {
            const badge = level.includes('beginner') ? 'success' : 
                         level.includes('intermediate') ? 'warning' : 'danger';
            
            html += `
                <div class="card topic-card mb-2" onclick="openTopicModal('${escapeHtml(topic.topic || '')}', '${escapeHtml(role)}')">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="card-title">${escapeHtml(topic.topic || '')}</h6>
                                <p class="card-text text-muted small">${escapeHtml(topic.description || '')}</p>
                            </div>
                            <span class="badge bg-${badge}">${escapeHtml(level)}</span>
                        </div>
                        ${topic.key_points ? `
                            <small class="text-muted">
                                <i class="fas fa-bookmark"></i> ${topic.key_points.slice(0, 3).join(', ')}
                            </small>
                        ` : ''}
                    </div>
                </div>
            `;
            topicIndex++;
        });
        
        html += '</div>';
    }
    
    container.innerHTML = html;
    if (emptyState) emptyState.style.display = 'none';
}

/**
 * Open topic detail modal
 */
async function openTopicModal(topic, role) {
    if (!topic) return;
    
    const modal = new bootstrap.Modal(document.getElementById('topicModal'));
    
    document.getElementById('topicModalTitle').textContent = topic;
    document.getElementById('topicContent').innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';
    
    // Fetch topic details
    try {
        const response = await apiRequest(`/study/topic/${encodeURIComponent(topic)}?role=${encodeURIComponent(role)}`, {
            method: 'GET'
        });
        
        if (response.success && response.topic_details) {
            displayTopicDetails(response.topic_details);
        } else {
            displayTopicDetails(getDefaultTopicDetails(topic));
        }
    } catch (error) {
        console.error('Error fetching topic details:', error);
        displayTopicDetails(getDefaultTopicDetails(topic));
    }
    
    modal.show();
}

/**
 * Display topic details in modal
 */
function displayTopicDetails(details) {
    const content = document.getElementById('topicContent');
    
    let html = `
        <div class="topic-details">
            ${details.description ? `
                <div class="mb-3">
                    <h6>Overview</h6>
                    <p>${escapeHtml(details.description)}</p>
                </div>
            ` : ''}
            
            ${details.key_concepts && details.key_concepts.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="fas fa-list"></i> Key Concepts</h6>
                    <ul>
                        ${details.key_concepts.map(c => `<li>${escapeHtml(c)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${details.key_points && details.key_points.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="fas fa-check"></i> Key Points</h6>
                    <ul>
                        ${details.key_points.map(p => `<li>${escapeHtml(p)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${details.example_problems && details.example_problems.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="fas fa-code"></i> Example Problems</h6>
                    <ul>
                        ${details.example_problems.map(p => `<li><code>${escapeHtml(p)}</code></li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${details.common_mistakes && details.common_mistakes.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="fas fa-exclamation-triangle text-warning"></i> Common Mistakes</h6>
                    <ul>
                        ${details.common_mistakes.map(m => `<li>${escapeHtml(m)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${details.resources && details.resources.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="fas fa-link"></i> Resources</h6>
                    <ul>
                        ${details.resources.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
    
    document.getElementById('topicContent').innerHTML = html;
}

/**
 * Get default topic details if API call fails
 */
function getDefaultTopicDetails(topic) {
    return {
        topic: topic,
        description: `Learn about ${topic} - an important topic in your interview preparation.`,
        key_points: [
            'Master the fundamentals',
            'Practice with real examples',
            'Understand common interview questions',
            'Review edge cases'
        ],
        resources: [
            'Official documentation',
            'Online tutorials',
            'Practice problems',
            'Coding platforms'
        ]
    };
}
