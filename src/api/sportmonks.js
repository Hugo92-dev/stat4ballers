const axios = require('axios');
require('dotenv').config();

class SportMonksAPI {
    constructor() {
        this.baseURL = process.env.SPORTMONKS_BASE_URL;
        this.apiKey = process.env.SPORTMONKS_API_KEY;
        this.requestCount = 0;
        this.requestQueue = [];
        this.rateLimitReset = null;
        this.maxRequestsPerHour = 3000;
        
        this.axiosInstance = axios.create({
            baseURL: this.baseURL,
            headers: {
                'Authorization': this.apiKey,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout: 30000
        });

        this.initializeRateLimitTracking();
    }

    initializeRateLimitTracking() {
        setInterval(() => {
            this.requestCount = 0;
            console.log('Request count reset. Ready for new requests.');
        }, 3600000); // Reset every hour
    }

    async makeRequest(endpoint, params = {}) {
        if (this.requestCount >= this.maxRequestsPerHour) {
            const waitTime = this.getWaitTime();
            console.log(`Rate limit reached. Waiting ${waitTime} minutes until next hour...`);
            await this.delay(waitTime * 60000);
            this.requestCount = 0;
        }

        try {
            this.requestCount++;
            console.log(`Making request ${this.requestCount}/${this.maxRequestsPerHour}: ${endpoint}`);
            
            const response = await this.axiosInstance.get(endpoint, { params });
            
            // Check rate limit headers
            if (response.headers['x-ratelimit-remaining']) {
                const remaining = parseInt(response.headers['x-ratelimit-remaining']);
                if (remaining < 100) {
                    console.warn(`Warning: Only ${remaining} requests remaining this hour`);
                }
            }
            
            return response.data;
        } catch (error) {
            if (error.response) {
                if (error.response.status === 429) {
                    console.error('Rate limit exceeded. Waiting for next hour...');
                    const waitTime = this.getWaitTime();
                    await this.delay(waitTime * 60000);
                    return this.makeRequest(endpoint, params);
                }
                console.error(`API Error: ${error.response.status} - ${error.response.data.message || error.response.statusText}`);
            } else {
                console.error('Network error:', error.message);
            }
            throw error;
        }
    }

    getWaitTime() {
        const now = new Date();
        const nextHour = new Date(now);
        nextHour.setHours(now.getHours() + 1, 1, 0, 0);
        return Math.ceil((nextHour - now) / 60000);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // League endpoints
    async getLeague(leagueId) {
        return this.makeRequest(`/leagues/${leagueId}`, {
            include: 'country'
        });
    }

    async getLeagueSeasons(leagueId) {
        return this.makeRequest(`/leagues/${leagueId}`, {
            include: 'seasons'
        });
    }

    // Team endpoints
    async getTeam(teamId) {
        return this.makeRequest(`/teams/${teamId}`);
    }

    async getTeamSquad(teamId, seasonId) {
        return this.makeRequest(`/squads/seasons/${seasonId}/teams/${teamId}`);
    }

    async getTeamStatistics(teamId, seasonId) {
        return this.makeRequest(`/teams/${teamId}/statistics`, {
            filters: `seasonId:${seasonId}`,
            include: 'details'
        });
    }

    // Player endpoints
    async getPlayer(playerId) {
        return this.makeRequest(`/players/${playerId}`, {
            include: 'team,position,nationality'
        });
    }

    async getPlayerStatistics(playerId, seasonId) {
        return this.makeRequest(`/players/${playerId}/statistics`, {
            filters: `seasonId:${seasonId}`,
            include: 'details'
        });
    }

    // Season endpoints
    async getSeasonTeams(seasonId) {
        return this.makeRequest(`/seasons/${seasonId}`, {
            include: 'teams'
        });
    }

    async getSeasonStandings(seasonId) {
        return this.makeRequest(`/standings/seasons/${seasonId}`, {
            include: 'team,details'
        });
    }

    // Batch operations for efficiency
    async getMultipleTeams(teamIds) {
        const teams = [];
        for (const teamId of teamIds) {
            try {
                const team = await this.getTeam(teamId);
                teams.push(team);
                await this.delay(100); // Small delay between requests
            } catch (error) {
                console.error(`Failed to fetch team ${teamId}:`, error.message);
            }
        }
        return teams;
    }

    async getSeasonData(leagueId, seasonId) {
        try {
            const data = {
                league: await this.getLeague(leagueId),
                teams: await this.getSeasonTeams(seasonId),
                standings: await this.getSeasonStandings(seasonId)
            };
            return data;
        } catch (error) {
            console.error(`Failed to fetch season data for league ${leagueId}, season ${seasonId}:`, error.message);
            throw error;
        }
    }

    // Statistics mapping for our radar charts
    mapPlayerStatistics(stats) {
        const statMapping = {
            // General statistics
            rating: stats.find(s => s.type_id === 118)?.data?.value || 0,
            appearances: stats.find(s => s.type_id === 321)?.data?.value || 0,
            minutesPlayed: stats.find(s => s.type_id === 119)?.data?.value || 0,
            captain: stats.find(s => s.type_id === 40)?.data?.value || 0,
            goals: stats.find(s => s.type_id === 52)?.data?.value || 0,
            assists: stats.find(s => s.type_id === 79)?.data?.value || 0,
            injuries: stats.find(s => s.type_id === 87)?.data?.value || 0,
            redCards: stats.find(s => s.type_id === 83)?.data?.value || 0,
            
            // Offensive creativity
            shotsTotal: stats.find(s => s.type_id === 42)?.data?.value || 0,
            shotsOnTarget: stats.find(s => s.type_id === 86)?.data?.value || 0,
            penalties: stats.find(s => s.type_id === 47)?.data?.value || 0,
            hitWoodwork: stats.find(s => s.type_id === 64)?.data?.value || 0,
            keyPasses: stats.find(s => s.type_id === 117)?.data?.value || 0,
            bigChancesCreated: stats.find(s => s.type_id === 580)?.data?.value || 0,
            expectedGoals: stats.find(s => s.type_id === 5304)?.data?.value || 0,
            accurateThroughBalls: stats.find(s => s.type_id === 125)?.data?.value || 0,
            accurateLongBalls: stats.find(s => s.type_id === 123)?.data?.value || 0,
            accurateCrosses: stats.find(s => s.type_id === 99)?.data?.value || 0,
            successfulDribbles: stats.find(s => s.type_id === 109)?.data?.value || 0,
            
            // Defensive commitment
            yellowCards: stats.find(s => s.type_id === 84)?.data?.value || 0,
            tackles: stats.find(s => s.type_id === 78)?.data?.value || 0,
            ownGoals: stats.find(s => s.type_id === 324)?.data?.value || 0,
            interceptions: stats.find(s => s.type_id === 100)?.data?.value || 0,
            duelsWon: stats.find(s => s.type_id === 106)?.data?.value || 0,
            aerialsWon: stats.find(s => s.type_id === 107)?.data?.value || 0,
            dispossessed: stats.find(s => s.type_id === 94)?.data?.value || 0,
            dribbledPast: stats.find(s => s.type_id === 110)?.data?.value || 0,
            fouls: stats.find(s => s.type_id === 56)?.data?.value || 0,
            foulsDrawn: stats.find(s => s.type_id === 96)?.data?.value || 0,
            errorLeadToGoal: stats.find(s => s.type_id === 571)?.data?.value || 0,
            
            // Goalkeeper specific
            saves: stats.find(s => s.type_id === 57)?.data?.value || 0,
            savesInsideBox: stats.find(s => s.type_id === 104)?.data?.value || 0,
            goalsConceded: stats.find(s => s.type_id === 88)?.data?.value || 0,
            cleanSheets: stats.find(s => s.type_id === 194)?.data?.value || 0
        };
        
        return statMapping;
    }
}

module.exports = new SportMonksAPI();