import Link from 'next/link';
import RadarChart from '@/components/RadarChart';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  // Base de données des joueurs avec stats réalistes
  const joueursData: { [key: string]: any } = {
    'dembele': {
      nom: 'Ousmane Dembélé',
      poste: 'Attaquant',
      numero: 10,
      age: 27,
      valeur: 60,
      // Stats réelles approximatives
      buts: 8, passes_decisives: 6, ppm: 2.1, minutes: 2200, titu: 24, absences: 15, cartons: 3,
      xg: 9.2, xa: 7.8, tirs: 68, tirs_cadres: 42, penalty: 75, courses: 134,
      interceptions: 18, tacles: 22, aeriens: 12, pressings: 156, f_subies: 48, f_commises: 31, c_jaunes: 3, c_rouges: 0,
      touches: 1680, dribbles: 52, passes: 1244, p_cles: 38, p_avant: 98, p_courtes: 87, p_longues: 68, centres: 24
    },
    'zaire-emery': {
      nom: 'Warren Zaïre-Emery',
      poste: 'Milieu',
      numero: 33,
      age: 18,
      valeur: 50,
      buts: 4, passes_decisives: 6, ppm: 2.2, minutes: 2100, titu: 22, absences: 5, cartons: 4,
      xg: 3.8, xa: 5.2, tirs: 32, tirs_cadres: 38, penalty: 0, courses: 112,
      interceptions: 42, tacles: 38, aeriens: 28, pressings: 178, f_subies: 36, f_commises: 28, c_jaunes: 4, c_rouges: 0,
      touches: 1920, dribbles: 28, passes: 1456, p_cles: 42, p_avant: 124, p_courtes: 91, p_longues: 72, centres: 12
    },
    'hakimi': {
      nom: 'Achraf Hakimi',
      poste: 'Défenseur',
      numero: 2,
      age: 26,
      valeur: 65,
      buts: 4, passes_decisives: 7, ppm: 2.1, minutes: 2500, titu: 28, absences: 0, cartons: 5,
      xg: 3.2, xa: 5.8, tirs: 32, tirs_cadres: 38, penalty: 0, courses: 186,
      interceptions: 48, tacles: 62, aeriens: 31, pressings: 124, f_subies: 28, f_commises: 22, c_jaunes: 5, c_rouges: 0,
      touches: 1850, dribbles: 38, passes: 1380, p_cles: 35, p_avant: 86, p_courtes: 85, p_longues: 71, centres: 42
    }
  };

  // Joueur par défaut si pas trouvé
  const defaultJoueur = {
    nom: 'Joueur',
    poste: 'N/A',
    numero: 0,
    age: 0,
    valeur: 0,
    buts: 0, passes_decisives: 0, ppm: 0, minutes: 0, titu: 0, absences: 0, cartons: 0,
    xg: 0, xa: 0, tirs: 0, tirs_cadres: 0, penalty: 0, courses: 0,
    interceptions: 0, tacles: 0, aeriens: 0, pressings: 0, f_subies: 0, f_commises: 0, c_jaunes: 0, c_rouges: 0,
    touches: 0, dribbles: 0, passes: 0, p_cles: 0, p_avant: 0, p_courtes: 0, p_longues: 0, centres: 0
  };

  const joueur = joueursData[params.joueur] || defaultJoueur;

  // Construction des graphiques avec les vraies données
  const statsGenerales = [
    { stat: 'Buts', value: joueur.buts, fullMark: 30 },
    { stat: 'Passes décisives', value: joueur.passes_decisives, fullMark: 20 },
    { stat: 'Points gagnés par match (quand le joueur joue)', value: joueur.ppm, fullMark: 3 },
    { stat: 'Minutes jouées', value: joueur.minutes, fullMark: 3500 },
    { stat: 'Nombre de titularisation', value: joueur.titu, fullMark: 38 },
    { stat: 'Nombre de jours absents/suspendus/blessés', value: joueur.absences, fullMark: 100 },
    { stat: 'Valeur marchande', value: joueur.valeur, fullMark: 200 },
    { stat: 'Cartons (jaune + rouge)', value: joueur.cartons, fullMark: 15 },
  ];

  const statsOffensives = [
    { stat: 'Buts', value: joueur.buts, fullMark: 30 },
    { stat: 'xG (expected goals)', value: joueur.xg, fullMark: 25 },
    { stat: 'Passes décisives', value: joueur.passes_decisives, fullMark: 20 },
    { stat: 'xA (expected assists)', value: joueur.xa, fullMark: 15 },
    { stat: 'Total tirs', value: joueur.tirs, fullMark: 120 },
    { stat: 'Tirs cadrés (%)', value: joueur.tirs_cadres, fullMark: 100 },
    { stat: 'Ratio penalty marqué', value: joueur.penalty, fullMark: 100 },
    { stat: 'Courses vers l\'avant', value: joueur.courses, fullMark: 200 },
  ];

  const statsDefensives = [
    { stat: 'Interceptions', value: joueur.interceptions, fullMark: 60 },
    { stat: 'Tacles réussis', value: joueur.tacles, fullMark: 50 },
    { stat: 'Duels aériens gagnés', value: joueur.aeriens, fullMark: 100 },
    { stat: 'Pressings réussis', value: joueur.pressings, fullMark: 200 },
    { stat: 'Fautes subies', value: joueur.f_subies, fullMark: 80 },
    { stat: 'Fautes commises', value: joueur.f_commises, fullMark: 50 },
    { stat: 'Cartons jaunes', value: joueur.c_jaunes, fullMark: 10 },
    { stat: 'Cartons rouges', value: joueur.c_rouges, fullMark: 3 },
  ];

  const statsCreatives = [
    { stat: 'Nombre de fois que le joueur touche la balle', value: joueur.touches, fullMark: 2500 },
    { stat: 'Dribbles réussis', value: joueur.dribbles, fullMark: 80 },
    { stat: 'Total passes', value: joueur.passes, fullMark: 2000 },
    { stat: 'Passes clés', value: joueur.p_cles, fullMark: 80 },
    { stat: 'Passes vers l\'avant', value: joueur.p_avant, fullMark: 150 },
    { stat: 'Passes courtes réussies (%)', value: joueur.p_courtes, fullMark: 100 },
    { stat: 'Passes longues réussies (%)', value: joueur.p_longues, fullMark: 100 },
    { stat: 'Centres réussis', value: joueur.centres, fullMark: 50 },
  ];

  return (
    <main className="min-h-screen bg-gray-50 py-4 md:py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        <Link href={`/ligue1/${params.club}`} className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l'effectif
        </Link>
        
        <div className="bg-white rounded-lg shadow-md p-4 md:p-8 mb-6">
          <div className="flex flex-col md:flex-row justify-between items-start">
            <div>
              <h1 className="text-2xl md:text-4xl font-bold text-blue-900 mb-2">{joueur.nom}</h1>
              <p className="text-lg md:text-xl text-gray-600">{joueur.poste} • #{joueur.numero}</p>
              <div className="flex flex-wrap gap-2 md:gap-4 mt-4 text-sm md:text-base text-gray-600">
                <span>{joueur.age} ans</span>
                <span className="font-semibold text-green-600">{joueur.valeur}M €</span>
              </div>
            </div>
            <div className="text-4xl md:text-6xl font-bold text-gray-200 mt-4 md:mt-0">
              #{joueur.numero}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-8">
          <RadarChart data={statsGenerales} title="Statistiques générales" color="#1e3a8a" />
          <RadarChart data={statsOffensives} title="Carte offensive" color="#dc2626" />
          <RadarChart data={statsDefensives} title="Carte défensive" color="#16a34a" />
          <RadarChart data={statsCreatives} title="Carte créative" color="#9333ea" />
        </div>
      </div>
    </main>
  );
}