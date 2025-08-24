// Chargement simplifié des données - uniquement Ligue 1 pour le moment
import ligue1Data from '@/public/data/ligue1_sportmonks_2025_26.json';

// Pour les autres ligues, on utilisera des placeholders pour le moment
const emptyLeague = { clubs: [] };

export const getLeagueData = (leagueId: string) => {
  switch(leagueId) {
    case 'ligue1':
      return ligue1Data;
    case 'premier-league':
    case 'laliga':
    case 'serie-a':
    case 'bundesliga':
      // TODO: Charger les autres ligues
      return emptyLeague;
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
    const clubNameLower = c.nom.toLowerCase();
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
      'brestois': ['stade brestois'],
      'auxerre': ['aj auxerre'],
      'le-havre': ['le havre ac'],
      'lehavre': ['le havre ac'],
      'angers': ['angers sco']
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