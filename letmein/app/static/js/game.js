let currentLevel = 1;
let sessionId = generateSessionId();
let levelsCompleted = 0;

function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9) + Date.now();
}

function saveGameState() {
    const gameState = {
        currentLevel: currentLevel,
        levelsCompleted: levelsCompleted,
        sessionId: sessionId
    };
    localStorage.setItem('letmeinGameState', JSON.stringify(gameState));
}

function loadGameState() {
    const saved = localStorage.getItem('letmeinGameState');
    if (saved) {
        try {
            const gameState = JSON.parse(saved);
            currentLevel = gameState.currentLevel || 1;
            levelsCompleted = gameState.levelsCompleted || 0;
            sessionId = gameState.sessionId || generateSessionId();
            
            // Update UI
            document.getElementById('current-level').textContent = currentLevel;
            document.getElementById('levels-completed').textContent = levelsCompleted;
            updateLevelButtons();
            
            // Set active level button
            document.querySelectorAll('.level-btn').forEach((btn, index) => {
                btn.classList.remove('active');
                if (index + 1 === currentLevel) {
                    btn.classList.add('active');
                }
            });
            
            return true;
        } catch (error) {
            console.error('Error loading game state:', error);
        }
    }
    return false;
}

function newGame() {
    if (confirm('Are you sure you want to start a new game? This will reset all progress.')) {
        localStorage.removeItem('letmeinGameState');
        currentLevel = 1;
        levelsCompleted = 0;
        sessionId = generateSessionId();
        
        // Update UI
        document.getElementById('current-level').textContent = currentLevel;
        document.getElementById('levels-completed').textContent = levelsCompleted;
        updateLevelButtons();
        
        // Reset to level 1
        document.querySelectorAll('.level-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelector('.level-btn').classList.add('active');
        
        // Clear chat and show welcome message
        selectLevel(1);
    }
}

async function selectLevel(level, event = null) {
    // Only allow selecting levels that are unlocked
    if (level > levelsCompleted + 1) {
        alert(`Complete Level ${levelsCompleted + 1} first!`);
        return;
    }
    
    currentLevel = level;
    document.getElementById('current-level').textContent = level;
    saveGameState();
    
    // Update active button
    document.querySelectorAll('.level-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    } else {
        // Find and activate the correct button
        const levelButtons = document.querySelectorAll('.level-btn');
        if (levelButtons[level - 1]) {
            levelButtons[level - 1].classList.add('active');
        }
    }
    
    // Clear chat and get welcome message
    const chatArea = document.getElementById('chat-area');
    chatArea.innerHTML = `
        <div class="message loading">
            🔄 Loading Level ${level}...
        </div>
    `;
    
    try {
        const response = await fetch(`/api/game/welcome/${level}`);
        const data = await response.json();
        
        if (data.success) {
            chatArea.innerHTML = `
                <div class="message ai-message">
                    <strong>🤖 Level ${level} AI:</strong><br>
                    ${data.welcome_message}
                </div>
            `;
        } else {
            chatArea.innerHTML = `
                <div class="message">
                    <strong>Level ${level} started!</strong><br>
                    Chat with the AI to try to get the password, then submit it below.
                </div>
            `;
        }
    } catch (error) {
        console.error('Error getting welcome message:', error);
        chatArea.innerHTML = `
            <div class="message">
                <strong>Level ${level} started!</strong><br>
                Chat with the AI to try to get the password, then submit it below.
            </div>
        `;
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatArea = document.getElementById('chat-area');
    
    const message = messageInput.value.trim();
    if (!message) {
        alert('Please enter a message');
        return;
    }
    
    // Disable send button
    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending...';
    
    // Add user message to chat
    addMessageToChat('user', message);
    messageInput.value = '';
    
    try {
        const response = await fetch('/api/game/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                level: currentLevel,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Add AI response to chat
            addMessageToChat('ai', data.ai_response);
        } else {
            addMessageToChat('error', 'Error: ' + (data.ai_response || 'Unknown error'));
        }
        
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('error', 'Connection error. Please check if the server is running.');
    }
    
    // Re-enable send button
    sendBtn.disabled = false;
    sendBtn.textContent = 'Send Message';
}

async function submitPassword() {
    const passwordInput = document.getElementById('password-input');
    const submitBtn = document.getElementById('submit-btn');
    
    const password = passwordInput.value.trim();
    if (!password) {
        alert('Please enter a password');
        return;
    }
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Checking...';
    
    try {
        const response = await fetch('/api/game/password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                level: currentLevel,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.correct) {
                addMessageToChat('success', `🎉 SUCCESS! Password "${password}" is correct!`);
                levelsCompleted = Math.max(levelsCompleted, currentLevel);
                document.getElementById('levels-completed').textContent = levelsCompleted;
                saveGameState();
                
                // Clear password input
                passwordInput.value = '';
                
                // Enable next level button
                updateLevelButtons();
                
                if (currentLevel < 4) {
                    // Auto-advance to next level after 2 seconds
                    addMessageToChat('success', `🚀 Advancing to Level ${currentLevel + 1} in 2 seconds...`);
                    setTimeout(() => {
                        const nextLevelBtn = document.querySelectorAll('.level-btn')[currentLevel]; // currentLevel is 0-indexed for next level
                        if (nextLevelBtn) {
                            nextLevelBtn.click();
                        }
                    }, 2000);
                } else {
                    addMessageToChat('success', '🏆 GAME COMPLETE! You are a master social engineer!');
                }
            } else {
                addMessageToChat('error', `❌ Wrong password: "${password}". Keep trying!`);
                passwordInput.value = '';
            }
        } else {
            addMessageToChat('error', 'Error checking password: ' + (data.message || 'Unknown error'));
        }
        
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('error', 'Connection error. Please check if the server is running.');
    }
    
    // Re-enable submit button
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit Password';
}

function updateLevelButtons() {
    const levelButtons = document.querySelectorAll('.level-btn');
    levelButtons.forEach((btn, index) => {
        const level = index + 1;
        if (level <= levelsCompleted + 1) {
            btn.disabled = false;
            btn.style.opacity = '1';
        } else {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        }
    });
}

function addMessageToChat(type, content) {
    const chatArea = document.getElementById('chat-area');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const prefix = type === 'user' ? '👤 You:' : 
                  type === 'ai' ? '🤖 AI:' : 
                  type === 'success' ? '✅' : 
                  type === 'error' ? '❌' : '';
    
    messageDiv.innerHTML = `<strong>${prefix}</strong><br>${content}`;
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

// Check connection status
async function checkConnection() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        document.getElementById('connection-status').textContent = 
            data.ollama_connected ? '✅ Connected' : '❌ Disconnected';
    } catch (error) {
        document.getElementById('connection-status').textContent = '❌ Error';
    }
}

// Initialize the game
function initializeGame() {
    // Load saved game state
    const hasState = loadGameState();
    
    // Enter key to send message
    document.getElementById('message-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Enter key to submit password
    document.getElementById('password-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitPassword();
        }
    });

    // Initialize level buttons
    updateLevelButtons();

    // If no saved state, start with level 1 welcome message
    if (!hasState) {
        selectLevel(1);
    } else {
        // Load welcome message for current level
        selectLevel(currentLevel);
    }

    // Check connection initially and periodically
    checkConnection();
    setInterval(checkConnection, 30000); // Check every 30 seconds
}

// Start the game when page loads
document.addEventListener('DOMContentLoaded', initializeGame);