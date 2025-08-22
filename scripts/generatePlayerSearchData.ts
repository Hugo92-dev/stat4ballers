import { ligue1Teams } from '../data/ligue1Teams';
import { premierLeagueTeams } from '../data/premierLeagueTeams';
import { ligaTeams } from '../data/ligaTeams';
import { serieATeams } from '../data/serieATeams';
import { bundesligaTeams } from '../data/bundesligaTeams';
import { slugifyPlayer } from '../utils/slugify';
import fs from 'fs';

interface SearchItem {
  type: 'league' | 'club' | 'player';
  id?: number;
  name: string;
  fullName?: string;
  displayName?: string;
  path: string;
  league?: string;
  club?: string;
  position?: string;
  searchTerms: string[];
}

const leagueNames: Record<string, string> = {
  'ligue1': 'Ligue 1',
  'premier-league': 'Premier League',
  'liga': 'La Liga',
  'serie-a': 'Serie A',
  'bundesliga': 'Bundesliga'
};

function generatePlayerSearchItems(): SearchItem[] {
  const playerItems: SearchItem[] = [];
  
  const allTeams = [
    ...ligue1Teams.map(t => ({ ...t, leagueSlug: 'ligue1' })),
    ...premierLeagueTeams.map(t => ({ ...t, leagueSlug: 'premier-league' })),
    ...ligaTeams.map(t => ({ ...t, leagueSlug: 'liga' })),
    ...serieATeams.map(t => ({ ...t, leagueSlug: 'serie-a' })),
    ...bundesligaTeams.map(t => ({ ...t, leagueSlug: 'bundesliga' }))
  ];

  allTeams.forEach(team => {
    team.players.forEach(player => {
      const displayName = player.displayName || player.fullName || player.name;
      const playerSlug = slugifyPlayer(displayName);
      
      // Créer les termes de recherche
      const searchTerms: string[] = [
        player.name.toLowerCase(),
        displayName.toLowerCase()
      ];
      
      // Ajouter le nom complet s'il existe
      if (player.fullName && player.fullName !== player.name) {
        searchTerms.push(player.fullName.toLowerCase());
      }
      
      // Ajouter les parties du nom
      const nameParts = displayName.split(' ');
      if (nameParts.length > 1) {
        searchTerms.push(...nameParts.map(p => p.toLowerCase()));
      }
      
      // Supprimer les doublons
      const uniqueTerms = [...new Set(searchTerms)];
      
      playerItems.push({
        type: 'player',
        id: player.id,
        name: displayName,
        fullName: player.fullName,
        displayName: player.displayName,
        path: `/${team.leagueSlug}/${team.slug}/${playerSlug}`,
        league: leagueNames[team.leagueSlug],
        club: team.name,
        position: player.position,
        searchTerms: uniqueTerms
      });
    });
  });
  
  return playerItems;
}

// Générer les données
const playerSearchItems = generatePlayerSearchItems();

// Créer le contenu du fichier
const fileContent = `// Données des joueurs pour la recherche - Généré automatiquement
// Date: ${new Date().toISOString().split('T')[0]}

import { SearchItem } from './searchDatabase';

export const playerSearchData: SearchItem[] = ${JSON.stringify(playerSearchItems, null, 2)};
`;

// Écrire le fichier
fs.writeFileSync('./data/playerSearchData.ts', fileContent);

console.log(`✓ Généré ${playerSearchItems.length} entrées de joueurs dans data/playerSearchData.ts`);