'use client';

import { PlayerStatistics } from '@/services/sportmonks';
import PlayerStrengths from './PlayerStrengths';
import Link from 'next/link';

interface Player {
  id: number;
  name: string;
  fullName?: string;
  displayName?: string;
  position: string;
  club: string;
  league: string;
  clubSlug: string;
  leagueSlug: string;
  playerSlug: string;
  image?: string;
}

interface PlayerWithStats extends Player {
  stats: PlayerStatistics;
}

interface PlayerComparisonListProps {
  players: PlayerWithStats[];
}

// Fonction pour obtenir la classe de couleur selon la comparaison
const getValueClass = (value: number | undefined, otherValues: (number | undefined)[], higherIsBetter: boolean = true) => {
  if (value === undefined || value === null) return 'text-gray-400';
  
  const validOtherValues = otherValues.filter(v => v !== undefined && v !== null) as number[];
  if (validOtherValues.length === 0) return 'text-gray-900';
  
  const maxValue = Math.max(...validOtherValues, value);
  const minValue = Math.min(...validOtherValues, value);
  
  if (value === maxValue && value === minValue) return 'text-gray-900'; // Tous égaux
  
  if (higherIsBetter) {
    if (value === maxValue) return 'text-green-600 font-semibold';
    if (value === minValue) return 'text-red-600';
  } else {
    // Pour les stats négatives (cartons, fautes, etc.)
    if (value === minValue) return 'text-green-600 font-semibold';
    if (value === maxValue) return 'text-red-600';
  }
  
  return 'text-gray-900';
};

