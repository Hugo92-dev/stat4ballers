export interface Team {
  id: string;
  name: string;
  logo?: string;
  stadium: string;
  founded: number;
  colors: string[];
  stats?: {
    position: number;
    points: number;
    played: number;
    wins: number;
    draws: number;
    losses: number;
  };
}

export interface League {
  id: string;
  name: string;
  flag: string;
  gradient: string;
  teams: Team[];
}

export const ligue1Teams: Team[] = [
  { id: 'psg', name: 'Paris Saint-Germain', stadium: 'Parc des Princes', founded: 1970, colors: ['#004170', '#DA020E', '#FFFFFF'] },
  { id: 'marseille', name: 'Olympique de Marseille', stadium: 'Orange Vélodrome', founded: 1899, colors: ['#2FAEE0', '#FFFFFF'] },
  { id: 'monaco', name: 'AS Monaco', stadium: 'Stade Louis II', founded: 1924, colors: ['#E63031', '#FFFFFF'] },
  { id: 'lille', name: 'LOSC Lille', stadium: 'Stade Pierre-Mauroy', founded: 1944, colors: ['#DC143C', '#FFFFFF', '#000080'] },
  { id: 'lyon', name: 'Olympique Lyonnais', stadium: 'Groupama Stadium', founded: 1950, colors: ['#DA020E', '#0033A0', '#FFFFFF'] },
  { id: 'nice', name: 'OGC Nice', stadium: 'Allianz Riviera', founded: 1904, colors: ['#CC0000', '#000000'] },
  { id: 'lens', name: 'RC Lens', stadium: 'Stade Bollaert-Delelis', founded: 1906, colors: ['#FFD700', '#FF0000'] },
  { id: 'rennes', name: 'Stade Rennais', stadium: 'Roazhon Park', founded: 1901, colors: ['#E13327', '#000000'] },
  { id: 'strasbourg', name: 'RC Strasbourg', stadium: 'Stade de la Meinau', founded: 1906, colors: ['#0099E0', '#FFFFFF'] },
  { id: 'brest', name: 'Stade Brestois', stadium: 'Stade Francis-Le Blé', founded: 1950, colors: ['#ED1C24', '#FFFFFF'] },
  { id: 'nantes', name: 'FC Nantes', stadium: 'Stade de la Beaujoire', founded: 1943, colors: ['#FCD405', '#008C3B'] },
  { id: 'toulouse', name: 'Toulouse FC', stadium: 'Stadium de Toulouse', founded: 1970, colors: ['#612B8A', '#FFFFFF'] },
  { id: 'auxerre', name: 'AJ Auxerre', stadium: 'Stade de l\'Abbé-Deschamps', founded: 1905, colors: ['#FFFFFF', '#87CEEB'] },
  { id: 'angers', name: 'Angers SCO', stadium: 'Stade Raymond Kopa', founded: 1919, colors: ['#FFFFFF', '#000000'] },
  { id: 'le-havre', name: 'Le Havre AC', stadium: 'Stade Océane', founded: 1894, colors: ['#003DA5', '#87CEEB'] },
  { id: 'paris-fc', name: 'Paris FC', stadium: 'Stade Charléty', founded: 1969, colors: ['#0033A0', '#FFFFFF'] },
  { id: 'metz', name: 'FC Metz', stadium: 'Stade Saint-Symphorien', founded: 1932, colors: ['#6F1E51', '#FFFFFF'] },
  { id: 'lorient', name: 'FC Lorient', stadium: 'Stade du Moustoir', founded: 1926, colors: ['#FF6600', '#000000'] }
];

