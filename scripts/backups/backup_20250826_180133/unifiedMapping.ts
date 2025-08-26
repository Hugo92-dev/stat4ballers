/**
 * Système de mapping unifié pour harmoniser les données
 * Ce fichier centralise tous les mappings entre slugs, IDs et noms
 */

// Mapping des slugs de ligues
export const LEAGUE_SLUGS = {
  'ligue1': 'ligue1',
  'premier-league': 'premier-league',
  'liga': 'liga',
  'serie-a': 'serie-a',
  'bundesliga': 'bundesliga'
} as const;

// IDs des saisons actuelles (2025/2026)
export const CURRENT_SEASON_IDS = {
  ligue1: 25651,
  premierLeague: 25583,
  liga: 25659,
  serieA: 25533,
  bundesliga: 25646
} as const;

// Mapping des slugs d'équipes harmonisés
export const TEAM_SLUG_MAPPING: Record<string, string> = {
  // Ligue 1
  'olympique-marseille': 'marseille',
  'olympique-de-marseille': 'marseille',
  'paris-saint-germain': 'psg',
  'paris-saint-germain-fc': 'psg',
  'olympique-lyonnais': 'lyon',
  'losc-lille': 'lille',
  'angers-sco': 'angers',
  'le-havre-ac': 'le-havre',
  'rc-lens': 'lens',
  'ogc-nice': 'nice',
  'stade-rennais': 'rennes',
  'stade-rennais-fc': 'rennes',
  'rc-strasbourg': 'strasbourg',
  'rc-strasbourg-alsace': 'strasbourg',
  'fc-nantes': 'nantes',
  'stade-brestois': 'brest',
  'stade-brestois-29': 'brest',
  'toulouse-fc': 'toulouse',
  'aj-auxerre': 'auxerre',
  'fc-metz': 'metz',
  'fc-lorient': 'lorient',
  'as-monaco': 'monaco',
  'montpellier-hsc': 'montpellier',
  'stade-de-reims': 'reims',
  'as-saint-etienne': 'saint-etienne',
  
  // Premier League
  'manchester-united-fc': 'manchester-united',
  'manchester-city-fc': 'manchester-city',
  'liverpool-fc': 'liverpool',
  'chelsea-fc': 'chelsea',
  'arsenal-fc': 'arsenal',
  'tottenham-hotspur': 'tottenham',
  'tottenham-hotspur-fc': 'tottenham',
  'west-ham-united': 'west-ham',
  'west-ham-united-fc': 'west-ham',
  'newcastle-united': 'newcastle',
  'newcastle-united-fc': 'newcastle',
  'aston-villa-fc': 'aston-villa',
  'brighton-and-hove-albion': 'brighton',
  'brighton-and-hove-albion-fc': 'brighton',
  'brighton-hove-albion': 'brighton',
  'wolverhampton-wanderers': 'wolves',
  'wolverhampton-wanderers-fc': 'wolves',
  'crystal-palace-fc': 'crystal-palace',
  'nottingham-forest-fc': 'nottingham-forest',
  'everton-fc': 'everton',
  'fulham-fc': 'fulham',
  'afc-bournemouth': 'bournemouth',
  'brentford-fc': 'brentford',
  'burnley-fc': 'burnley',
  'leeds-united': 'leeds',
  'leeds-united-fc': 'leeds',
  'sunderland-afc': 'sunderland',
  'leicester-city': 'leicester',
  'leicester-city-fc': 'leicester',
  'southampton-fc': 'southampton',
  'ipswich-town': 'ipswich',
  'ipswich-town-fc': 'ipswich',
  
  // La Liga
  'real-madrid-cf': 'real-madrid',
  'fc-barcelona': 'barcelona',
  'atletico-madrid': 'atletico-madrid',
  'atletico-de-madrid': 'atletico-madrid',
  'sevilla-fc': 'sevilla',
  'real-betis': 'real-betis',
  'real-betis-balompie': 'real-betis',
  'real-sociedad': 'real-sociedad',
  'athletic-club': 'athletic-bilbao',
  'athletic-bilbao': 'athletic-bilbao',
  'valencia-cf': 'valencia',
  'villarreal-cf': 'villarreal',
  'getafe-cf': 'getafe',
  'rcd-espanyol': 'espanyol',
  'ca-osasuna': 'osasuna',
  'rayo-vallecano': 'rayo-vallecano',
  'rcd-mallorca': 'mallorca',
  'celta-vigo': 'celta-vigo',
  'rc-celta': 'celta-vigo',
  'celta-de-vigo': 'celta-vigo',
  'deportivo-alaves': 'alaves',
  'elche-cf': 'elche',
  'levante-ud': 'levante',
  'girona-fc': 'girona',
  'real-valladolid': 'valladolid',
  'real-valladolid-cf': 'valladolid',
  
  // Serie A
  'juventus-fc': 'juventus',
  'ac-milan': 'milan',
  'inter-milan': 'inter',
  'fc-internazionale': 'inter',
  'ssc-napoli': 'napoli',
  'as-roma': 'roma',
  'ss-lazio': 'lazio',
  'atalanta-bc': 'atalanta',
  'acf-fiorentina': 'fiorentina',
  'torino-fc': 'torino',
  'bologna-fc': 'bologna',
  'bologna-fc-1909': 'bologna',
  'udinese-calcio': 'udinese',
  'us-sassuolo': 'sassuolo',
  'genoa-cfc': 'genoa',
  'hellas-verona': 'verona',
  'hellas-verona-fc': 'verona',
  'cagliari-calcio': 'cagliari',
  'parma-calcio': 'parma',
  'parma-calcio-1913': 'parma',
  'us-lecce': 'lecce',
  'us-cremonese': 'cremonese',
  'pisa-sc': 'pisa',
  'como-1907': 'como',
  'empoli-fc': 'empoli',
  
  // Bundesliga
  'fc-bayern-munchen': 'bayern-munich',
  'fc-bayern-münchen': 'bayern-munich',
  'borussia-dortmund': 'dortmund',
  'rb-leipzig': 'leipzig',
  'bayer-04-leverkusen': 'leverkusen',
  'bayer-leverkusen': 'leverkusen',
  'borussia-monchengladbach': 'monchengladbach',
  'borussia-mönchengladbach': 'monchengladbach',
  'eintracht-frankfurt': 'frankfurt',
  'vfl-wolfsburg': 'wolfsburg',
  'sc-freiburg': 'freiburg',
  'tsg-hoffenheim': 'hoffenheim',
  'tsg-1899-hoffenheim': 'hoffenheim',
  'vfb-stuttgart': 'stuttgart',
  'fc-koln': 'koln',
  '1-fc-koln': 'koln',
  'fc-köln': 'koln',
  'fc-union-berlin': 'union-berlin',
  '1-fc-union-berlin': 'union-berlin',
  'fc-augsburg': 'augsburg',
  'werder-bremen': 'bremen',
  'sv-werder-bremen': 'bremen',
  'mainz-05': 'mainz',
  'fsv-mainz-05': 'mainz',
  '1-fsv-mainz-05': 'mainz',
  'heidenheim': 'heidenheim',
  '1-fc-heidenheim': 'heidenheim',
  '1-fc-heidenheim-1846': 'heidenheim',
  'fc-st-pauli': 'st-pauli',
  'st-pauli': 'st-pauli',
  'hamburger-sv': 'hamburg',
  'holstein-kiel': 'holstein-kiel'
};

