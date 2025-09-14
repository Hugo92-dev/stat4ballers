const fs = require('fs');
const path = require('path');

// Teams missing from database for Ligue 1 2025/2026
const missingTeams = [
    {
        sportmonksId: 690,
        name: "LOSC Lille",
        slug: "losc-lille",
        shortName: "LOSC",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/18/690.png",
        founded: 1944,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade Pierre-Mauroy",
            capacity: 50083,
            city: "Lille"
        }
    },
    {
        sportmonksId: 776,
        name: "Angers SCO",
        slug: "angers-sco",
        shortName: "SCO",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/8/776.png",
        founded: 1919,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade Raymond Kopa",
            capacity: 18752,
            city: "Angers"
        }
    },
    {
        sportmonksId: 1055,
        name: "Le Havre",
        slug: "le-havre",
        shortName: "HAC",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/31/1055.png",
        founded: 1872,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade Océane",
            capacity: 25178,
            city: "Le Havre"
        }
    },
    {
        sportmonksId: 3513,
        name: "Metz",
        slug: "metz",
        shortName: "FCM",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/25/3513.png",
        founded: 1932,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade Saint-Symphorien",
            capacity: 30000,
            city: "Metz"
        }
    },
    {
        sportmonksId: 3682,
        name: "Auxerre",
        slug: "auxerre",
        shortName: "AJA",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/2/3682.png",
        founded: 1905,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade de l'Abbé-Deschamps",
            capacity: 18541,
            city: "Auxerre"
        }
    },
    {
        sportmonksId: 4508,
        name: "Paris FC",
        slug: "paris-fc",
        shortName: "PFC",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/28/4508.png",
        founded: 1969,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade Charléty",
            capacity: 20000,
            city: "Paris"
        }
    },
    {
        sportmonksId: 6789,
        name: "Monaco",
        slug: "monaco",
        shortName: "ASM",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/5/6789.png",
        founded: 1924,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade Louis II",
            capacity: 18523,
            city: "Monaco"
        }
    },
    {
        sportmonksId: 9257,
        name: "Lorient",
        slug: "lorient",
        shortName: "FCL",
        logo: "https://cdn.sportmonks.com/images/soccer/teams/9/9257.png",
        founded: 1926,
        league: "ligue1",
        country: "France",
        venue: {
            name: "Stade du Moustoir",
            capacity: 18890,
            city: "Lorient"
        }
    }
];

// Read existing teams
const teamsPath = path.join(__dirname, '../../data/db/teams.json');
let teams = [];

try {
    const data = fs.readFileSync(teamsPath, 'utf8');
    teams = JSON.parse(data);
} catch (error) {
    console.error('Error reading teams.json:', error);
    process.exit(1);
}

// Add missing teams
missingTeams.forEach(team => {
    // Check if team already exists
    const exists = teams.some(t => t.sportmonksId === team.sportmonksId);

    if (!exists) {
        // Generate ID
        team.id = Date.now().toString() + Math.floor(Math.random() * 1000);
        team.lastUpdated = new Date().toISOString();

        teams.push(team);
        console.log(`✅ Added ${team.name} to database`);
    } else {
        console.log(`⚠️ ${team.name} already exists in database`);
    }
});

// Sort teams by sportmonksId
teams.sort((a, b) => a.sportmonksId - b.sportmonksId);

// Write back to file
try {
    fs.writeFileSync(teamsPath, JSON.stringify(teams, null, 2));
    console.log('\n✅ Teams database updated successfully!');
} catch (error) {
    console.error('Error writing teams.json:', error);
    process.exit(1);
}