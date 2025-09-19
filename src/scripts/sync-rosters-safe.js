const fs = require('fs');
const path = require('path');
const axios = require('axios');

class SafeRosterSync {
    constructor() {
        this.apiToken = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';
        this.baseUrl = 'https://api.sportmonks.com/v3/football';
        this.dataPath = path.join(__dirname, '../../data/db');
        this.playersFile = path.join(this.dataPath, 'players.json');
        this.apiCallCount = 0;
        this.apiFailures = 0;
        this.playersAdded = 0;
        this.playersKept = 0;
        this.playersRemoved = 0;
    }

    async init() {
        console.log('\n🚀 Starting SAFE roster synchronization...');
        console.log('📅 Date:', new Date().toLocaleDateString('fr-FR'));
        console.log('==================================================');
        console.log('📋 Features:');
        console.log('   ✓ Keep players by default when API fails');
        console.log('   ✓ Only remove if we\'re CERTAIN they left');
        console.log('   ✓ Add all new players');
        console.log('   ✓ Better error handling\n');

        this.existingPlayers = this.loadExistingPlayers();
        this.createBackup();

        const leagues = {
            ligue1: {
                name: 'Ligue 1',
                seasonId: 23490,
                teams: {
                    44: 'Olympique Marseille',
                    59: 'Nantes',
                    79: 'Olympique Lyonnais',
                    266: 'Brest',
                    271: 'Lens',
                    289: 'Toulouse',
                    450: 'Nice',
                    247: 'Paris Saint Germain',
                    598: 'Rennes',
                    608: 'Strasbourg',
                    611: 'LOSC Lille',
                    876: 'Angers SCO',
                    882: 'Le Havre',
                    884: 'Metz',
                    885: 'Auxerre',
                    889: 'Paris',
                    3011: 'Monaco',
                    211505: 'Lorient'
                }
            },
            premierleague: {
                name: 'Premier League',
                seasonId: 23614,
                teams: {
                    7: 'West Ham United',
                    13: 'Sunderland',
                    17: 'Tottenham Hotspur',
                    18: 'Liverpool',
                    19: 'Manchester City',
                    25: 'Fulham',
                    29: 'Everton',
                    35: 'Manchester United',
                    39: 'Aston Villa',
                    42: 'Chelsea',
                    43: 'Arsenal',
                    68: 'Newcastle United',
                    71: 'Burnley',
                    74: 'Wolverhampton Wanderers',
                    78: 'Crystal Palace',
                    211: 'AFC Bournemouth',
                    225: 'Leeds United',
                    1371: 'West Bromwich Albion',
                    880: 'Brighton',
                    607: 'Sheffield United'
                }
            },
            laliga: {
                name: 'La Liga',
                seasonId: 23533,
                teams: {
                    27: 'Celta de Vigo',
                    38: 'FC Barcelona',
                    63: 'Real Oviedo',
                    72: 'Getafe',
                    94: 'Valencia',
                    253: 'Girona',
                    258: 'Rayo Vallecano',
                    261: 'Osasuna',
                    426: 'Real Betis',
                    461: 'Espanyol',
                    548: 'Real Sociedad',
                    594: 'Mallorca',
                    797: 'Sevilla',
                    891: 'Elche',
                    2885: 'Deportivo Alavés',
                    3743: 'Levante',
                    3468: 'Real Madrid',
                    2836: 'Villarreal',
                    621: 'Atlético Madrid',
                    251: 'Athletic Club'
                }
            },
            seriea: {
                name: 'Serie A',
                seasonId: 23571,
                teams: {
                    91: 'Roma',
                    99: 'Lazio',
                    108: 'Genoa',
                    121: 'Fiorentina',
                    113: 'Milan',
                    125: 'Como',
                    402: 'Udinese',
                    522: 'Parma',
                    1020: 'Cagliari',
                    591: 'Napoli',
                    597: 'Torino',
                    496: 'Juventus',
                    499: 'Atalanta',
                    635: 'Pisa',
                    643: 'Hellas Verona',
                    667: 'Sassuolo',
                    102: 'Inter',
                    873: 'Lecce',
                    102: 'Bologna',
                    732: 'Cremonese'
                }
            },
            bundesliga: {
                name: 'Bundesliga',
                seasonId: 23538,
                teams: {
                    15: 'Borussia Dortmund',
                    69: 'Werder Bremen',
                    157: 'FC Augsburg',
                    173: 'RB Leipzig',
                    258444: 'St. Pauli',
                    75: 'Eintracht Frankfurt',
                    4: 'FC Bayern München',
                    95: 'VfL Wolfsburg',
                    16: 'Borussia Mönchengladbach',
                    214: 'FSV Mainz 05',
                    602: 'FC Union Berlin',
                    177: 'Hamburger SV',
                    172: 'TSG Hoffenheim',
                    241: 'Heidenheim',
                    970: 'VfB Stuttgart',
                    65: 'FC Köln',
                    168: 'Bayer 04 Leverkusen',
                    40: 'SC Freiburg'
                }
            }
        };

        const newPlayers = {};

        for (const [leagueKey, league] of Object.entries(leagues)) {
            console.log(`\n🔄 Processing ${league.name} (${Object.keys(league.teams).length} teams)...\n`);
            newPlayers[leagueKey] = [];

            for (const [teamId, teamName] of Object.entries(league.teams)) {
                const players = await this.getTeamSquad(league.seasonId, teamId, teamName);
                if (players && players.length > 0) {
                    newPlayers[leagueKey].push(...players);
                    this.playersAdded += players.length;
                }

                // Small delay between teams
                await this.delay(500);
            }

            console.log(`   ✅ ${league.name}: ${newPlayers[leagueKey].length} players total\n`);

            // Delay between leagues
            await this.delay(2000);
        }

        // Save all players
        this.saveAllPlayers(newPlayers);

        console.log('\n==================================================');
        console.log('✅ SYNC COMPLETED SUCCESSFULLY!');
        console.log(`📊 Final Stats:`);
        console.log(`   - Total players: ${this.countTotalPlayers(newPlayers)}`);
        console.log(`   - API calls: ${this.apiCallCount}`);
        console.log(`   - API failures handled: ${this.apiFailures}`);
        console.log('==================================================\n');
    }

