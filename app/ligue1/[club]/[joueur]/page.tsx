import Link from 'next/link';
import RadarChart from '@/components/RadarChart';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  // Données de test pour Dembélé
  const joueur = {
    nom: 'Ousmane Dembélé',
    poste: 'Attaquant',
    numero: 10,
    age: 27,
    nationalite: '🇫🇷 France',
    taille: '178 cm',
    valeur: '60M €'
  };

  // Stats pour les graphiques radar
  const statsGenerales = [
    { stat: 'Buts', value: 15, fullMark: 30 },
    { stat: 'Passes D.', value: 8, fullMark: 20 },
    { stat: 'Minutes', value: 2500, fullMark: 3500 },
    { stat: 'Titularisations', value: 28, fullMark: 38 },
    { stat: 'Cartons', value: 3, fullMark: 15 },
    { stat: 'Note moyenne', value: 7.2, fullMark: 10 },
  ];

  const statsOffensives = [
    { stat: 'Buts', value: 15, fullMark: 30 },
    { stat: 'xG', value: 12.5, fullMark: 25 },
    { stat: 'Tirs/match', value: 3.2, fullMark: 5 },
    { stat: 'Tirs cadrés %', value: 45, fullMark: 100 },
    { stat: 'Dribbles réussis', value: 65, fullMark: 100 },
    { stat: 'Passes clés', value: 42, fullMark: 80 },
  ];

  const statsDefensives = [
    { stat: 'Tacles', value: 18, fullMark: 50 },
    { stat: 'Interceptions', value: 22, fullMark: 60 },
    { stat: 'Duels aériens %', value: 35, fullMark: 100 },
    { stat: 'Pressings', value: 124, fullMark: 200 },
    { stat: 'Fautes', value: 28, fullMark: 50 },
    { stat: 'Dégagements', value: 8, fullMark: 30 },
  ];

  const statsCreatives = [
    { stat: 'Passes', value: 1420, fullMark: 2000 },
    { stat: 'Précision %', value: 85, fullMark: 100 },
    { stat: 'Passes clés', value: 42, fullMark: 80 },
    { stat: 'Centres réussis', value: 28, fullMark: 50 },
    { stat: 'Passes longues', value: 125, fullMark: 200 },
    { stat: 'Touches/match', value: 58, fullMark: 80 },
  ];

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href={`/ligue1/${params.club}`} className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l'effectif
        </Link>
        
        {/* En-tête du joueur */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold text-blue-900 mb-2">{joueur.nom}</h1>
              <p className="text-xl text-gray-600">{joueur.poste} • #{joueur.numero}</p>
              <div className="flex gap-4 mt-4 text-gray-600">
                <span>{joueur.nationalite}</span>
                <span>{joueur.age} ans</span>
                <span>{joueur.taille}</span>
                <span className="font-semibold text-green-600">{joueur.valeur}</span>
              </div>
            </div>
            <div className="text-6xl font-bold text-gray-200">
              #{joueur.numero}
            </div>
          </div>
        </div>

        {/* Graphiques radar */}
        <div className="grid md:grid-cols-2 gap-8">
          <RadarChart 
            data={statsGenerales} 
            title="📊 Statistiques Générales" 
            color="#1e3a8a"
          />
          <RadarChart 
            data={statsOffensives} 
            title="⚡ Statistiques Offensives" 
            color="#dc2626"
          />
          <RadarChart 
            data={statsDefensives} 
            title="🛡️ Statistiques Défensives" 
            color="#16a34a"
          />
          <RadarChart 
            data={statsCreatives} 
            title="🎯 Statistiques Créatives" 
            color="#9333ea"
          />
        </div>
      </div>
    </main>
  );
}