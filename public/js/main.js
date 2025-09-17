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
        <div class="suggestion-item" data-url="${item.url}">
            <span class="suggestion-type">${item.type}</span>
            <span class="suggestion-name">${item.name}</span>
        </div>
    `).join('');

    searchSuggestions.classList.add('active');

    // Ajouter les event listeners aux suggestions
    const items = searchSuggestions.querySelectorAll('.suggestion-item');
    items.forEach(item => {
        item.addEventListener('click', function() {
            const url = this.dataset.url;
            window.location.href = url;
        });
    });
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
        // Créer le conteneur de suggestions pour chaque input
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.className = 'player-suggestions';
        suggestionsContainer.style.display = 'none';
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(suggestionsContainer);

        input.addEventListener('input', (e) => {
            clearTimeout(state.searchTimeout);
            const query = e.target.value.trim();

            if (query.length < 2) {
                hidePlayerSuggestions(e.target);
                e.target.dataset.playerId = '';
                updateCompareButton();
                return;
            }

            state.searchTimeout = setTimeout(() => {
                fetchPlayerSuggestions(query, e.target);
            }, 300);
        });

        // Fermer les suggestions lors du clic en dehors
        input.addEventListener('blur', (e) => {
            setTimeout(() => hidePlayerSuggestions(e.target), 200);
        });

        // Afficher les suggestions au focus si présentes
        input.addEventListener('focus', (e) => {
            const suggestions = e.target.parentElement.querySelector('.player-suggestions');
            if (suggestions && suggestions.innerHTML) {
                suggestions.style.display = 'block';
            }
        });
    });

    if (compareBtn) {
        compareBtn.addEventListener('click', comparePlayersI);
    }
}

async function fetchPlayerSuggestions(query, inputElement) {
    try {
        const response = await fetch(`/api/search/players?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.success && data.data.length > 0) {
            displayPlayerSuggestions(data.data, inputElement);
        } else {
            hidePlayerSuggestions(inputElement);
        }
    } catch (error) {
        console.error('Error fetching player suggestions:', error);
    }
}

function displayPlayerSuggestions(players, inputElement) {
    const suggestionsDiv = inputElement.parentElement.querySelector('.player-suggestions');

    if (!suggestionsDiv) return;

    suggestionsDiv.innerHTML = players.map(player => `
        <div class="suggestion-item"
             data-player-id="${player.id}"
             data-player-name="${player.name.replace(/"/g, '&quot;')}"
             data-input-index="${inputElement.dataset.playerIndex}">
            <span class="suggestion-name">${player.name}</span>
            ${player.team ? `<span class="suggestion-team">${player.team}</span>` : ''}
        </div>
    `).join('');

    suggestionsDiv.style.display = 'block';

    // Ajouter les event listeners
    const items = suggestionsDiv.querySelectorAll('.suggestion-item');
    items.forEach(item => {
        item.addEventListener('mousedown', function(e) {
            e.preventDefault(); // Empêcher le blur de l'input
            const playerId = this.dataset.playerId;
            const playerName = this.dataset.playerName;
            const inputIndex = this.dataset.inputIndex;
            selectPlayer(playerId, playerName, inputIndex);
        });
    });
}

function hidePlayerSuggestions(inputElement) {
    const suggestions = inputElement.parentElement.querySelector('.player-suggestions');
    if (suggestions) {
        suggestions.style.display = 'none';
    }
}

function selectPlayer(playerId, playerName, inputIndex) {
    const input = document.querySelector(`[data-player-index="${inputIndex}"]`);
    input.value = playerName;
    input.dataset.playerId = playerId;

    hidePlayerSuggestions(input);
    updateCompareButton();
}

// Export pour compatibilité
window.selectPlayer = selectPlayer;

function updateCompareButton() {
    const selectedCount = Array.from(playerInputs).filter(input => input.dataset.playerId).length;

    if (compareBtn) {
        compareBtn.disabled = selectedCount < 2;
        compareBtn.textContent = selectedCount >= 2 ?
            `Compare ${selectedCount} Players` : 'Select at least 2 players';
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