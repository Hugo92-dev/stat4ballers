const { database } = require('../utils/database');

// Quelques joueurs stars du PSG pour tester
const PSG_PLAYERS = [
    {
        sportmonksId: 1001,
        name: 'Kylian Mbappé',
        slug: 'kylian-mbappe',
        firstName: 'Kylian',
        lastName: 'Mbappé',
        displayName: 'Kylian Mbappé',
        position: 'Forward',
        jerseyNumber: 7,
        nationality: 'France',
        age: 25,
        isGoalkeeper: false,
        team: {
            sportmonksId: 591,
            slug: 'paris-saint-germain',
            name: 'Paris Saint Germain'
        },
        // Statistiques de test pour les radar charts
        statistics: {
            rating: 8.5,
            appearances: 38,
            goals: 44,
            assists: 10,
            minutesPlayed: 3200,
            yellowCards: 3,
            redCards: 0,
            shots: 180,
            shotsOnTarget: 95,
            keyPasses: 85,
            passAccuracy: 84,
            duelsWon: 145,
            dribbles: 142,
            successfulDribbles: 88
        },
        radarCharts: {
            general: {
                rating: 85,
                goals: 44,
                assists: 10,
                keyPasses: 85,
                dribbles: 142,
                duels: 145,
                shots: 180,
                passes: 1250
            },
            offensive: {
                goals: 44,
                assists: 10,
                shots: 180,
                shotsOnTarget: 95,
                keyPasses: 85,
                throughBalls: 32,
                successfulDribbles: 88,
                chancesCreated: 95,
                penaltiesScored: 8,
                freeKicksScored: 2,
                conversationRate: 24
            },
            defensive: {
                tackles: 12,
                blocks: 5,
                interceptions: 8,
                clearances: 3,
                aerialDuelsWon: 22,
                duelsWon: 145,
                foulsCommitted: 28,
                yellowCards: 3,
                redCards: 0,
                offsides: 45,
                savingActions: 0
            }
        }
    },
    {
        sportmonksId: 1002,
        name: 'Achraf Hakimi',
        slug: 'achraf-hakimi',
        firstName: 'Achraf',
        lastName: 'Hakimi',
        displayName: 'Achraf Hakimi',
        position: 'Defender',
        jerseyNumber: 2,
        nationality: 'Morocco',
        age: 25,
        isGoalkeeper: false,
        team: {
            sportmonksId: 591,
            slug: 'paris-saint-germain',
            name: 'Paris Saint Germain'
        },
        statistics: {
            rating: 7.8,
            appearances: 35,
            goals: 5,
            assists: 8,
            minutesPlayed: 3000
        },
        radarCharts: {
            general: {
                rating: 78,
                goals: 5,
                assists: 8,
                keyPasses: 65,
                dribbles: 89,
                duels: 125,
                shots: 45,
                passes: 1680
            },
            offensive: {
                goals: 5,
                assists: 8,
                shots: 45,
                shotsOnTarget: 18,
                keyPasses: 65,
                throughBalls: 15,
                successfulDribbles: 62,
                chancesCreated: 73,
                penaltiesScored: 0,
                freeKicksScored: 0,
                conversationRate: 11
            },
            defensive: {
                tackles: 85,
                blocks: 32,
                interceptions: 68,
                clearances: 95,
                aerialDuelsWon: 42,
                duelsWon: 125,
                foulsCommitted: 35,
                yellowCards: 5,
                redCards: 0,
                offsides: 8,
                savingActions: 0
            }
        }
    },
    {
        sportmonksId: 1003,
        name: 'Gianluigi Donnarumma',
        slug: 'gianluigi-donnarumma',
        firstName: 'Gianluigi',
        lastName: 'Donnarumma',
        displayName: 'Gianluigi Donnarumma',
        position: 'Goalkeeper',
        jerseyNumber: 99,
        nationality: 'Italy',
        age: 25,
        isGoalkeeper: true,
        team: {
            sportmonksId: 591,
            slug: 'paris-saint-germain',
            name: 'Paris Saint Germain'
        },
        statistics: {
            rating: 7.5,
            appearances: 35,
            cleanSheets: 15,
            saves: 112,
            minutesPlayed: 3150
        },
        radarCharts: {
            general: {
                rating: 75,
                cleanSheets: 15,
                saves: 112,
                punches: 18,
                passAccuracy: 82,
                duels: 25,
                aerialDuels: 35,
                minutesPlayed: 3150
            },
            goalkeeper: {
                saves: 112,
                cleanSheets: 15,
                penaltiesSaved: 3,
                punches: 18
            }
        }
    }
];

async function addTestPlayers() {
    await database.init();
    
    console.log('Adding test players for PSG...');
    
    for (const player of PSG_PLAYERS) {
        await database.findOneAndUpdate(
            'players',
            { sportmonksId: player.sportmonksId },
            { ...player, lastUpdated: new Date().toISOString() },
            { upsert: true }
        );
        console.log(`✓ Added ${player.name}`);
    }
    
    console.log('\n✅ Test players added successfully!');
}

addTestPlayers().catch(console.error);