export const premierLeagueTeams: Team[] = [
  { id: 'manchester-city', name: 'Manchester City', stadium: 'Etihad Stadium', founded: 1880, colors: ['#6CABDD', '#FFFFFF'] },
  { id: 'arsenal', name: 'Arsenal', stadium: 'Emirates Stadium', founded: 1886, colors: ['#EF0107', '#FFFFFF'] },
  { id: 'liverpool', name: 'Liverpool', stadium: 'Anfield', founded: 1892, colors: ['#C8102E', '#00B2A9'] },
  { id: 'chelsea', name: 'Chelsea', stadium: 'Stamford Bridge', founded: 1905, colors: ['#034694', '#FFFFFF'] },
  { id: 'manchester-united', name: 'Manchester United', stadium: 'Old Trafford', founded: 1878, colors: ['#DA020E', '#FBE122'] },
  { id: 'tottenham', name: 'Tottenham Hotspur', stadium: 'Tottenham Hotspur Stadium', founded: 1882, colors: ['#132257', '#FFFFFF'] },
  { id: 'newcastle', name: 'Newcastle United', stadium: 'St James\' Park', founded: 1892, colors: ['#241F20', '#FFFFFF'] },
  { id: 'aston-villa', name: 'Aston Villa', stadium: 'Villa Park', founded: 1874, colors: ['#670E36', '#95BFE5'] },
  { id: 'brighton', name: 'Brighton & Hove Albion', stadium: 'Amex Stadium', founded: 1901, colors: ['#0057B8', '#FFFFFF'] },
  { id: 'west-ham', name: 'West Ham United', stadium: 'London Stadium', founded: 1895, colors: ['#7A263A', '#1BB1E7'] },
  { id: 'fulham', name: 'Fulham', stadium: 'Craven Cottage', founded: 1879, colors: ['#FFFFFF', '#000000'] },
  { id: 'bournemouth', name: 'AFC Bournemouth', stadium: 'Vitality Stadium', founded: 1899, colors: ['#DA020E', '#000000'] },
  { id: 'brentford', name: 'Brentford', stadium: 'Brentford Community Stadium', founded: 1889, colors: ['#FFD700', '#FF0000'] },
  { id: 'everton', name: 'Everton', stadium: 'Goodison Park', founded: 1878, colors: ['#003399', '#FFFFFF'] },
  { id: 'nottingham-forest', name: 'Nottingham Forest', stadium: 'City Ground', founded: 1865, colors: ['#DD0000', '#FFFFFF'] },
  { id: 'crystal-palace', name: 'Crystal Palace', stadium: 'Selhurst Park', founded: 1905, colors: ['#1B458F', '#C4122E'] },
  { id: 'wolves', name: 'Wolverhampton Wanderers', stadium: 'Molineux Stadium', founded: 1877, colors: ['#FDB913', '#231F20'] },
  { id: 'leicester', name: 'Leicester City', stadium: 'King Power Stadium', founded: 1884, colors: ['#003090', '#FDBE11'] },
  { id: 'leeds', name: 'Leeds United', stadium: 'Elland Road', founded: 1919, colors: ['#FFCD00', '#003090'] },
  { id: 'southampton', name: 'Southampton', stadium: 'St Mary\'s Stadium', founded: 1885, colors: ['#D71920', '#130C0E'] }
];

