// Mapping complet des IDs vers les noms de fichiers réels
export const clubLogoFiles: Record<string, Record<string, string>> = {
  'ligue1': {
    'psg': 'Paris Saint-Germain.png',
    'marseille': 'Olympique Marseille.png',
    'monaco': 'AS Monaco.png',
    'lille': 'LOSC Lille.png',
    'lyon': 'Olympique Lyon.png',
    'nice': 'OGC Nice.png',
    'lens': 'RC Lens.png',
    'rennes': 'Stade Rennais FC.png',
    'strasbourg': 'RC Strasbourg Alsace.png',
    'brest': 'Stade Brestois 29.png',
    'nantes': 'FC Nantes.png',
    'toulouse': 'FC Toulouse.png',
    'auxerre': 'AJ Auxerre.png',
    'angers': 'Angers SCO.png',
    'le-havre': 'Le Havre AC.png',
    'paris-fc': 'Paris FC.png',
    'metz': 'FC Metz.png',
    'lorient': 'FC Lorient.png',
  },
  'premier-league': {
    'manchester-city': 'Manchester City.png',
    'arsenal': 'Arsenal FC.png',
    'liverpool': 'Liverpool FC.png',
    'chelsea': 'Chelsea FC.png',
    'manchester-united': 'Manchester United.png',
    'tottenham': 'Tottenham Hotspur.png',
    'newcastle': 'Newcastle United.png',
    'aston-villa': 'Aston Villa.png',
    'brighton': 'Brighton & Hove Albion.png',
    'west-ham': 'West Ham United.png',
    'fulham': 'Fulham FC.png',
    'bournemouth': 'AFC Bournemouth.png',
    'brentford': 'Brentford FC.png',
    'everton': 'Everton FC.png',
    'nottingham-forest': 'Nottingham Forest.png',
    'crystal-palace': 'Crystal Palace.png',
    'wolves': 'Wolverhampton Wanderers.png',
    'leicester': 'Leicester City.png', // À vérifier
    'leeds': 'Leeds United.png',
    'southampton': 'Southampton FC.png', // À vérifier
    'burnley': 'Burnley FC.png',
    'sunderland': 'Sunderland AFC.png',
  },
  'liga': {
    'real-madrid': 'Real Madrid.png',
    'barcelona': 'FC Barcelona.png',
    'atletico-madrid': 'Atlético de Madrid.png',
    'sevilla': 'Sevilla FC.png',
    'real-sociedad': 'Real Sociedad.png',
    'real-betis': 'Real Betis Balompié.png',
    'villarreal': 'Villarreal CF.png',
    'athletic-bilbao': 'Athletic Bilbao.png',
    'valencia': 'Valencia CF.png',
    'osasuna': 'CA Osasuna.png',
    'rayo-vallecano': 'Rayo Vallecano.png',
    'celta-vigo': 'Celta de Vigo.png',
    'mallorca': 'RCD Mallorca.png',
    'girona': 'Girona FC.png',
    'getafe': 'Getafe CF.png',
    'espanyol': 'RCD Espanyol Barcelona.png',
    'cadiz': 'Cádiz CF.png', // À vérifier
    'elche': 'Elche CF.png',
    'valladolid': 'Real Valladolid.png', // À vérifier
    'almeria': 'UD Almería.png', // À vérifier
    'levante': 'Levante UD.png',
    'alaves': 'Deportivo Alavés.png',
    'real-oviedo': 'Real Oviedo.png',
  },
  'serie-a': {
    'juventus': 'Juventus FC.png',
    'inter': 'Inter Milan.png',
    'milan': 'AC Milan.png',
    'napoli': 'SSC Napoli.png',
    'roma': 'AS Roma.png',
    'lazio': 'SS Lazio.png',
    'atalanta': 'Atalanta BC.png',
    'fiorentina': 'ACF Fiorentina.png',
    'bologna': 'Bologna FC 1909.png',
    'torino': 'Torino FC.png',
    'udinese': 'Udinese Calcio.png',
    'genoa': 'Genoa CFC.png',
    'sassuolo': 'US Sassuolo.png',
    'empoli': 'Empoli FC.png', // À vérifier
    'cagliari': 'Cagliari Calcio.png',
    'spezia': 'Spezia Calcio.png', // À vérifier
    'verona': 'Hellas Verona.png',
    'salernitana': 'US Salernitana 1919.png', // À vérifier
    'sampdoria': 'UC Sampdoria.png', // À vérifier
    'venezia': 'Venezia FC.png', // À vérifier
    'como': 'Como 1907.png',
    'cremonese': 'US Cremonese.png',
    'lecce': 'US Lecce.png',
    'parme': 'Parma Calcio 1913.png',
    'pise': 'Pisa Sporting Club.png',
  },
  'bundesliga': {
    'bayern': 'Bayern Munich.png',
    'borussia-dortmund': 'Borussia Dortmund.png',
    'leipzig': 'RB Leipzig.png',
    'bayer-leverkusen': 'Bayer 04 Leverkusen.png',
    'union-berlin': '1.FC Union Berlin.png',
    'freiburg': 'SC Freiburg.png',
    'eintracht-frankfurt': 'Eintracht Frankfurt.png',
    'wolfsburg': 'VfL Wolfsburg.png',
    'mainz': '1.FSV Mainz 05.png',
    'borussia-monchengladbach': 'Borussia Mönchengladbach.png',
    'koln': '1.FC Köln.png',
    'hoffenheim': 'TSG 1899 Hoffenheim.png',
    'stuttgart': 'VfB Stuttgart.png',
    'augsburg': 'FC Augsburg.png',
    'hertha-berlin': 'Hertha BSC.png', // À vérifier
    'werder': 'SV Werder Bremen.png',
    'bochum': 'VfL Bochum.png', // À vérifier
    'hambourg': 'Hamburger SV.png',
    'sankt-pauli': 'FC St. Pauli.png',
    'heidenheim': '1.FC Heidenheim 1846.png',
  }
};

// Fonction pour obtenir le logo d'un club
export const getClubLogoPath = (leagueId: string, clubId: string): string => {
  const fileName = clubLogoFiles[leagueId]?.[clubId];
  if (fileName) {
    return `/logos/clubs/${leagueId}/${encodeURIComponent(fileName)}`;
  }
  // Fallback : essayer avec l'ID directement
  return `/logos/clubs/${leagueId}/${clubId}.png`;
};