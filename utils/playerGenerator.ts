// Générateur de joueurs avec données mock réalistes
export interface PlayerData {
  id: string;
  nom: string;
  poste: string;
  numero: number;
  buts: number;
  passes_decisives: number;
  minutes: number;
  age: number;
  valeur: number;
  // Stats supplémentaires pour les graphiques
  ppm: number;
  titu: number;
  absences: number;
  cartons: number;
  xg: number;
  xa: number;
  tirs: number;
  tirs_cadres: number;
  penalty: number;
  courses: number;
  interceptions: number;
  tacles: number;
  aeriens: number;
  pressings: number;
  f_subies: number;
  f_commises: number;
  c_jaunes: number;
  c_rouges: number;
  touches: number;
  dribbles: number;
  passes: number;
  p_cles: number;
  p_avant: number;
  p_courtes: number;
  p_longues: number;
  centres: number;
}

export interface PlayerStats {
  generalData: {
    goals: number;
    shotActions: number;
    assists: number;
    touches: number;
    penaltyAreaPasses: number;
    finalThirdPasses: number;
    penaltyAreaCrosses: number;
    successfulDribbles: number;
  };
  possessionData: {
    touches: number;
    successfulDribbles: number;
    successfulPasses: number;
    progressivePasses: number;
    pressureControls: number;
    progressiveRuns: number;
    assists: number;
    shotActions: number;
  };
  performanceData: {
    goals: number;
    assists: number;
    nonPenaltyXG: number;
    xA: number;
    shotActions: number;
    defensiveActions: number;
    nonPenaltyShots: number;
    touches: number;
  };
  defensiveData: {
    defensiveActions: number;
    successfulTackles: number;
    interceptions: number;
    ballsRecovered: number;
    aerialDuelsWon: number;
    clearances: number;
    errorsLeadingToShot: number;
    successfulPasses: number;
  };
}

const firstNames = ['Lucas', 'Marco', 'João', 'Carlos', 'Luis', 'Diego', 'Pablo', 'Kevin', 'Thomas', 'Pierre', 'Antoine', 'Mohamed', 'Karim', 'Youssef', 'James', 'David', 'Michael', 'Robert', 'Andrea', 'Lorenzo'];
const lastNames = ['Silva', 'Santos', 'Garcia', 'Rodriguez', 'Martinez', 'Lopez', 'Gonzalez', 'Hernandez', 'Müller', 'Schmidt', 'Dupont', 'Martin', 'Bernard', 'Smith', 'Johnson', 'Williams', 'Rossi', 'Ferrari', 'Bianchi', 'Romano'];