export const ligaTeams: Team[] = [
  { id: 'real-madrid', name: 'Real Madrid', stadium: 'Santiago Bernabéu', founded: 1902, colors: ['#FFFFFF', '#D7B903'] },
  { id: 'barcelone', name: 'FC Barcelone', stadium: 'Camp Nou', founded: 1899, colors: ['#A50044', '#004D98'] },
  { id: 'atletico-madrid', name: 'Atlético Madrid', stadium: 'Civitas Metropolitano', founded: 1903, colors: ['#CE3524', '#FFFFFF', '#272E61'] },
  { id: 'sevilla', name: 'Sevilla FC', stadium: 'Ramón Sánchez Pizjuán', founded: 1890, colors: ['#F43333', '#FFFFFF'] },
  { id: 'real-sociedad', name: 'Real Sociedad', stadium: 'Reale Arena', founded: 1909, colors: ['#0067B1', '#FFFFFF'] },
  { id: 'real-betis', name: 'Real Betis', stadium: 'Benito Villamarín', founded: 1907, colors: ['#00954F', '#FFFFFF'] },
  { id: 'villarreal', name: 'Villarreal CF', stadium: 'Estadio de la Cerámica', founded: 1923, colors: ['#FFE667', '#005187'] },
  { id: 'athletic-bilbao', name: 'Athletic Bilbao', stadium: 'San Mamés', founded: 1898, colors: ['#EE2523', '#FFFFFF', '#000000'] },
  { id: 'valencia', name: 'Valencia CF', stadium: 'Mestalla', founded: 1919, colors: ['#EE3524', '#FFDF1C'] },
  { id: 'osasuna', name: 'CA Osasuna', stadium: 'El Sadar', founded: 1920, colors: ['#D91A21', '#0A346F'] },
  { id: 'rayo-vallecano', name: 'Rayo Vallecano', stadium: 'Campo de Vallecas', founded: 1924, colors: ['#E53027', '#FFFFFF'] },
  { id: 'celta-vigo', name: 'Celta Vigo', stadium: 'Balaídos', founded: 1923, colors: ['#8AC3EE', '#FFFFFF'] },
  { id: 'mallorca', name: 'RCD Mallorca', stadium: 'Visit Mallorca Estadi', founded: 1916, colors: ['#E20613', '#000000'] },
  { id: 'girona', name: 'Girona FC', stadium: 'Estadi Montilivi', founded: 1930, colors: ['#CD2534', '#FFFFFF'] },
  { id: 'getafe', name: 'Getafe CF', stadium: 'Coliseum Alfonso Pérez', founded: 1983, colors: ['#005999', '#FFFFFF'] },
  { id: 'espanyol', name: 'RCD Espanyol', stadium: 'RCDE Stadium', founded: 1900, colors: ['#007FC8', '#FFFFFF'] },
  { id: 'cadiz', name: 'Cádiz CF', stadium: 'Nuevo Mirandilla', founded: 1910, colors: ['#F7E810', '#0045A5'] },
  { id: 'elche', name: 'Elche CF', stadium: 'Manuel Martínez Valero', founded: 1923, colors: ['#4B7F3C', '#FFFFFF'] },
  { id: 'valladolid', name: 'Real Valladolid', stadium: 'José Zorrilla', founded: 1928, colors: ['#5B2482', '#FFFFFF'] },
  { id: 'almeria', name: 'UD Almería', stadium: 'Power Horse Stadium', founded: 1989, colors: ['#EE1119', '#FFFFFF'] }
];

export const serieATeams: Team[] = [
  { id: 'juventus', name: 'Juventus', stadium: 'Allianz Stadium', founded: 1897, colors: ['#000000', '#FFFFFF'] },
  { id: 'inter', name: 'Inter Milan', stadium: 'San Siro', founded: 1908, colors: ['#0068A8', '#000000'] },
  { id: 'milan', name: 'AC Milan', stadium: 'San Siro', founded: 1899, colors: ['#FB090B', '#000000'] },
  { id: 'napoli', name: 'SSC Napoli', stadium: 'Diego Armando Maradona', founded: 1926, colors: ['#12A0D7', '#FFFFFF'] },
  { id: 'roma', name: 'AS Roma', stadium: 'Stadio Olimpico', founded: 1927, colors: ['#8E1F2F', '#FBCE38'] },
  { id: 'lazio', name: 'SS Lazio', stadium: 'Stadio Olimpico', founded: 1900, colors: ['#87D8F7', '#FFFFFF'] },
  { id: 'atalanta', name: 'Atalanta', stadium: 'Gewiss Stadium', founded: 1907, colors: ['#1E71B8', '#000000'] },
  { id: 'fiorentina', name: 'Fiorentina', stadium: 'Artemio Franchi', founded: 1926, colors: ['#792F8C', '#FFFFFF'] },
  { id: 'bologna', name: 'Bologna', stadium: 'Renato Dall\'Ara', founded: 1909, colors: ['#1A2F48', '#CA3433'] },
  { id: 'torino', name: 'Torino', stadium: 'Olimpico Grande Torino', founded: 1906, colors: ['#881F1B', '#FFFFFF'] },
  { id: 'udinese', name: 'Udinese', stadium: 'Dacia Arena', founded: 1896, colors: ['#000000', '#FFFFFF'] },
  { id: 'genoa', name: 'Genoa', stadium: 'Luigi Ferraris', founded: 1893, colors: ['#9B1915', '#003A70'] },
  { id: 'sassuolo', name: 'Sassuolo', stadium: 'Mapei Stadium', founded: 1920, colors: ['#00A752', '#000000'] },
  { id: 'empoli', name: 'Empoli', stadium: 'Carlo Castellani', founded: 1920, colors: ['#1B76BC', '#FFFFFF'] },
  { id: 'cagliari', name: 'Cagliari', stadium: 'Unipol Domus', founded: 1920, colors: ['#B01028', '#001C58'] },
  { id: 'spezia', name: 'Spezia', stadium: 'Alberto Picco', founded: 1906, colors: ['#FFFFFF', '#000000'] },
  { id: 'verona', name: 'Hellas Verona', stadium: 'Marcantonio Bentegodi', founded: 1903, colors: ['#002F6C', '#FFD100'] },
  { id: 'salernitana', name: 'Salernitana', stadium: 'Arechi', founded: 1919, colors: ['#62001F', '#FFFFFF'] },
  { id: 'sampdoria', name: 'Sampdoria', stadium: 'Luigi Ferraris', founded: 1946, colors: ['#003A7D', '#FFFFFF', '#D41239'] },
  { id: 'venezia', name: 'Venezia', stadium: 'Pier Luigi Penzo', founded: 1907, colors: ['#FF6900', '#000000', '#009E49'] }
];

