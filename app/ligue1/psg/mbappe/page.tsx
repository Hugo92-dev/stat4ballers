import Link from 'next/link';
import CSSRadarChart from '@/components/CSSRadarChart';

export default function MbappePage() {
  const generalData = {
    'Nombre de buts marqués': 35,
    'Actions menant à un tir': 42,
    'Passes décisives': 10,
    'Nombre de fois que le joueur touche la balle': 2150,
    'Passes vers la surface de réparation': 38,
    'Passes dans le dernier tiers': 85,
    'Centres dans la surface de réparation': 25,
    'Dribbles réussis': 68
  };

  const possessionData = {
    'Nombre de fois que le joueur touche la balle': 2150,
    'Dribbles réussis': 68,
    'Passes réussies': 890,
    'Passes progressives': 125,
    'Contrôles du ballon sous pression': 92,
    'Courses progressives': 78,
    'Passes décisives': 10,
    'Actions menant à un tir': 42
  };

  const performanceData = {
    'Nombre de buts marqués': 35,
    'Passes décisives': 10,
    'Buts sans penalty (xG)': 28.5,
    'Passes décisives attendues (xA)': 8.2,
    'Actions menant à un tir': 42,
    'Actions défensives': 35,
    'Tirs non-penalty': 95,
    'Nombre de fois que le joueur touche la balle': 2150
  };

  const defensiveData = {
    'Actions défensives': 35,
    'Tacles réussis': 18,
    'Interceptions': 12,
    'Ballons récupérés': 85,
    'Duels aériens gagnés': 22,
    'Dégagements': 5,
    'Erreurs menant à un tir adverse': 1,
    'Passes réussies': 890
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-6">
          <Link href="/ligue1" className="text-blue-900 hover:underline">
            Ligue 1
          </Link>
          <span className="mx-2 text-gray-500">/</span>
          <Link href="/ligue1/psg" className="text-blue-900 hover:underline">
            PSG
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h1 className="text-4xl font-bold text-blue-900 mb-2">Kylian Mbappé</h1>
          <div className="flex items-center gap-4 text-gray-600">
            <span className="text-2xl font-bold">#7</span>
            <span className="text-xl">Attaquant</span>
            <span className="text-xl">PSG</span>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">Statistiques Générales</h2>
            <CSSRadarChart data={generalData} />
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">Possession</h2>
            <CSSRadarChart data={possessionData} />
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">Performance</h2>
            <CSSRadarChart data={performanceData} />
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-blue-900 mb-4">Défense</h2>
            <CSSRadarChart data={defensiveData} />
          </div>
        </div>
      </div>
    </main>
  );
}