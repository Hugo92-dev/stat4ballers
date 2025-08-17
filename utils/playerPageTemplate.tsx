import Link from 'next/link';
import CSSRadarChart from '@/components/CSSRadarChart';
import { generatePlayerStats } from '@/utils/playerGenerator';

interface PlayerPageProps {
  championshipPath: string;
  championshipName: string;
  clubPath: string;
  clubName: string;
  playerName: string;
  playerNumber: number;
  playerPosition: string;
}

export function createPlayerPage({
  championshipPath,
  championshipName,
  clubPath,
  clubName,
  playerName,
  playerNumber,
  playerPosition
}: PlayerPageProps) {
  const stats = generatePlayerStats(playerPosition);
  
  return `import Link from 'next/link';
import CSSRadarChart from '@/components/CSSRadarChart';

export default function PlayerPage() {
  const generalData = {
    'Nombre de buts marqués': ${stats.generalData.goals},
    'Actions menant à un tir': ${stats.generalData.shotActions},
    'Passes décisives': ${stats.generalData.assists},
    'Nombre de fois que le joueur touche la balle': ${stats.generalData.touches},
    'Passes vers la surface de réparation': ${stats.generalData.penaltyAreaPasses},
    'Passes dans le dernier tiers': ${stats.generalData.finalThirdPasses},
    'Centres dans la surface de réparation': ${stats.generalData.penaltyAreaCrosses},
    'Dribbles réussis': ${stats.generalData.successfulDribbles}
  };

  const possessionData = {
    'Nombre de fois que le joueur touche la balle': ${stats.possessionData.touches},
    'Dribbles réussis': ${stats.possessionData.successfulDribbles},
    'Passes réussies': ${stats.possessionData.successfulPasses},
    'Passes progressives': ${stats.possessionData.progressivePasses},
    'Contrôles du ballon sous pression': ${stats.possessionData.pressureControls},
    'Courses progressives': ${stats.possessionData.progressiveRuns},
    'Passes décisives': ${stats.possessionData.assists},
    'Actions menant à un tir': ${stats.possessionData.shotActions}
  };

  const performanceData = {
    'Nombre de buts marqués': ${stats.performanceData.goals},
    'Passes décisives': ${stats.performanceData.assists},
    'Buts sans penalty (xG)': ${stats.performanceData.nonPenaltyXG},
    'Passes décisives attendues (xA)': ${stats.performanceData.xA},
    'Actions menant à un tir': ${stats.performanceData.shotActions},
    'Actions défensives': ${stats.performanceData.defensiveActions},
    'Tirs non-penalty': ${stats.performanceData.nonPenaltyShots},
    'Nombre de fois que le joueur touche la balle': ${stats.performanceData.touches}
  };

  const defensiveData = {
    'Actions défensives': ${stats.defensiveData.defensiveActions},
    'Tacles réussis': ${stats.defensiveData.successfulTackles},
    'Interceptions': ${stats.defensiveData.interceptions},
    'Ballons récupérés': ${stats.defensiveData.ballsRecovered},
    'Duels aériens gagnés': ${stats.defensiveData.aerialDuelsWon},
    'Dégagements': ${stats.defensiveData.clearances},
    'Erreurs menant à un tir adverse': ${stats.defensiveData.errorsLeadingToShot},
    'Passes réussies': ${stats.defensiveData.successfulPasses}
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-6">
          <Link href="/${championshipPath}" className="text-blue-900 hover:underline">
            ${championshipName}
          </Link>
          <span className="mx-2 text-gray-500">/</span>
          <Link href="/${championshipPath}/${clubPath}" className="text-blue-900 hover:underline">
            ${clubName}
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h1 className="text-4xl font-bold text-blue-900 mb-2">${playerName}</h1>
          <div className="flex items-center gap-4 text-gray-600">
            <span className="text-2xl font-bold">#{playerNumber}</span>
            <span className="text-xl">${playerPosition}</span>
            <span className="text-xl">${clubName}</span>
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
}`;
}