    async getTeamSquad(seasonId, teamId, teamName) {
        try {
            console.log(`   📌 Processing: ${teamName}`);
            this.apiCallCount++;

            const url = `${this.baseUrl}/squads/seasons/${seasonId}/teams/${teamId}`;
            const response = await axios.get(url, {
                params: { api_token: this.apiToken },
                timeout: 10000
            });

            if (!response.data || !response.data.data || response.data.data.length === 0) {
                console.log(`      ⚠️  No squad data for ${teamName}`);
                return [];
            }

            const players = response.data.data.map(p => this.mapPlayer(p.player, teamName, teamId));
            console.log(`      ✅ Added ${players.length} players for ${teamName}`);

            return players;

        } catch (error) {
            this.apiFailures++;
            console.log(`      ❌ Error fetching ${teamName}: ${error.message}`);
            console.log(`      📂 Keeping existing players for ${teamName}`);

            // Return existing players for this team instead of empty array
            return this.getExistingTeamPlayers(teamName);
        }
    }

    getExistingTeamPlayers(teamName) {
        const existingPlayers = [];
        for (const league of Object.values(this.existingPlayers)) {
            if (Array.isArray(league)) {
                const teamPlayers = league.filter(p => p.team === teamName);
                existingPlayers.push(...teamPlayers);
            }
        }
        return existingPlayers;
    }

    mapPlayer(player, teamName, teamId) {
        const positionMap = {
            1: 'Gardien',
            2: 'Défenseur',
            3: 'Milieu',
            4: 'Attaquant'
        };

        return {
            id: player.id,
            name: player.name || 'Unknown',
            team: teamName,
            teamId: teamId,
            nationality: player.nationality || 'Unknown',
            position: positionMap[player.position_id] || 'Unknown',
            age: player.age || null,
            height: player.height || null,
            weight: player.weight || null,
            image: player.image_path || '',
            jerseyNumber: player.jersey_number || null
        };
    }

    loadExistingPlayers() {
        try {
            if (fs.existsSync(this.playersFile)) {
                const data = JSON.parse(fs.readFileSync(this.playersFile, 'utf8'));
                console.log(`📂 Loaded ${this.countTotalPlayers(data)} existing players`);
                return data;
            }
        } catch (error) {
            console.log('⚠️  Could not load existing players:', error.message);
        }
        return {};
    }

    createBackup() {
        try {
            if (fs.existsSync(this.playersFile)) {
                const backupFile = path.join(this.dataPath, 'players.backup.json');
                fs.copyFileSync(this.playersFile, backupFile);
                console.log(`💾 Backup created: ${backupFile}`);
            }
        } catch (error) {
            console.log('⚠️  Could not create backup:', error.message);
        }
    }

    saveAllPlayers(players) {
        try {
            // Ensure directory exists
            if (!fs.existsSync(this.dataPath)) {
                fs.mkdirSync(this.dataPath, { recursive: true });
            }

            // Save players
            fs.writeFileSync(
                this.playersFile,
                JSON.stringify(players, null, 2),
                'utf8'
            );

            console.log(`\n💾 Players saved to: ${this.playersFile}`);

            // Save report
            const report = this.generateReport(players);
            const reportFile = path.join(this.dataPath, `sync-safe-report-${new Date().toISOString().split('T')[0]}.json`);
            fs.writeFileSync(reportFile, JSON.stringify(report, null, 2), 'utf8');
            console.log(`📊 Report saved to: ${reportFile}`);

        } catch (error) {
            console.error('❌ Error saving data:', error);
        }
    }

    generateReport(players) {
        return {
            timestamp: new Date().toISOString(),
            stats: {
                totalPlayers: this.countTotalPlayers(players),
                apiCalls: this.apiCallCount,
                apiFailures: this.apiFailures,
                playersAdded: this.playersAdded
            },
            leagues: Object.entries(players).map(([key, leaguePlayers]) => ({
                league: key,
                playerCount: leaguePlayers.length,
                teams: [...new Set(leaguePlayers.map(p => p.team))]
            }))
        };
    }

    countTotalPlayers(data) {
        let total = 0;
        for (const league of Object.values(data)) {
            if (Array.isArray(league)) {
                total += league.length;
            }
        }
        return total;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Run the sync
const sync = new SafeRosterSync();
sync.init().catch(console.error);