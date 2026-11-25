/**
 * Interview Q&A functionality
 */

let currentQuestions = [];

document.addEventListener('DOMContentLoaded', () => {
    initializeInterviewQA();
});

function initializeInterviewQA() {
    // Setup event listeners if needed
}

/**
 * Generate interview questions
 */
async function generateQuestions() {
    if (!checkApiKey()) return;
    
    const role = document.getElementById('qaRole').value;
    const experience = document.getElementById('qaExperience').value;
    const domain = document.getElementById('qaDomain').value;
    const count = parseInt(document.getElementById('qaCount').value) || 5;
    
    if (!role) {
        showAlert('Please select a target role', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        const response = await apiRequest('/interview/questions', {
            method: 'POST',
            body: JSON.stringify({
                role,
                experience_level: experience,
                domain: domain || role,
                count
            })
        });
        
        if (response.success) {
            currentQuestions = response.questions || [];
            displayQuestions(currentQuestions);
            showAlert(`✓ Generated ${currentQuestions.length} questions!`, 'success', 3000);
        } else {
            showAlert('Failed to generate questions', 'danger');
        }
    } catch (error) {
        console.error('Error generating questions:', error);
        showAlert('Error generating questions. Please try again.', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Display questions as cards
 */
function displayQuestions(questions) {
    const container = document.getElementById('questionsContainer');
    const emptyState = document.getElementById('emptyQAState');
    
    if (!container) return;
    
    if (!questions || questions.length === 0) {
        container.innerHTML = '';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }
    
    let html = '<div class="row">';
    
    questions.forEach((q, index) => {
        html += `
            <div class="col-lg-12 mb-3">
                <div class="card question-card" onclick="openQuestionModal(${index})">
                    <div class="card-body">
                        <h6 class="card-subtitle text-muted mb-2">Question ${index + 1}</h6>
                        <p class="card-text">${escapeHtml(q.question || '')}</p>
                        <small class="text-muted">
                            <i class="fas fa-book"></i> Click to practice
                        </small>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    if (emptyState) emptyState.style.display = 'none';
}

/**
 * Open question modal for answering
 */
function openQuestionModal(index) {
    if (index < 0 || index >= currentQuestions.length) return;
    
    const question = currentQuestions[index];
    const modal = new bootstrap.Modal(document.getElementById('questionModal'));
    
    // Set modal content
    document.getElementById('questionModalTitle').textContent = `Question ${index + 1}`;
    document.getElementById('modalQuestionText').textContent = question.question || '';
    document.getElementById('modalIdealAnswer').textContent = question.ideal_answer || '';
    document.getElementById('userAnswer').value = '';
    
    // Hide sections initially
    document.getElementById('idealAnswerSection').style.display = 'none';
    document.getElementById('feedbackSection').style.display = 'none';
    document.getElementById('showAnswerBtn').style.display = 'inline-block';
    document.getElementById('submitAnswerBtn').style.display = 'inline-block';
    
    // Store current question index
    modal._currentQuestionIndex = index;
    
    modal.show();
}

/**
 * Show ideal answer
 */
function showIdealAnswer() {
    const section = document.getElementById('idealAnswerSection');
    section.style.display = 'block';
    document.getElementById('showAnswerBtn').disabled = true;
}

/**
 * Submit user's answer for evaluation
 */
async function submitAnswer() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('questionModal'));
    const index = modal._currentQuestionIndex;
    
    if (index < 0 || index >= currentQuestions.length) return;
    
    const question = currentQuestions[index];
    const userAnswer = document.getElementById('userAnswer').value.trim();
    
    if (!userAnswer) {
        showAlert('Please provide an answer', 'warning');
        return;
    }
    
    if (!checkApiKey()) return;
    
    try {
        showLoading();
        
        const response = await apiRequest('/interview/evaluate', {
            method: 'POST',
            body: JSON.stringify({
                question: question.question || '',
                user_answer: userAnswer,
                ideal_answer: question.ideal_answer || ''
            })
        });
        
        if (response.success && response.feedback) {
            displayFeedback(response.feedback);
            document.getElementById('submitAnswerBtn').disabled = true;
        }
    } catch (error) {
        console.error('Error evaluating answer:', error);
        showAlert('Error evaluating your answer. Please try again.', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Display feedback
 */
function displayFeedback(feedback) {
    const section = document.getElementById('feedbackSection');
    const content = document.getElementById('feedbackContent');
    
    let html = '<div>';
    
    // Score
    if (feedback.score) {
        const scoreColor = feedback.score >= 75 ? 'success' : feedback.score >= 50 ? 'warning' : 'danger';
        html += `
            <div class="alert alert-${scoreColor} mb-3">
                <h6><i class="fas fa-star"></i> Score: ${feedback.score}/100</h6>
            </div>
        `;
    }
    
    // Summary
    if (feedback.summary) {
        html += `
            <div class="mb-3">
                <h6><i class="fas fa-comment"></i> Summary</h6>
                <p>${escapeHtml(feedback.summary)}</p>
            </div>
        `;
    }
    
    // Strengths
    if (feedback.strengths && feedback.strengths.length > 0) {
        html += `
            <div class="mb-3">
                <h6><i class="fas fa-thumbs-up text-success"></i> Strengths</h6>
                <ul>
                    ${feedback.strengths.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Areas to improve
    if (feedback.improvements && feedback.improvements.length > 0) {
        html += `
            <div class="mb-3">
                <h6><i class="fas fa-lightbulb text-warning"></i> Areas to Improve</h6>
                <ul>
                    ${feedback.improvements.map(i => `<li>${escapeHtml(i)}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    html += '</div>';
    content.innerHTML = html;
    section.style.display = 'block';
}
