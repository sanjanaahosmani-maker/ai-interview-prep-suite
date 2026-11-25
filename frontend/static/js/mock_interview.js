/**
 * Mock Interview functionality
 */

let mockSessionId = null;
let currentQuestionIndex = 0;
let totalQuestions = 0;
let interviewStartTime = null;
let sessionResponses = [];
let sessionFeedback = [];

document.addEventListener('DOMContentLoaded', () => {
    initializeMockInterview();
});

function initializeMockInterview() {
    // Setup event listeners if needed
}

/**
 * Start mock interview
 */
async function startMockInterview() {
    if (!checkApiKey()) return;
    
    const role = document.getElementById('mockRole').value;
    const experience = document.getElementById('mockExperience').value;
    const domain = document.getElementById('mockDomain').value;
    const numQuestions = parseInt(document.getElementById('mockQuestionCount').value) || 5;
    
    if (!role) {
        showAlert('Please select a target role', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        const response = await apiRequest('/mock-interview/start', {
            method: 'POST',
            body: JSON.stringify({
                role,
                experience_level: experience,
                domain: domain || role,
                num_questions: numQuestions
            })
        });
        
        if (response.success) {
            mockSessionId = response.session_id;
            currentQuestionIndex = 0;
            totalQuestions = response.total_questions;
            interviewStartTime = new Date();
            sessionResponses = [];
            sessionFeedback = [];
            
            // Display interview panel
            document.getElementById('setupPanel').style.display = 'none';
            document.getElementById('interviewPanel').style.display = 'block';
            document.getElementById('resultsPanel').style.display = 'none';
            
            // Display first question
            displayCurrentQuestion(response.current_question);
            showAlert(`✓ Mock interview started! ${totalQuestions} questions.`, 'success', 2000);
        } else {
            showAlert('Failed to start mock interview', 'danger');
        }
    } catch (error) {
        console.error('Error starting mock interview:', error);
        showAlert('Error starting mock interview. Please try again.', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Display current question
 */
function displayCurrentQuestion(question) {
    if (!question) {
        showAlert('No question available', 'danger');
        return;
    }
    
    // Update progress
    document.getElementById('currentQuestionNum').textContent = currentQuestionIndex + 1;
    document.getElementById('totalQuestionsNum').textContent = totalQuestions;
    
    const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = progress + '%';
    progressBar.textContent = Math.round(progress) + '%';
    
    // Display question
    document.getElementById('questionDisplay').textContent = question.question || '';
    document.getElementById('answerInput').value = '';
    
    // Reset UI
    document.getElementById('idealAnswerSection').style.display = 'none';
    document.getElementById('showAnswerBtn').style.display = 'inline-block';
    document.getElementById('showAnswerBtn').disabled = false;
    document.getElementById('submitAnswerBtn').disabled = false;
    
    // Store current question for feedback later
    window.currentQuestion = question;
}

/**
 * Show ideal answer for mock interview
 */
function showIdealAnswerForMock() {
    if (!window.currentQuestion) return;
    
    const section = document.getElementById('idealAnswerSection');
    const display = document.getElementById('idealAnswerDisplay');
    
    display.textContent = window.currentQuestion.ideal_answer || '';
    section.style.display = 'block';
    
    document.getElementById('showAnswerBtn').disabled = true;
}

/**
 * Submit mock interview answer and get next question
 */
async function submitMockAnswer() {
    if (!mockSessionId) {
        showAlert('Interview session not found', 'danger');
        return;
    }
    
    const userAnswer = document.getElementById('answerInput').value.trim();
    
    if (!userAnswer) {
        showAlert('Please provide an answer', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        // Store response
        sessionResponses.push(userAnswer);
        
        // Get next question
        const response = await apiRequest(`/mock-interview/${mockSessionId}/next`, {
            method: 'POST',
            body: JSON.stringify({
                response: userAnswer
            })
        });
        
        if (response.success) {
            // Store feedback
            if (response.previous_feedback) {
                sessionFeedback.push(response.previous_feedback);
            }
            
            if (response.completed) {
                // Interview completed
                await completeInterview();
            } else {
                // Show next question
                currentQuestionIndex++;
                displayCurrentQuestion(response.current_question);
                showAlert(`✓ Answer submitted! Moving to question ${response.current_question_index + 1}/${totalQuestions}`, 'info', 2000);
            }
        } else {
            showAlert('Failed to get next question', 'danger');
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
        showAlert('Error submitting answer. Please try again.', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Complete mock interview and show results
 */
async function completeInterview() {
    try {
        showLoading();
        
        const response = await apiRequest(`/mock-interview/${mockSessionId}/complete`, {
            method: 'POST',
            body: JSON.stringify({})
        });
        
        if (response.success) {
            displayResults(response);
        } else {
            showAlert('Failed to complete interview', 'danger');
        }
    } catch (error) {
        console.error('Error completing interview:', error);
        showAlert('Error completing interview', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Display interview results
 */
function displayResults(results) {
    // Hide interview panel, show results panel
    document.getElementById('interviewPanel').style.display = 'none';
    document.getElementById('resultsPanel').style.display = 'block';
    
    // Calculate duration
    const duration = Math.round((new Date() - interviewStartTime) / 60000);
    
    // Update results display
    document.getElementById('resultTotal').textContent = results.total_questions;
    document.getElementById('resultScore').textContent = Math.round(results.average_score) + '%';
    document.getElementById('resultDuration').textContent = duration + ' min';
    
    // Display feedback
    displayFeedbackSummary(results.feedback);
    
    showAlert('✓ Interview completed! Great effort!', 'success', 3000);
}

/**
 * Display feedback summary
 */
function displayFeedbackSummary(feedback) {
    const container = document.getElementById('feedbackSummary');
    
    if (!feedback || feedback.length === 0) {
        container.innerHTML = '<p>No feedback available</p>';
        return;
    }
    
    let html = '<div class="feedback-list">';
    
    feedback.forEach((item, index) => {
        const scoreColor = item.score >= 75 ? 'success' : item.score >= 50 ? 'warning' : 'danger';
        
        html += `
            <div class="card mb-2">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title">Question ${index + 1}</h6>
                        <span class="badge bg-${scoreColor}">${item.score || 0}/100</span>
                    </div>
                    ${item.summary ? `<p class="card-text small text-muted">${escapeHtml(item.summary)}</p>` : ''}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

/**
 * Download interview report
 */
function downloadResults() {
    const reportContent = `
AI Interview Prep Suite - Interview Report
==========================================

Interview Date: ${new Date().toLocaleString()}
Duration: ${Math.round((new Date() - interviewStartTime) / 60000)} minutes
Session ID: ${mockSessionId}

Performance Summary:
- Total Questions: ${totalQuestions}
- Questions Answered: ${sessionResponses.length}
- Average Score: ${Math.round(sessionFeedback.reduce((a, b) => a + (b.score || 0), 0) / sessionFeedback.length)}%

Questions and Responses:
${sessionResponses.map((resp, idx) => `
Question ${idx + 1}:
${resp}
---
`).join('\n')}
    `;
    
    downloadAsFile(reportContent, `interview_report_${Date.now()}.txt`, 'text/plain');
    showAlert('Report downloaded!', 'success', 2000);
}

/**
 * Return to setup for new interview
 */
function returnToSetup() {
    // Reset state
    mockSessionId = null;
    currentQuestionIndex = 0;
    totalQuestions = 0;
    interviewStartTime = null;
    sessionResponses = [];
    sessionFeedback = [];
    
    // Show setup panel
    document.getElementById('setupPanel').style.display = 'block';
    document.getElementById('interviewPanel').style.display = 'none';
    document.getElementById('resultsPanel').style.display = 'none';
    
    // Reset form
    document.getElementById('mockRole').value = '';
    document.getElementById('mockExperience').value = 'mid';
    document.getElementById('mockDomain').value = '';
    document.getElementById('mockQuestionCount').value = '5';
}