/**
 * Normalise un slug d'équipe
 */
export function normalizeTeamSlug(slug: string): string {
  if (!slug) return '';
  const normalized = slug.toLowerCase().trim();
  return TEAM_SLUG_MAPPING[normalized] || normalized;
}

/**
 * Obtient le nom de fichier du logo pour une équipe
 */
export function getTeamLogoFilename(teamName: string): string {
  // Mapping spécifique pour les noms de fichiers de logos
  const logoMapping: Record<string, string> = {
    // Ligue 1
    'marseille': 'Olympique Marseille.png',
    'psg': 'Paris Saint Germain.png',
    'lyon': 'Olympique Lyonnais.png',
    'lille': 'LOSC Lille.png',
    'monaco': 'Monaco.png',
    'nice': 'Nice.png',
    'lens': 'Lens.png',
    'rennes': 'Rennes.png',
    'strasbourg': 'Strasbourg.png',
    'nantes': 'Nantes.png',
    'brest': 'Brest.png',
    'toulouse': 'Toulouse.png',
    'auxerre': 'Auxerre.png',
    'angers': 'Angers SCO.png',
    'le-havre': 'Le Havre.png',
    'montpellier': 'Montpellier HSC.png',
    'reims': 'Stade de Reims.png',
    'saint-etienne': 'AS Saint-Étienne.png',
    'metz': 'FC Metz.png',
    'lorient': 'FC Lorient.png',
    'paris-fc': 'Paris.png',
    
    // Ajoutez les autres ligues selon le besoin
  };
  
  return logoMapping[teamName] || `${teamName}.png`;
}

/**
 * Trouve un joueur par son slug dans une équipe
 */
export function findPlayerBySlug(players: any[], slug: string): any {
  if (!players || !slug) return null;
  
  const normalizedSlug = slug.toLowerCase().trim();
  
  return players.find(player => {
    // Priorité 1: Slug stocké
    if (player.playerSlug === normalizedSlug) return true;
    
    // Priorité 2: Slug généré depuis displayName
    const displayName = player.displayName || player.fullName || player.nom || player.name;
    if (displayName) {
      const generatedSlug = slugifyPlayer(displayName);
      if (generatedSlug === normalizedSlug) return true;
    }
    
    return false;
  });
}

/**
 * Convertit un nom en slug
 */
function slugifyPlayer(name: string): string {
  if (!name) return '';
  
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[øØ]/g, 'o')
    .replace(/[æÆ]/g, 'ae')
    .replace(/[ßś]/g, 's')
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

/**
 * Obtient le nom de la ligue depuis le slug
 */
export function getLeagueName(leagueSlug: string): string {
  const leagueNames: Record<string, string> = {
    'ligue1': 'Ligue 1',
    'premier-league': 'Premier League',
    'liga': 'La Liga',
    'serie-a': 'Serie A',
    'bundesliga': 'Bundesliga'
  };
  
  return leagueNames[leagueSlug] || leagueSlug;
}

/**
 * Obtient la couleur de la ligue
 */
export function getLeagueColor(leagueSlug: string): string {
  const leagueColors: Record<string, string> = {
    'ligue1': 'from-blue-600 to-blue-800',
    'premier-league': 'from-purple-600 to-purple-800',
    'liga': 'from-orange-600 to-orange-800',
    'serie-a': 'from-green-600 to-green-800',
    'bundesliga': 'from-gray-800 to-black'
  };
  
  return leagueColors[leagueSlug] || 'from-gray-600 to-gray-800';
}