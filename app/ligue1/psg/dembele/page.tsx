import Link from 'next/link';
import CSSRadarChart from '@/components/CSSRadarChart';

export default function DembelePage() {
  const joueur = {
    nom: 'Ousmane Dembélé',
    poste: 'Attaquant',
    numero: 10,
    age: 27,
    valeur: 60,
    buts: 8, 
    passes_decisives: 6, 
    ppm: 2.1,
    minutes: 2200, 
    titu: 24, 
    absences: 15, 
    cartons: 3,
    xg: 9.2, 
    xa: 7.8, 
    tirs: 68, 
    tirs_cadres: 42, 
    penalty: 75, 
    courses: 134,
    interceptions: 18, 
    tacles: 22, 
    aeriens: 12, 
    pressings: 156, 
    f_subies: 48, 
    f_commises: 31, 
    c_jaunes: 3, 
    c_rouges: 0,
    touches: 1680, 
    dribbles: 52, 
    passes: 1244, 
    p_cles: 38, 
    p_avant: 98, 
    p_courtes: 87, 
    p_longues: 68, 
    centres: 24
  };

  // Données pour les graphiques radar avec tes libellés
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
        <Link href="/ligue1/psg" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l&apos;effectif PSG
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

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Statistiques de la saison</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-900">{joueur.buts}</div>
              <div className="text-sm text-gray-600 mt-2">Buts marqués</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-900">{joueur.passes_decisives}</div>
              <div className="text-sm text-gray-600 mt-2">Passes décisives</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-3xl font-bold text-yellow-900">{joueur.minutes}</div>
              <div className="text-sm text-gray-600 mt-2">Minutes jouées</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-3xl font-bold text-purple-900">{joueur.titu}</div>
              <div className="text-sm text-gray-600 mt-2">Titularisations</div>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Informations supplémentaires</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>Jours d&apos;absence: {joueur.absences}</div>
              <div>Total cartons: {joueur.cartons}</div>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-8 mt-6">
          <CSSRadarChart data={statsGenerales} title="Statistiques générales" color="#1e3a8a" />
          <CSSRadarChart data={statsOffensives} title="Carte offensive" color="#dc2626" />
          <CSSRadarChart data={statsDefensives} title="Carte défensive" color="#16a34a" />
          <CSSRadarChart data={statsCreatives} title="Carte créative" color="#9333ea" />
        </div>
      </div>
    </main>
  );
}