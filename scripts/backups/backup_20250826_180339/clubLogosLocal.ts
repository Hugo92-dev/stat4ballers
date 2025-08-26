// Configuration des logos locaux des clubs
// Les logos doivent être placés dans /public/logos/clubs/[league]/[club-id].png

export const getClubLogo = (leagueId: string, clubId: string): string => {
  // Retourne le chemin local du logo
  return `/logos/clubs/${leagueId}/${clubId}.png`;
};

// Mapping des IDs de clubs pour référence
export const clubIds = {
  ligue1: [
    'psg', 'marseille', 'monaco', 'lille', 'lyon', 'nice', 'lens', 'rennes',
    'strasbourg', 'brest', 'nantes', 'toulouse', 'auxerre', 'angers',
    'le-havre', 'paris-fc', 'metz', 'lorient'
  ],
  'premier-league': [
    'manchester-city', 'arsenal', 'liverpool', 'chelsea', 'manchester-united',
    'tottenham', 'newcastle', 'aston-villa', 'brighton', 'west-ham', 'fulham',
    'bournemouth', 'brentford', 'everton', 'nottingham-forest', 'crystal-palace',
    'wolves', 'leicester', 'leeds', 'southampton'
  ],
  liga: [
    'real-madrid', 'barcelone', 'atletico-madrid', 'sevilla', 'real-sociedad',
    'real-betis', 'villarreal', 'athletic-bilbao', 'valencia', 'osasuna',
    'rayo-vallecano', 'celta-vigo', 'mallorca', 'girona', 'getafe',
    'espanyol', 'cadiz', 'elche', 'valladolid', 'almeria'
  ],
  'serie-a': [
    'juventus', 'inter', 'milan', 'napoli', 'roma', 'lazio', 'atalanta',
    'fiorentina', 'bologna', 'torino', 'udinese', 'genoa', 'sassuolo',
    'empoli', 'cagliari', 'spezia', 'verona', 'salernitana', 'sampdoria', 'venezia'
  ],
  bundesliga: [
    'bayern', 'borussia-dortmund', 'leipzig', 'bayer-leverkusen', 'union-berlin',
    'freiburg', 'eintracht-frankfurt', 'wolfsburg', 'mainz', 'borussia-monchengladbach',
    'koln', 'hoffenheim', 'stuttgart', 'augsburg', 'hertha-berlin', 'werder',
    'bochum', 'hambourg'
  ]
};