function randomBetween(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateStats(poste: string): Partial<PlayerData> {
  const baseStats = {
    minutes: randomBetween(500, 3000),
    age: randomBetween(18, 35),
    valeur: randomBetween(5, 80),
    ppm: Number((Math.random() * 2 + 1).toFixed(1)),
    titu: randomBetween(5, 30),
    absences: randomBetween(0, 30),
    touches: randomBetween(500, 2500),
    passes: randomBetween(300, 2000),
    p_courtes: randomBetween(75, 95),
    p_longues: randomBetween(50, 85),
  };

  // Stats spécifiques par poste
  if (poste === 'Gardien') {
    return {
      ...baseStats,
      buts: 0,
      passes_decisives: 0,
      cartons: randomBetween(0, 3),
      xg: 0,
      xa: 0,
      tirs: 0,
      tirs_cadres: 0,
      penalty: 0,
      courses: 0,
      interceptions: randomBetween(0, 10),
      tacles: 0,
      aeriens: randomBetween(10, 30),
      pressings: 0,
      f_subies: randomBetween(0, 5),
      f_commises: randomBetween(0, 3),
      c_jaunes: randomBetween(0, 2),
      c_rouges: 0,
      dribbles: 0,
      p_cles: 0,
      p_avant: randomBetween(10, 30),
      centres: 0,
    };
  } else if (poste === 'Défenseur') {
    return {
      ...baseStats,
      buts: randomBetween(0, 5),
      passes_decisives: randomBetween(0, 4),
      cartons: randomBetween(2, 8),
      xg: Number((Math.random() * 3).toFixed(1)),
      xa: Number((Math.random() * 3).toFixed(1)),
      tirs: randomBetween(10, 40),
      tirs_cadres: randomBetween(20, 50),
      penalty: 0,
      courses: randomBetween(50, 150),
      interceptions: randomBetween(30, 70),
      tacles: randomBetween(40, 80),
      aeriens: randomBetween(30, 60),
      pressings: randomBetween(80, 150),
      f_subies: randomBetween(10, 40),
      f_commises: randomBetween(15, 35),
      c_jaunes: randomBetween(2, 7),
      c_rouges: randomBetween(0, 1),
      dribbles: randomBetween(5, 30),
      p_cles: randomBetween(5, 20),
      p_avant: randomBetween(50, 100),
      centres: randomBetween(5, 30),
    };
  } else if (poste === 'Milieu') {
    return {
      ...baseStats,
      buts: randomBetween(2, 10),
      passes_decisives: randomBetween(3, 12),
      cartons: randomBetween(2, 6),
      xg: Number((Math.random() * 8).toFixed(1)),
      xa: Number((Math.random() * 10).toFixed(1)),
      tirs: randomBetween(20, 60),
      tirs_cadres: randomBetween(30, 60),
      penalty: randomBetween(0, 100),
      courses: randomBetween(80, 180),
      interceptions: randomBetween(20, 50),
      tacles: randomBetween(30, 60),
      aeriens: randomBetween(10, 40),
      pressings: randomBetween(100, 200),
      f_subies: randomBetween(20, 50),
      f_commises: randomBetween(15, 30),
      c_jaunes: randomBetween(2, 5),
      c_rouges: 0,
      dribbles: randomBetween(20, 50),
      p_cles: randomBetween(20, 60),
      p_avant: randomBetween(80, 150),
      centres: randomBetween(10, 40),
    };
  } else { // Attaquant
    return {
      ...baseStats,
      buts: randomBetween(5, 25),
      passes_decisives: randomBetween(2, 10),
      cartons: randomBetween(1, 4),
      xg: Number((Math.random() * 20 + 5).toFixed(1)),
      xa: Number((Math.random() * 8 + 2).toFixed(1)),
      tirs: randomBetween(40, 120),
      tirs_cadres: randomBetween(35, 65),
      penalty: randomBetween(50, 100),
      courses: randomBetween(100, 200),
      interceptions: randomBetween(5, 20),
      tacles: randomBetween(10, 30),
      aeriens: randomBetween(10, 50),
      pressings: randomBetween(120, 200),
      f_subies: randomBetween(30, 60),
      f_commises: randomBetween(10, 25),
      c_jaunes: randomBetween(1, 3),
      c_rouges: 0,
      dribbles: randomBetween(30, 80),
      p_cles: randomBetween(15, 40),
      p_avant: randomBetween(50, 100),
      centres: randomBetween(15, 50),
    };
  }
}

export function generatePlayerStats(position: string): PlayerStats {
  const isDefender = position === 'Défenseur';
  const isGoalkeeper = position === 'Gardien';
  const isMidfielder = position === 'Milieu';
  const isAttacker = position === 'Attaquant';
  
  return {
    generalData: {
      goals: isGoalkeeper ? 0 : (isDefender ? randomBetween(0, 5) : (isMidfielder ? randomBetween(2, 10) : randomBetween(5, 25))),
      shotActions: isGoalkeeper ? 0 : randomBetween(10, 50),
      assists: isGoalkeeper ? 0 : (isDefender ? randomBetween(0, 4) : (isMidfielder ? randomBetween(3, 12) : randomBetween(2, 10))),
      touches: randomBetween(500, 2500),
      penaltyAreaPasses: isGoalkeeper ? 0 : randomBetween(5, 40),
      finalThirdPasses: randomBetween(10, 100),
      penaltyAreaCrosses: isGoalkeeper ? 0 : randomBetween(5, 30),
      successfulDribbles: isGoalkeeper ? 0 : randomBetween(10, 60)
    },
    possessionData: {
      touches: randomBetween(500, 2500),
      successfulDribbles: isGoalkeeper ? 0 : randomBetween(10, 60),
      successfulPasses: randomBetween(200, 1500),
      progressivePasses: randomBetween(50, 200),
      pressureControls: randomBetween(20, 100),
      progressiveRuns: isGoalkeeper ? 0 : randomBetween(10, 80),
      assists: isGoalkeeper ? 0 : (isDefender ? randomBetween(0, 4) : (isMidfielder ? randomBetween(3, 12) : randomBetween(2, 10))),
      shotActions: isGoalkeeper ? 0 : randomBetween(10, 50)
    },
    performanceData: {
      goals: isGoalkeeper ? 0 : (isDefender ? randomBetween(0, 5) : (isMidfielder ? randomBetween(2, 10) : randomBetween(5, 25))),
      assists: isGoalkeeper ? 0 : (isDefender ? randomBetween(0, 4) : (isMidfielder ? randomBetween(3, 12) : randomBetween(2, 10))),
      nonPenaltyXG: isGoalkeeper ? 0 : Number((Math.random() * 15).toFixed(1)),
      xA: isGoalkeeper ? 0 : Number((Math.random() * 10).toFixed(1)),
      shotActions: isGoalkeeper ? 0 : randomBetween(10, 50),
      defensiveActions: isAttacker ? randomBetween(20, 60) : randomBetween(60, 150),
      nonPenaltyShots: isGoalkeeper ? 0 : randomBetween(10, 80),
      touches: randomBetween(500, 2500)
    },
    defensiveData: {
      defensiveActions: isAttacker ? randomBetween(20, 60) : randomBetween(60, 150),
      successfulTackles: isGoalkeeper ? 0 : (isAttacker ? randomBetween(10, 30) : randomBetween(30, 80)),
      interceptions: isAttacker ? randomBetween(5, 20) : randomBetween(20, 70),
      ballsRecovered: randomBetween(30, 120),
      aerialDuelsWon: randomBetween(10, 60),
      clearances: isAttacker ? randomBetween(0, 10) : randomBetween(10, 50),
      errorsLeadingToShot: randomBetween(0, 3),
      successfulPasses: randomBetween(200, 1500)
    }
  };
}

export function generatePlayers(clubName: string, count: number = 15): PlayerData[] {
  const players: PlayerData[] = [];
  const usedNumbers = new Set<number>();
  const postes = ['Gardien', 'Défenseur', 'Défenseur', 'Défenseur', 'Défenseur', 'Milieu', 'Milieu', 'Milieu', 'Milieu', 'Milieu', 'Attaquant', 'Attaquant', 'Attaquant', 'Défenseur', 'Milieu'];
  
  for (let i = 0; i < count; i++) {
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    
    let numero: number;
    do {
      numero = i === 0 ? 1 : randomBetween(2, 99); // Gardien = 1
    } while (usedNumbers.has(numero));
    usedNumbers.add(numero);
    
    const poste = postes[i];
    const stats = generateStats(poste);
    
    players.push({
      id: `${firstName.toLowerCase()}-${lastName.toLowerCase()}`,
      nom: `${firstName} ${lastName}`,
      poste,
      numero,
      ...stats as PlayerData,
    });
  }
  
  return players.sort((a, b) => {
    const posteOrder = ['Gardien', 'Défenseur', 'Milieu', 'Attaquant'];
    return posteOrder.indexOf(a.poste) - posteOrder.indexOf(b.poste);
  });
}