export default function PlayerComparisonList({ players }: PlayerComparisonListProps) {
  const hasGoalkeeper = players.some(p => 
    p.position?.toLowerCase().includes('gardien') || 
    p.position?.toLowerCase().includes('goalkeeper') ||
    p.position?.toLowerCase() === 'gk'
  );

  // Composant pour une ligne de comparaison
  const ComparisonRow = ({ 
    label, 
    values, 
    suffix = '', 
    isNegative = false,
    formatter = (v: number) => v.toFixed(v % 1 === 0 ? 0 : 1)
  }: { 
    label: string; 
    values: (number | undefined)[];
    suffix?: string;
    isNegative?: boolean;
    formatter?: (v: number) => string;
  }) => {
    return (
      <tr className="hover:bg-gray-50">
        <td className="py-3 px-4 font-medium text-gray-700 border-b">{label}</td>
        {values.map((value, index) => {
          const otherValues = values.filter((_, i) => i !== index);
          const valueClass = getValueClass(value, otherValues, !isNegative);
          return (
            <td key={index} className={`py-3 px-4 text-center border-b ${valueClass}`}>
              {value !== undefined && value !== null ? `${formatter(value)}${suffix}` : '-'}
            </td>
          );
        })}
      </tr>
    );
  };

  // CARTE GÉNÉRALE
  const GeneralCard = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">⚽ Carte Générale</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <div className="flex flex-col items-center gap-2">
                      {player.image ? (
                        <img
                          src={player.image}
                          alt={player.displayName || player.fullName || player.name}
                          className="w-10 h-10 rounded-full object-cover border-2 border-gray-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : null}
                      <Link 
                        href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                        className="hover:text-blue-600 hover:underline text-sm"
                      >
                        {player.displayName || player.fullName || player.name}
                      </Link>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Matchs joués" values={players.map(p => p.stats.appearences)} />
              <ComparisonRow label="Titularisations" values={players.map(p => p.stats.lineups)} />
              <ComparisonRow label="Minutes jouées" values={players.map(p => p.stats.minutes)} />
              <ComparisonRow label="Capitaine" values={players.map(p => p.stats.captain)} />
              <ComparisonRow label="Note moyenne" values={players.map(p => p.stats.rating)} />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE GÉNÉRALE POUR GARDIENS
  const GeneralCardGoalkeeper = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">📊 Général</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <div className="flex flex-col items-center gap-2">
                      {player.image ? (
                        <img
                          src={player.image}
                          alt={player.displayName || player.fullName || player.name}
                          className="w-10 h-10 rounded-full object-cover border-2 border-gray-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : null}
                      <Link 
                        href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                        className="hover:text-blue-600 hover:underline text-sm"
                      >
                        {player.displayName || player.fullName || player.name}
                      </Link>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Note moyenne" values={players.map(p => p.stats.rating)} />
              <ComparisonRow label="Minutes jouées" values={players.map(p => p.stats.minutes)} />
              <ComparisonRow label="Titularisations" values={players.map(p => p.stats.lineups)} />
              <ComparisonRow label="Matchs joués" values={players.map(p => p.stats.appearences)} />
              <ComparisonRow label="Capitaine" values={players.map(p => p.stats.captain)} />
              <ComparisonRow label="Précision des passes" values={players.map(p => p.stats.passes_accuracy)} suffix="%" />
              <ComparisonRow label="Cartons jaunes" values={players.map(p => p.stats.yellow_cards)} isNegative />
              <ComparisonRow label="Cartons rouges" values={players.map(p => (p.stats.red_cards || 0) + (p.stats.yellowred_cards || 0))} isNegative />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE OFFENSIVE
  const OffensiveCard = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">⚔️ Carte Offensive</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <div className="flex flex-col items-center gap-2">
                      {player.image ? (
                        <img
                          src={player.image}
                          alt={player.displayName || player.fullName || player.name}
                          className="w-10 h-10 rounded-full object-cover border-2 border-gray-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : null}
                      <Link 
                        href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                        className="hover:text-blue-600 hover:underline text-sm"
                      >
                        {player.displayName || player.fullName || player.name}
                      </Link>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Buts" values={players.map(p => p.stats.goals)} />
              <ComparisonRow label="Passes décisives" values={players.map(p => p.stats.assists)} />
              <ComparisonRow label="Tirs tentés" values={players.map(p => p.stats.shots)} />
              <ComparisonRow label="Tirs cadrés" values={players.map(p => p.stats.shots_on_target)} />
              <ComparisonRow label="Tirs sur les montants" values={players.map(p => p.stats.hit_woodwork)} />
              <ComparisonRow label="Hors-jeu" values={players.map(p => p.stats.offsides)} isNegative />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE CRÉATIVE
  const CreativeCard = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🧑‍🎨 Carte Créative</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <div className="flex flex-col items-center gap-2">
                      {player.image ? (
                        <img
                          src={player.image}
                          alt={player.displayName || player.fullName || player.name}
                          className="w-10 h-10 rounded-full object-cover border-2 border-gray-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : null}
                      <Link 
                        href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                        className="hover:text-blue-600 hover:underline text-sm"
                      >
                        {player.displayName || player.fullName || player.name}
                      </Link>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Passes" values={players.map(p => p.stats.passes_total || p.stats.passes)} />
              <ComparisonRow label="Précision des passes" values={players.map(p => p.stats.passes_accuracy)} suffix="%" />
              <ComparisonRow label="Passes clés" values={players.map(p => p.stats.key_passes)} />
              <ComparisonRow label="Centres" values={players.map(p => p.stats.crosses_total || p.stats.crosses)} />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE DÉFENSIVE & DISCIPLINE
  const DefensiveCard = () => {
    const totalRedCards = players.map(p => (p.stats.red_cards || 0) + (p.stats.yellowred_cards || 0));
    
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🛡️ Carte Défensive & Discipline</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <div className="flex flex-col items-center gap-2">
                      {player.image ? (
                        <img
                          src={player.image}
                          alt={player.displayName || player.fullName || player.name}
                          className="w-10 h-10 rounded-full object-cover border-2 border-gray-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : null}
                      <Link 
                        href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                        className="hover:text-blue-600 hover:underline text-sm"
                      >
                        {player.displayName || player.fullName || player.name}
                      </Link>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Duels totaux" values={players.map(p => p.stats.duels)} />
              <ComparisonRow label="Duels gagnés" values={players.map(p => p.stats.duels_won)} />
              <ComparisonRow label="Duels aériens gagnés" values={players.map(p => p.stats.aerial_duels_won)} />
              <ComparisonRow label="Tacles" values={players.map(p => p.stats.tackles)} />
              <ComparisonRow label="Fautes commises" values={players.map(p => p.stats.fouls)} isNegative />
              <ComparisonRow label="Fautes subies" values={players.map(p => p.stats.fouls_drawn)} />
              <ComparisonRow label="Cartons jaunes" values={players.map(p => p.stats.yellow_cards)} isNegative />
              <ComparisonRow label="Cartons rouges" values={totalRedCards} isNegative />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE GARDIEN
  const GoalkeeperCard = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🧤 Carte Gardien</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <div className="flex flex-col items-center gap-2">
                      {player.image ? (
                        <img
                          src={player.image}
                          alt={player.displayName || player.fullName || player.name}
                          className="w-10 h-10 rounded-full object-cover border-2 border-gray-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : null}
                      <Link 
                        href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                        className="hover:text-blue-600 hover:underline text-sm"
                      >
                        {player.displayName || player.fullName || player.name}
                      </Link>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Buts encaissés" values={players.map(p => p.stats.goals_conceded)} isNegative />
              <ComparisonRow label="Arrêts" values={players.map(p => p.stats.saves)} />
              <ComparisonRow label="Arrêts dans la surface" values={players.map(p => p.stats.inside_box_saves)} />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Points forts en haut */}
      <PlayerStrengths players={players} />
      
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold mb-2">Comparaison Détaillée</h2>
        <p className="text-gray-600">
          Les valeurs en <span className="text-green-600 font-semibold">vert</span> sont les meilleures, 
          en <span className="text-red-600">rouge</span> les moins bonnes
        </p>
      </div>

      {/* Cartes de comparaison */}
      <div className="space-y-6">
        {hasGoalkeeper ? (
          <>
            <GeneralCardGoalkeeper />
            <GoalkeeperCard />
          </>
        ) : (
          <>
            <GeneralCard />
            <OffensiveCard />
            <CreativeCard />
            <DefensiveCard />
          </>
        )}
      </div>
    </div>
  );
}