export const bundesligaTeams: Team[] = [
  { id: 'bayern', name: 'Bayern Munich', stadium: 'Allianz Arena', founded: 1900, colors: ['#DC052D', '#FFFFFF'] },
  { id: 'borussia-dortmund', name: 'Borussia Dortmund', stadium: 'Signal Iduna Park', founded: 1909, colors: ['#FDE100', '#000000'] },
  { id: 'leipzig', name: 'RB Leipzig', stadium: 'Red Bull Arena', founded: 2009, colors: ['#DD0741', '#FFFFFF'] },
  { id: 'bayer-leverkusen', name: 'Bayer Leverkusen', stadium: 'BayArena', founded: 1904, colors: ['#E32221', '#000000'] },
  { id: 'union-berlin', name: 'Union Berlin', stadium: 'Stadion An der Alten Försterei', founded: 1966, colors: ['#EB1923', '#FFFFFF'] },
  { id: 'freiburg', name: 'SC Freiburg', stadium: 'Europa-Park Stadion', founded: 1904, colors: ['#EE1C25', '#FFFFFF'] },
  { id: 'eintracht-frankfurt', name: 'Eintracht Frankfurt', stadium: 'Deutsche Bank Park', founded: 1899, colors: ['#E00034', '#000000', '#FFFFFF'] },
  { id: 'wolfsburg', name: 'VfL Wolfsburg', stadium: 'Volkswagen Arena', founded: 1945, colors: ['#65B32E', '#FFFFFF'] },
  { id: 'mainz', name: 'Mainz 05', stadium: 'Mewa Arena', founded: 1905, colors: ['#C3141E', '#FFFFFF'] },
  { id: 'borussia-monchengladbach', name: 'Borussia Mönchengladbach', stadium: 'Borussia-Park', founded: 1900, colors: ['#000000', '#FFFFFF', '#007A33'] },
  { id: 'koln', name: 'FC Köln', stadium: 'RheinEnergieStadion', founded: 1948, colors: ['#ED1C24', '#FFFFFF'] },
  { id: 'hoffenheim', name: 'TSG Hoffenheim', stadium: 'PreZero Arena', founded: 1899, colors: ['#1961AC', '#FFFFFF'] },
  { id: 'stuttgart', name: 'VfB Stuttgart', stadium: 'Mercedes-Benz Arena', founded: 1893, colors: ['#E32219', '#FFFFFF'] },
  { id: 'augsburg', name: 'FC Augsburg', stadium: 'WWK Arena', founded: 1907, colors: ['#BA3733', '#46714D'] },
  { id: 'hertha-berlin', name: 'Hertha Berlin', stadium: 'Olympiastadion', founded: 1892, colors: ['#005CA9', '#FFFFFF'] },
  { id: 'werder', name: 'Werder Bremen', stadium: 'Weserstadion', founded: 1899, colors: ['#1D9053', '#FFFFFF'] },
  { id: 'bochum', name: 'VfL Bochum', stadium: 'Vonovia Ruhrstadion', founded: 1848, colors: ['#005BA6', '#FFFFFF'] },
  { id: 'hambourg', name: 'Hamburger SV', stadium: 'Volksparkstadion', founded: 1887, colors: ['#003278', '#FFFFFF', '#ED1B23'] }
];