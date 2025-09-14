const express = require('express');
const path = require('path');
const compression = require('compression');
const helmet = require('helmet');
const cors = require('cors');
require('dotenv').config();
const { init: initDatabase } = require('./src/utils/database');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
            scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
            fontSrc: ["'self'", "https://fonts.gstatic.com"],
            imgSrc: ["'self'", "data:", "https:"],
        },
    },
}));

// Middleware
app.use(cors());
app.use(compression());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// View engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Initialize local database
initDatabase().then(() => {
    console.log('✅ Database ready');
}).catch(err => {
    console.error('❌ Database initialization error:', err);
});

// Routes
app.get('/', (req, res) => {
    res.render('index', {
        title: 'Stat4Ballers - Football Statistics',
        leagues: [
            { id: 'ligue1', name: 'Ligue 1', country: 'France' },
            { id: 'premierleague', name: 'Premier League', country: 'England' },
            { id: 'liga', name: 'La Liga', country: 'Spain' },
            { id: 'seriea', name: 'Serie A', country: 'Italy' },
            { id: 'bundesliga', name: 'Bundesliga', country: 'Germany' }
        ]
    });
});

// API Routes
app.use('/api/leagues', require('./src/routes/leagues'));
app.use('/api/teams', require('./src/routes/teams'));
app.use('/api/players', require('./src/routes/players'));
app.use('/api/search', require('./src/routes/search'));

// League pages
app.get('/league/:leagueId', (req, res) => {
    res.render('league', { 
        leagueId: req.params.leagueId,
        title: `${req.params.leagueId} - Stat4Ballers`
    });
});

// Team pages - using team slug instead of ID
app.get('/team/:teamSlug', (req, res) => {
    res.render('team', { 
        teamSlug: req.params.teamSlug,
        title: 'Team Stats - Stat4Ballers'
    });
});

// Player pages
app.get('/player/:playerId', (req, res) => {
    res.render('player', { 
        playerId: req.params.playerId,
        title: 'Player Stats - Stat4Ballers'
    });
});

// Comparison page
app.get('/compare', (req, res) => {
    res.render('compare', { 
        title: 'Player Comparison - Stat4Ballers'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).render('404', { 
        title: 'Page Not Found - Stat4Ballers'
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).render('error', { 
        title: 'Error - Stat4Ballers',
        error: process.env.NODE_ENV === 'development' ? err : {}
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Stat4Ballers server running on http://localhost:${PORT}`);
    console.log(`📊 Environment: ${process.env.NODE_ENV}`);
    console.log(`⚡ SportMonks API configured and ready`);
});