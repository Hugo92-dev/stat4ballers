import Link from 'next/link';
import CSSRadarChart from '@/components/CSSRadarChart';

export default function VerrattiPage() {
  const generalData = {
    'Nombre de buts marqués': 4,
    'Actions menant à un tir': 28,
    'Passes décisives': 8,
    'Nombre de fois que le joueur touche la balle': 2850,
    'Passes vers la surface de réparation': 52,
    'Passes dans le dernier tiers': 145,
    'Centres dans la surface de réparation': 18,
    'Dribbles réussis': 42
  };

  const possessionData = {
    'Nombre de fois que le joueur touche la balle': 2850,
    'Dribbles réussis': 42,
    'Passes réussies': 1650,
    'Passes progressives': 185,
    'Contrôles du ballon sous pression': 125,
    'Courses progressives': 35,
    'Passes décisives': 8,
    'Actions menant à un tir': 28
  };

  const performanceData = {
    'Nombre de buts marqués': 4,
    'Passes décisives': 8,
    'Buts sans penalty (xG)': 3.2,
    'Passes décisives attendues (xA)': 6.8,
    'Actions menant à un tir': 28,
    'Actions défensives': 95,
    'Tirs non-penalty': 35,
    'Nombre de fois que le joueur touche la balle': 2850
  };

  const defensiveData = {
    'Actions défensives': 95,
    'Tacles réussis': 58,
    'Interceptions': 45,
    'Ballons récupérés': 125,
    'Duels aériens gagnés': 28,
    'Dégagements': 22,
    'Erreurs menant à un tir adverse': 0,
    'Passes réussies': 1650
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
          <h1 className="text-4xl font-bold text-blue-900 mb-2">Marco Verratti</h1>
          <div className="flex items-center gap-4 text-gray-600">
            <span className="text-2xl font-bold">#6</span>
            <span className="text-xl">Milieu</span>
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