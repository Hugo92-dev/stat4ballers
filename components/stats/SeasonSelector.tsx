'use client';

import { PlayerStatistics } from '@/services/sportmonks';

interface SeasonSelectorProps {
  current: PlayerStatistics | null;
  previous: PlayerStatistics[];
  cumulative: PlayerStatistics | null;
  selectedSeason: string;
  onSeasonChange: (season: string) => void;
}

export default function SeasonSelector({ 
  current, 
  previous,
  cumulative,
  selectedSeason, 
  onSeasonChange 
}: SeasonSelectorProps) {
  // Créer la liste des saisons disponibles
  const seasons: { id: string; name: string; hasData: boolean; isCumulative?: boolean }[] = [];
  
  // Vue cumulée (toujours en premier)
  if (cumulative) {
    seasons.push({
      id: 'cumulative',
      name: '📊 Total des 3 dernières saisons',
      hasData: true,
      isCumulative: true
    });
  }
  
  // Saison actuelle
  if (current !== null) {
    seasons.push({
      id: 'current',
      name: '2025/2026',
      hasData: true  // On affiche même si 0 match (c'est une info valide)
    });
  }
  
  // Saisons précédentes
  const previousSeasonNames = ['2024/2025', '2023/2024'];
  previous.forEach((season, index) => {
    if (season !== null) {
      seasons.push({
        id: `previous-${index}`,
        name: season.season_name || previousSeasonNames[index] || `Saison ${index + 1}`,
        hasData: true  // Toujours afficher les saisons précédentes même avec 0 match
      });
    }
  });
  
  return (
    <div className="mb-6">
      <div className="flex flex-wrap gap-2">
        {seasons.map((season) => (
          <button
            key={season.id}
            onClick={() => onSeasonChange(season.id)}
            className={`
              px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${selectedSeason === season.id 
                ? season.isCumulative 
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-md' 
                  : 'bg-blue-600 text-white shadow-md'
                : season.hasData
                  ? season.isCumulative
                    ? 'bg-gradient-to-r from-purple-100 to-blue-100 text-gray-700 hover:from-purple-200 hover:to-blue-200'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  : 'bg-gray-50 text-gray-400 cursor-not-allowed'
              }
            `}
            disabled={!season.hasData}
          >
            {season.name}
            {!season.hasData && !season.isCumulative && ' (Pas de données)'}
          </button>
        ))}
      </div>
      {selectedSeason === 'cumulative' && (
        <p className="text-xs text-gray-500 mt-2">
          📈 Statistiques cumulées des saisons 2023/2024, 2024/2025 et 2025/2026
        </p>
      )}
    </div>
  );
}