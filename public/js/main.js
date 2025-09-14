// Global state
const state = {
    selectedPlayers: [],
    searchTimeout: null,
    currentLanguage: 'en'
};

// DOM Elements
const globalSearch = document.getElementById('global-search');
const searchSuggestions = document.getElementById('search-suggestions');
const compareBtn = document.getElementById('compare-btn');
const playerInputs = document.querySelectorAll('.player-input');
const langBtns = document.querySelectorAll('.lang-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeSearch();
    initializePlayerComparison();
    initializeLanguageSelector();
});

// Search functionality
function initializeSearch() {
    if (!globalSearch) return;
    
    globalSearch.addEventListener('input', (e) => {
        clearTimeout(state.searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            hideSuggestions();
            return;
        }
        
        state.searchTimeout = setTimeout(() => {
            fetchSuggestions(query);
        }, 300);
    });
    
    globalSearch.addEventListener('focus', () => {
        if (globalSearch.value.length >= 2) {
            searchSuggestions.classList.add('active');
        }
    });
    
    document.addEventListener('click', (e) => {
        if (!globalSearch.contains(e.target) && !searchSuggestions.contains(e.target)) {
            hideSuggestions();
        }
    });
}

async function fetchSuggestions(query) {
    try {
        const response = await fetch(`/api/search/suggestions?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            displaySuggestions(data.data);
        } else {
            hideSuggestions();
        }
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

function displaySuggestions(suggestions) {
    searchSuggestions.innerHTML = suggestions.map(item => `
        <div class="suggestion-item" onclick="navigateTo('${item.url}')">
            <span class="suggestion-type">${item.type}</span>
            <span class="suggestion-name">${item.name}</span>
        </div>
    `).join('');
    
    searchSuggestions.classList.add('active');
}

function hideSuggestions() {
    searchSuggestions.classList.remove('active');
    searchSuggestions.innerHTML = '';
}

window.navigateTo = function(url) {
    window.location.href = url;
}

// Player comparison functionality
function initializePlayerComparison() {
    if (!playerInputs.length) return;
    
    playerInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            const index = parseInt(e.target.dataset.playerIndex) - 1;
            clearTimeout(state.searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length < 2) {
                hidePlayerSuggestions(e.target);
                return;
            }
            
            state.searchTimeout = setTimeout(() => {
                fetchPlayerSuggestions(query, e.target);
            }, 300);
        });
    });
    
    if (compareBtn) {
        compareBtn.addEventListener('click', comparePlayersI);
    }
}

async function fetchPlayerSuggestions(query, inputElement) {
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&type=player&limit=5`);
        const data = await response.json();
        
        if (data.success && data.data.players.length > 0) {
            displayPlayerSuggestions(data.data.players, inputElement);
        }
    } catch (error) {
        console.error('Error fetching player suggestions:', error);
    }
}

function displayPlayerSuggestions(players, inputElement) {
    // Remove existing suggestions
    const existingSuggestions = inputElement.parentElement.querySelector('.player-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }
    
    // Create new suggestions dropdown
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'player-suggestions search-suggestions active';
    suggestionsDiv.style.position = 'absolute';
    suggestionsDiv.style.top = '100%';
    suggestionsDiv.style.left = '0';
    suggestionsDiv.style.right = '0';
    suggestionsDiv.style.zIndex = '1000';
    
    suggestionsDiv.innerHTML = players.map(player => `
        <div class="suggestion-item" onclick="selectPlayer('${player.sportmonksId}', '${player.name}', '${inputElement.dataset.playerIndex}')">
            <span class="suggestion-name">${player.name}</span>
            <span class="suggestion-team">${player.team ? player.team.name : ''}</span>
        </div>
    `).join('');
    
    inputElement.parentElement.style.position = 'relative';
    inputElement.parentElement.appendChild(suggestionsDiv);
}

function hidePlayerSuggestions(inputElement) {
    const suggestions = inputElement.parentElement.querySelector('.player-suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

function selectPlayer(playerId, playerName, inputIndex) {
    const input = document.querySelector(`[data-player-index="${inputIndex}"]`);
    input.value = playerName;
    input.dataset.playerId = playerId;
    
    hidePlayerSuggestions(input);
    updateCompareButton();
}

function updateCompareButton() {
    const selectedCount = Array.from(playerInputs).filter(input => input.dataset.playerId).length;
    
    if (compareBtn) {
        compareBtn.disabled = selectedCount < 2;
    }
}

function comparePlayersI() {
    const playerIds = Array.from(playerInputs)
        .filter(input => input.dataset.playerId)
        .map(input => input.dataset.playerId);
    
    if (playerIds.length >= 2) {
        const params = new URLSearchParams();
        playerIds.forEach(id => params.append('player', id));
        window.location.href = `/compare?${params.toString()}`;
    }
}

// Language selector
function initializeLanguageSelector() {
    langBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const lang = e.target.dataset.lang;
            changeLanguage(lang);
        });
    });
}

function changeLanguage(lang) {
    // Update active button
    langBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    
    // Store preference
    localStorage.setItem('preferredLanguage', lang);
    state.currentLanguage = lang;
    
    // In a real implementation, this would trigger i18n translation
    console.log(`Language changed to: ${lang}`);
    
    // Future: Reload content with new language
    // loadTranslations(lang);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// API helpers
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`/api${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Export for use in other scripts
window.stat4ballers = {
    apiCall,
    state,
    navigateTo
};