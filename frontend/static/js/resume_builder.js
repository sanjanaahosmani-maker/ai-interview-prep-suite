/**
 * Resume Builder functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Resume builder JS loaded');
    initializeResumeBuilder();
});

function initializeResumeBuilder() {
    console.log('Initializing resume builder');
    // Setup form event listeners
    const form = document.getElementById('resumeForm');
    if (form) {
        console.log('Form found');
        form.addEventListener('submit', (e) => e.preventDefault());
    } else {
        console.error('Form not found!');
    }
}

/**
 * Generate resume from user input
 */
async function generateResume() {
    console.log('Generate Resume clicked');
    
    // Get form data
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const targetRole = document.getElementById('targetRole').value;
    const education = document.getElementById('education').value.trim();
    const experience = document.getElementById('experience').value.trim();
    const skills = document.getElementById('skills').value.trim();
    const projects = document.getElementById('projects').value.trim();
    const certifications = document.getElementById('certifications').value.trim();
    
    console.log('Form data:', { name, email, targetRole, skills });
    
    // Validate required fields
    if (!name || !email || !targetRole || !skills) {
        showAlert('Please fill in Name, Email, Target Role, and Skills fields', 'warning');
        console.log('Validation failed - missing fields');
        return;
    }
    
    try {
        showLoading();
        
        console.log('Sending request to /api/resume/generate');
        
        const response = await apiRequest('/resume/generate', {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                phone,
                target_role: targetRole,
                education,
                experience,
                skills,
                projects,
                certifications
            })
        });
        
        console.log('Response received:', response);
        
        if (response.success) {
            console.log('Resume generated successfully');
            // Display resume
            displayResume(response.resume);
            
            // Get and display optimization suggestions (non-blocking)
            try {
                await getOptimizationSuggestions(response.resume, targetRole);
            } catch (suggestionError) {
                console.warn('Could not fetch optimization suggestions:', suggestionError);
                // Don't fail the whole flow if suggestions fail
            }
        } else {
            console.error('Response failed:', response.error);
            showAlert('Failed to generate resume: ' + (response.error || 'Unknown error'), 'danger');
        }
    } catch (error) {
        console.error('Error generating resume:', error);
        showAlert('Error: ' + error.message, 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Display resume with professional header
 */
function displayResume(resume) {
    const resumeCard = document.getElementById('resumeCard');
    const resumeContent = document.getElementById('resumeContent');
    const emptyState = document.getElementById('emptyState');
    
    if (!resumeCard || !resumeContent) return;
    
    // Get contact info from form
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const targetRole = document.getElementById('targetRole').value;
    
    // Create professional header with contact info
    let contactInfo = email;
    if (phone) contactInfo += ` • ${phone}`;
    
    const headerHTML = `
        <div class="resume-header" style="text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #333;">
            <h2 style="margin: 0; font-weight: 700; font-size: 24px;">${escapeHtml(name)}</h2>
            <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">
                <strong>${escapeHtml(targetRole)}</strong> | ${escapeHtml(contactInfo)}
            </p>
        </div>
    `;
    
    // Format resume content
    const formattedResume = formatResumeContent(resume);
    
    resumeContent.innerHTML = headerHTML + formattedResume;
    resumeCard.style.display = 'block';
    if (emptyState) emptyState.style.display = 'none';
    
    showAlert('✓ Resume generated successfully!', 'success', 3000);
}

/**
 * Format resume content for display — professional sections only
 */
function formatResumeContent(resume) {
    let html = resume;
    
    // Escape HTML
    html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    
    // Simple markdown-to-HTML conversion
    // Headers: ## to <h2>, ### to <h3>
    html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
    html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
    
    // Bold: **text** to <strong>text</strong>
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Line breaks: split by newlines and wrap in paragraphs
    let lines = html.split('\n');
    let processed = [];
    let inList = false;
    let listItems = [];
    
    for (let line of lines) {
        line = line.trim();
        if (!line) continue;
        
        if (line.startsWith('<h2>') || line.startsWith('<h3>')) {
            if (inList) {
                processed.push('<ul>' + listItems.join('') + '</ul>');
                listItems = [];
                inList = false;
            }
            processed.push(line);
        } else if (line.startsWith('- ')) {
            inList = true;
            listItems.push('<li>' + line.substring(2) + '</li>');
        } else {
            if (inList) {
                processed.push('<ul>' + listItems.join('') + '</ul>');
                listItems = [];
                inList = false;
            }
            processed.push('<p>' + line + '</p>');
        }
    }
    
    if (inList) {
        processed.push('<ul>' + listItems.join('') + '</ul>');
    }
    
    html = processed.join('');
    
    // Style headers with section divider
    html = html.replace(/<h2>(.*?)<\/h2>/gi, function(match, title) {
        return '<div class="resume-section-header"><strong style="font-size: 14px; letter-spacing: 0.5px; text-transform: uppercase; color: #222;">' + title + '</strong></div>';
    });

    // Style h3 as role/company titles
    html = html.replace(/<h3>(.*?)<\/h3>/gi, function(match, title) {
        return '<h3 class="resume-role-title" style="margin: 12px 0 4px 0; font-weight: 600; font-size: 15px;">' + title + '</h3>';
    });
    
    // Improve list styling
    html = html.replace(/<ul>/g, '<ul style="margin: 12px 0; padding-left: 20px;">');
    html = html.replace(/<li>/g, '<li style="margin: 6px 0; line-height: 1.6;">');
    
    // Improve paragraph spacing
    html = html.replace(/<p>/g, '<p style="margin: 8px 0; line-height: 1.6; font-size: 14px;">');

    return '<div class="resume-preview-content" style="font-family: Segoe UI, Tahoma, sans-serif; font-size: 14px; line-height: 1.6; color: #333;">' + html + '</div>';
}

/**
 * Get optimization suggestions
 */
async function getOptimizationSuggestions(resume, targetRole) {
    try {
        const response = await apiRequest('/resume/optimize', {
            method: 'POST',
            body: JSON.stringify({
                resume_text: resume,
                target_role: targetRole
            })
        });
        
        if (response.success) {
            displaySuggestions(response.suggestions);
        }
    } catch (error) {
        console.error('Error getting suggestions:', error);
    }
}

/**
 * Display optimization suggestions
 */
function displaySuggestions(suggestions) {
    const suggestionsCard = document.getElementById('suggestionsCard');
    const suggestionsContent = document.getElementById('suggestionsContent');
    
    if (!suggestionsCard || !suggestionsContent) return;
    
    let html = '<div class="suggestions">';
    
    // Keywords
    if (suggestions.keywords && suggestions.keywords.length > 0) {
        html += `
            <div class="mb-3">
                <h6><i class="fas fa-tag"></i> Missing Keywords</h6>
                <div class="keywords-list">
                    ${suggestions.keywords.map(kw => `<span class="badge bg-info">${escapeHtml(kw)}</span>`).join(' ')}
                </div>
            </div>
        `;
    }
    
    // Action Verbs
    if (suggestions.action_verbs && suggestions.action_verbs.length > 0) {
        html += `
            <div class="mb-3">
                <h6><i class="fas fa-pen-fancy"></i> Suggested Action Verbs</h6>
                <div class="action-verbs-list">
                    ${suggestions.action_verbs.map(verb => `<span class="badge bg-success">${escapeHtml(verb)}</span>`).join(' ')}
                </div>
            </div>
        `;
    }
    
    // Improvements
    if (suggestions.improvements && suggestions.improvements.length > 0) {
        html += `
            <div class="mb-3">
                <h6><i class="fas fa-lightbulb"></i> Improvement Tips</h6>
                <ul class="list-unstyled">
                    ${suggestions.improvements.map(imp => `<li><i class="fas fa-check text-success"></i> ${escapeHtml(imp)}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    html += '</div>';
    
    suggestionsContent.innerHTML = html;
    suggestionsCard.style.display = 'block';
}

/**
 * Download resume as text file
 */
function downloadResume() {
    const resumeContent = document.getElementById('resumeContent').innerText;
    const name = document.getElementById('name').value || 'resume';
    const filename = `${name.replace(/\s+/g, '_')}_resume.txt`;
    
    downloadAsFile(resumeContent, filename, 'text/plain');
    showAlert('Resume downloaded successfully!', 'success', 2000);
}

/**
 * Copy resume to clipboard
 */
function copyResume() {
    const resumeContent = document.getElementById('resumeContent').innerText;
    copyToClipboard(resumeContent);
}
