// Centralisation des données de tous les championnats

let ligue1Data: any = null;
let premierLeagueData: any = null;
let laligaData: any = null;
let serieAData: any = null;
let bundesligaData: any = null;

// Import conditionnel des données
try {
  ligue1Data = require('@/public/data/ligue1_sportmonks_2025_26.json');
} catch (e) {
  console.log('Ligue 1 data not found');
}

try {
  premierLeagueData = require('@/public/data/premier-league_sportmonks_2025_26.json');
} catch (e) {
  console.log('Premier League data not found');
}

try {
  laligaData = require('@/public/data/laliga_sportmonks_2025_26.json');
} catch (e) {
  console.log('La Liga data not found');
}

try {
  serieAData = require('@/public/data/serie-a_sportmonks_2025_26.json');
} catch (e) {
  console.log('Serie A data not found');
}

try {
  bundesligaData = require('@/public/data/bundesliga_sportmonks_2025_26.json');
} catch (e) {
  console.log('Bundesliga data not found');
}

export const getLeagueData = (leagueId: string) => {
  switch(leagueId) {
    case 'ligue1':
      return ligue1Data;
    case 'premier-league':
      return premierLeagueData;
    case 'laliga':
      return laligaData;
    case 'serie-a':
      return serieAData;
    case 'bundesliga':
      return bundesligaData;
    default:
      return null;
  }
};

export const getClubPlayers = (leagueId: string, clubId: string) => {
  const leagueData = getLeagueData(leagueId);
  
  if (!leagueData || !leagueData.clubs) {
    return [];
  }
  
  // Trouver le club avec un matching flexible
  const club = leagueData.clubs.find((c: any) => {
    // Normaliser le nom du club depuis les données
    const clubNameLower = c.nom.toLowerCase();
    
    // Normaliser l'ID depuis l'URL
    const urlIdLower = clubId.toLowerCase();
    
    // Cas spéciaux d'abord
    const specialMatches: { [key: string]: string[] } = {
      'psg': ['paris saint-germain'],
      'paris-saint-germain': ['paris saint-germain'],
      'om': ['olympique de marseille'],
      'marseille': ['olympique de marseille'],
      'ol': ['olympique lyonnais'],
      'lyon': ['olympique lyonnais'],
      'asse': ['as saint-étienne', 'saint-étienne'],
      'saint-etienne': ['as saint-étienne', 'saint-étienne'],
      'saintetienne': ['as saint-étienne', 'saint-étienne'],
      'rennes': ['stade rennais'],
      'stade-rennais': ['stade rennais'],
      'monaco': ['as monaco'],
      'lille': ['lille osc'],
      'nice': ['ogc nice'],
      'lens': ['rc lens'],
      'reims': ['stade de reims'],
      'toulouse': ['toulouse fc'],
      'nantes': ['fc nantes'],
      'montpellier': ['montpellier hsc'],
      'strasbourg': ['rc strasbourg'],
      'brest': ['stade brestois'],
      'auxerre': ['aj auxerre'],
      'le-havre': ['le havre ac'],
      'lehavre': ['le havre ac'],
      'angers': ['angers sco'],
      // Premier League
      'man-city': ['manchester city'],
      'manchester-city': ['manchester city'],
      'man-united': ['manchester united'],
      'manchester-united': ['manchester united'],
      'arsenal': ['arsenal'],
      'chelsea': ['chelsea'],
      'liverpool': ['liverpool'],
      'tottenham': ['tottenham hotspur'],
      'spurs': ['tottenham hotspur'],
      // La Liga
      'real-madrid': ['real madrid'],
      'real': ['real madrid'],
      'barcelona': ['fc barcelona'],
      'barca': ['fc barcelona'],
      'atletico-madrid': ['atlético madrid', 'atletico madrid'],
      'atletico': ['atlético madrid', 'atletico madrid'],
      // Serie A
      'juventus': ['juventus'],
      'juve': ['juventus'],
      'milan': ['ac milan'],
      'ac-milan': ['ac milan'],
      'inter': ['inter milan'],
      'inter-milan': ['inter milan'],
      'roma': ['as roma'],
      'as-roma': ['as roma'],
      'napoli': ['ssc napoli'],
      'lazio': ['lazio'],
      // Bundesliga
      'bayern': ['bayern munich'],
      'bayern-munich': ['bayern munich'],
      'dortmund': ['borussia dortmund'],
      'bvb': ['borussia dortmund'],
      'leipzig': ['rb leipzig'],
      'rb-leipzig': ['rb leipzig'],
      'leverkusen': ['bayer 04 leverkusen'],
      'bayer-leverkusen': ['bayer 04 leverkusen']
    };
    
    // Vérifier les cas spéciaux d'abord
    if (specialMatches[urlIdLower]) {
      for (const specialName of specialMatches[urlIdLower]) {
        if (clubNameLower === specialName || clubNameLower.includes(specialName)) {
          return true;
        }
      }
    }
    
    // Créer plusieurs variantes du nom pour le matching
    const nameVariants = [
      clubNameLower,
      clubNameLower.replace(/[\s-]/g, ''), // sans espaces ni tirets
      clubNameLower.replace(/^(as |fc |rc |aj |og[cn] |ud |cd |rcd |ss[cn] |ac[f]? |us |vf[lb] |rb |sc |tsv? |1\. |stade )/, ''), // sans préfixes
      clubNameLower.split(' ').pop() || '', // dernier mot seulement
    ];
    
    const idVariants = [
      urlIdLower,
      urlIdLower.replace(/-/g, ''), // sans tirets
      urlIdLower.replace(/-/g, ' '), // tirets remplacés par espaces
    ];
    
    // Tester toutes les combinaisons
    for (const nameVar of nameVariants) {
      for (const idVar of idVariants) {
        if (nameVar === idVar) return true;
        if (nameVar.includes(idVar) && idVar.length > 3) return true;
      }
    }
    
    return false;
  });
  
  return club?.joueurs || [];
};