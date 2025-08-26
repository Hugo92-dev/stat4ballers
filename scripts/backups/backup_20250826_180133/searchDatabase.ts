export interface SearchItem {
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

export const searchDatabase: SearchItem[] = [
  // Leagues
  { type: 'league', name: 'Ligue 1', path: '/ligue1', searchTerms: ['ligue 1', 'ligue1', 'france', 'championnat france'] },
  { type: 'league', name: 'Premier League', path: '/premier-league', searchTerms: ['premier league', 'angleterre', 'england', 'pl'] },
  { type: 'league', name: 'La Liga', path: '/liga', searchTerms: ['liga', 'la liga', 'espagne', 'spain', 'liga santander'] },
  { type: 'league', name: 'Serie A', path: '/serie-a', searchTerms: ['serie a', 'italie', 'italy', 'calcio'] },
  { type: 'league', name: 'Bundesliga', path: '/bundesliga', searchTerms: ['bundesliga', 'allemagne', 'germany'] },
  
  // Ligue 1 Clubs
  { type: 'club', name: 'Paris Saint-Germain', path: '/ligue1/psg', league: 'Ligue 1', searchTerms: ['psg', 'paris', 'paris saint germain', 'paris sg'] },
  { type: 'club', name: 'Olympique de Marseille', path: '/ligue1/marseille', league: 'Ligue 1', searchTerms: ['om', 'marseille', 'olympique marseille', 'olympique de mar'] },
  { type: 'club', name: 'AS Monaco', path: '/ligue1/monaco', league: 'Ligue 1', searchTerms: ['monaco', 'as monaco', 'asm'] },
  { type: 'club', name: 'LOSC Lille', path: '/ligue1/lille', league: 'Ligue 1', searchTerms: ['lille', 'losc', 'losc lille'] },
  { type: 'club', name: 'Olympique Lyonnais', path: '/ligue1/lyon', league: 'Ligue 1', searchTerms: ['lyon', 'ol', 'olympique lyonnais'] },
  { type: 'club', name: 'OGC Nice', path: '/ligue1/nice', league: 'Ligue 1', searchTerms: ['nice', 'ogc nice'] },
  { type: 'club', name: 'RC Lens', path: '/ligue1/lens', league: 'Ligue 1', searchTerms: ['lens', 'rc lens', 'racing lens'] },
  { type: 'club', name: 'Stade Rennais', path: '/ligue1/rennes', league: 'Ligue 1', searchTerms: ['rennes', 'stade rennais', 'srfc'] },
  { type: 'club', name: 'RC Strasbourg', path: '/ligue1/strasbourg', league: 'Ligue 1', searchTerms: ['strasbourg', 'rc strasbourg', 'racing strasbourg'] },
  { type: 'club', name: 'Stade Brestois', path: '/ligue1/brest', league: 'Ligue 1', searchTerms: ['brest', 'stade brestois', 'sb29'] },
  { type: 'club', name: 'FC Nantes', path: '/ligue1/nantes', league: 'Ligue 1', searchTerms: ['nantes', 'fc nantes', 'fcn'] },
  { type: 'club', name: 'Toulouse FC', path: '/ligue1/toulouse', league: 'Ligue 1', searchTerms: ['toulouse', 'tfc', 'toulouse fc'] },
  
  // Premier League Clubs
  { type: 'club', name: 'Manchester City', path: '/premier-league/manchester-city', league: 'Premier League', searchTerms: ['manchester city', 'man city', 'city', 'mcfc'] },
  { type: 'club', name: 'Arsenal', path: '/premier-league/arsenal', league: 'Premier League', searchTerms: ['arsenal', 'gunners', 'afc'] },
  { type: 'club', name: 'Liverpool', path: '/premier-league/liverpool', league: 'Premier League', searchTerms: ['liverpool', 'lfc', 'reds'] },
  { type: 'club', name: 'Chelsea', path: '/premier-league/chelsea', league: 'Premier League', searchTerms: ['chelsea', 'cfc', 'blues'] },
  { type: 'club', name: 'Manchester United', path: '/premier-league/manchester-united', league: 'Premier League', searchTerms: ['manchester united', 'man united', 'united', 'mufc', 'man u'] },
  { type: 'club', name: 'Tottenham Hotspur', path: '/premier-league/tottenham', league: 'Premier League', searchTerms: ['tottenham', 'spurs', 'thfc', 'tottenham hotspur'] },
  
  // Liga Clubs
  { type: 'club', name: 'Real Madrid', path: '/liga/real-madrid', league: 'La Liga', searchTerms: ['real madrid', 'real', 'madrid', 'rmcf'] },
  { type: 'club', name: 'FC Barcelone', path: '/liga/barcelone', league: 'La Liga', searchTerms: ['barcelone', 'barcelona', 'barca', 'fcb', 'barça'] },
  { type: 'club', name: 'Atlético Madrid', path: '/liga/atletico-madrid', league: 'La Liga', searchTerms: ['atletico madrid', 'atletico', 'atleti', 'atm'] },
  { type: 'club', name: 'Sevilla FC', path: '/liga/sevilla', league: 'La Liga', searchTerms: ['sevilla', 'sevilla fc', 'sfc'] },
  { type: 'club', name: 'Valencia CF', path: '/liga/valencia', league: 'La Liga', searchTerms: ['valencia', 'valencia cf', 'vcf'] },
  
  // Serie A Clubs
  { type: 'club', name: 'Juventus', path: '/serie-a/juventus', league: 'Serie A', searchTerms: ['juventus', 'juve', 'juventus fc'] },
  { type: 'club', name: 'Inter Milan', path: '/serie-a/inter', league: 'Serie A', searchTerms: ['inter', 'inter milan', 'internazionale'] },
  { type: 'club', name: 'AC Milan', path: '/serie-a/milan', league: 'Serie A', searchTerms: ['milan', 'ac milan', 'rossoneri'] },
  { type: 'club', name: 'SSC Napoli', path: '/serie-a/napoli', league: 'Serie A', searchTerms: ['napoli', 'naples', 'ssc napoli'] },
  { type: 'club', name: 'AS Roma', path: '/serie-a/roma', league: 'Serie A', searchTerms: ['roma', 'as roma', 'rome'] },
  
  // Bundesliga Clubs
  { type: 'club', name: 'Bayern Munich', path: '/bundesliga/bayern', league: 'Bundesliga', searchTerms: ['bayern', 'bayern munich', 'bayern munchen', 'fcb'] },
  { type: 'club', name: 'Borussia Dortmund', path: '/bundesliga/borussia-dortmund', league: 'Bundesliga', searchTerms: ['dortmund', 'borussia dortmund', 'bvb'] },
  { type: 'club', name: 'RB Leipzig', path: '/bundesliga/leipzig', league: 'Bundesliga', searchTerms: ['leipzig', 'rb leipzig', 'red bull leipzig'] },
  { type: 'club', name: 'Bayer Leverkusen', path: '/bundesliga/bayer-leverkusen', league: 'Bundesliga', searchTerms: ['leverkusen', 'bayer leverkusen', 'bayer'] },
];

// Import player data dynamically generated from team rosters
import { playerSearchData } from './playerSearchData';

// Combine all search data
export const fullSearchDatabase = [...searchDatabase, ...playerSearchData];