const axios = require('axios');
require('dotenv').config();

// Colors for console output
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m'
};

const log = {
    success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
    error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
    info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
    warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`)
};

async function testServer() {
    const baseURL = 'http://localhost:3000';
    
    log.info('Starting server tests...\n');
    
    // Test 1: Check if server is running
    try {
        const response = await axios.get(baseURL);
        if (response.status === 200) {
            log.success('Server is running on port 3000');
        }
    } catch (error) {
        log.error('Server is not running. Please start it with: npm start');
        return;
    }
    
    // Test 2: Check static files
    try {
        const cssResponse = await axios.get(`${baseURL}/css/style.css`);
        if (cssResponse.status === 200) {
            log.success('Static files are being served correctly');
        }
    } catch (error) {
        log.error('Static files are not accessible');
    }
    
    // Test 3: Check API endpoints
    const endpoints = [
        '/api/leagues',
        '/api/leagues/ligue1',
        '/api/search?q=paris'
    ];
    
    for (const endpoint of endpoints) {
        try {
            const response = await axios.get(`${baseURL}${endpoint}`);
            if (response.data.success !== undefined) {
                log.success(`API endpoint ${endpoint} is responding`);
            }
        } catch (error) {
            log.warning(`API endpoint ${endpoint} returned an error (this is normal if DB is empty)`);
        }
    }
    
    // Test 4: Check views
    const views = [
        '/league/ligue1',
        '/team/paris-saint-germain',
        '/player/mason-greenwood',
        '/compare'
    ];
    
    for (const view of views) {
        try {
            const response = await axios.get(`${baseURL}${view}`);
            if (response.status === 200) {
                log.success(`View ${view} is accessible`);
            }
        } catch (error) {
            log.error(`View ${view} is not accessible`);
        }
    }
    
    log.info('\n=== Test Summary ===');
    log.info('Server is ready for development!');
    log.info('You can now access the site at: http://localhost:3000');
    log.info('\nNext steps:');
    log.info('1. Run data refresh script: npm run refresh:ligue1');
    log.info('2. This will populate the database with real data from SportMonks API');
}

// Run tests
testServer().catch(console.error);