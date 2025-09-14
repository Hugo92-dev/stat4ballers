const { database, League, Team, Player } = require('../utils/database');

async function initTestData() {
    await database.init();
    
    // Add test teams for Ligue 1 with proper slugs
    const testTeams = [
        {
            sportmonksId: 591,
            name: 'Paris Saint-Germain',
            slug: 'paris-saint-germain',
            shortName: 'PSG',
            logo: '/images/teams/psg.png',
            venue: {
                name: 'Parc des Princes',
                capacity: 47929,
                city: 'Paris'
            }
        },
        {
            sportmonksId: 592,
            name: 'Olympique de Marseille',
            slug: 'olympique-de-marseille',
            shortName: 'OM',
            logo: '/images/teams/om.png',
            venue: {
                name: 'Orange Vélodrome',
                capacity: 67394,
                city: 'Marseille'
            }
        },
        {
            sportmonksId: 593,
            name: 'Olympique Lyonnais',
            slug: 'olympique-lyonnais',
            shortName: 'OL',
            logo: '/images/teams/ol.png',
            venue: {
                name: 'Groupama Stadium',
                capacity: 59186,
                city: 'Lyon'
            }
        },
        {
            sportmonksId: 594,
            name: 'AS Monaco',
            slug: 'as-monaco',
            shortName: 'ASM',
            logo: '/images/teams/monaco.png',
            venue: {
                name: 'Stade Louis II',
                capacity: 18523,
                city: 'Monaco'
            }
        },
        {
            sportmonksId: 595,
            name: 'LOSC Lille',
            slug: 'losc-lille',
            shortName: 'LOSC',
            logo: '/images/teams/lille.png',
            venue: {
                name: 'Stade Pierre-Mauroy',
                capacity: 50157,
                city: 'Lille'
            }
        }
    ];
    
    // Insert teams
    for (const team of testTeams) {
        await database.findOneAndUpdate(
            'teams',
            { sportmonksId: team.sportmonksId },
            team,
            { upsert: true }
        );
    }
    
    console.log('✅ Test data initialized with team slugs');
}

initTestData().catch(console.error);