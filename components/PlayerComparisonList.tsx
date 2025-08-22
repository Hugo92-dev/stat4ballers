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
    const shotsAccuracies = players.map(p => 
      p.stats.shots && p.stats.shots > 0 
        ? ((p.stats.shots_on_target || 0) / p.stats.shots * 100) 
        : undefined
    );

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
                    <Link 
                      href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                      className="hover:text-blue-600 hover:underline"
                    >
                      {player.displayName || player.fullName || player.name}
                    </Link>
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
              {!hasGoalkeeper && (
                <>
                  <ComparisonRow label="Touches de balle" values={players.map(p => p.stats.touches)} />
                  <ComparisonRow label="Précision des tirs" values={shotsAccuracies} suffix="%" />
                </>
              )}
              <ComparisonRow label="Précision des passes" values={players.map(p => p.stats.passes_accuracy)} suffix="%" />
              {hasGoalkeeper && (
                <>
                  <ComparisonRow label="Cartons jaunes" values={players.map(p => p.stats.yellow_cards)} isNegative />
                  <ComparisonRow label="Cartons rouges" values={players.map(p => p.stats.red_cards)} isNegative />
                </>
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE OFFENSIVE
  const OffensiveCard = () => {
    const penaltyAccuracies = players.map(p => 
      p.stats.penalties && p.stats.penalties > 0 
        ? ((p.stats.penalties_scored || 0) / p.stats.penalties * 100) 
        : undefined
    );

    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">⚽ Offensif</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <Link 
                      href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                      className="hover:text-blue-600 hover:underline"
                    >
                      {player.displayName || player.fullName || player.name}
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Buts marqués" values={players.map(p => p.stats.goals)} />
              <ComparisonRow label="Expected Goals (xG)" values={players.map(p => p.stats.expected_goals)} />
              <ComparisonRow label="Passes décisives" values={players.map(p => p.stats.assists)} />
              <ComparisonRow label="Expected Assists (xA)" values={players.map(p => p.stats.expected_assists)} />
              <ComparisonRow label="Total tirs" values={players.map(p => p.stats.shots)} />
              <ComparisonRow label="Total penalties" values={players.map(p => p.stats.penalties)} />
              <ComparisonRow label="Précision des penalties" values={penaltyAccuracies} suffix="%" />
              <ComparisonRow label="Poteaux+barres" values={players.map(p => p.stats.hit_woodwork)} />
              <ComparisonRow label="Hors-jeux" values={players.map(p => p.stats.offsides)} isNegative />
              <ComparisonRow label="Pertes de balle" values={players.map(p => p.stats.ball_losses)} isNegative />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE CRÉATIVE
  const CreativeCard = () => {
    const dribbleAccuracies = players.map(p => 
      p.stats.dribbles && p.stats.dribbles > 0
        ? ((p.stats.dribbles_succeeded || 0) / p.stats.dribbles * 100)
        : undefined
    );

    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🎯 Créatif (passes & dribbles)</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <Link 
                      href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                      className="hover:text-blue-600 hover:underline"
                    >
                      {player.displayName || player.fullName || player.name}
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Total passes" values={players.map(p => p.stats.passes_total)} />
              <ComparisonRow label="Passes clés" values={players.map(p => p.stats.key_passes)} />
              <ComparisonRow label="Total centres" values={players.map(p => p.stats.crosses_total)} />
              <ComparisonRow label="Précision centres" values={players.map(p => p.stats.crosses_accuracy)} suffix="%" />
              <ComparisonRow label="Total dribbles" values={players.map(p => p.stats.dribbles)} />
              <ComparisonRow label="Précision dribbles" values={dribbleAccuracies} suffix="%" />
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // CARTE DÉFENSIVE & DISCIPLINE
  const DefensiveCard = () => {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🛡️ Défensif & Discipline</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <Link 
                      href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                      className="hover:text-blue-600 hover:underline"
                    >
                      {player.displayName || player.fullName || player.name}
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Récupérations" values={players.map(p => p.stats.ball_recoveries)} />
              <ComparisonRow label="Tacles" values={players.map(p => p.stats.tackles)} />
              <ComparisonRow label="Interceptions" values={players.map(p => p.stats.interceptions)} />
              <ComparisonRow label="Total duels" values={players.map(p => p.stats.duels)} />
              <ComparisonRow label="Duels gagnés" values={players.map(p => p.stats.duels_won)} />
              <ComparisonRow label="Duels aériens" values={players.map(p => p.stats.aerial_duels)} />
              <ComparisonRow label="Aériens gagnés" values={players.map(p => p.stats.aerial_duels_won)} />
              <ComparisonRow label="Fautes commises" values={players.map(p => p.stats.fouls)} isNegative />
              <ComparisonRow label="Fautes subies" values={players.map(p => p.stats.fouls_drawn)} />
              <ComparisonRow label="Cartons jaunes" values={players.map(p => p.stats.yellow_cards)} isNegative />
              <ComparisonRow label="Cartons rouges" values={players.map(p => p.stats.red_cards)} isNegative />
              <ComparisonRow label="Penalties concédés" values={players.map(p => p.stats.penalties_committed)} isNegative />
              <ComparisonRow label="Erreurs→but" values={players.map(p => p.stats.mistakes_leading_to_goals)} isNegative />
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
        <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🥅 Gardien</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="text-left py-3 px-4 font-medium text-gray-700 border-b">Statistique</th>
                {players.map((player) => (
                  <th key={player.id} className="text-center py-3 px-4 font-medium text-gray-900 border-b">
                    <Link 
                      href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                      className="hover:text-blue-600 hover:underline"
                    >
                      {player.displayName || player.fullName || player.name}
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <ComparisonRow label="Arrêts" values={players.map(p => p.stats.saves)} />
              <ComparisonRow label="Arrêts dans la surface" values={players.map(p => p.stats.inside_box_saves)} />
              <ComparisonRow label="Penalties arrêtés" values={players.map(p => p.stats.penalties_saved)} />
              <ComparisonRow label="Clean sheets" values={players.map(p => p.stats.clean_sheets)} />
              <ComparisonRow label="Buts encaissés" values={players.map(p => p.stats.goals_conceded)} isNegative />
              <ComparisonRow label="Penalties concédés" values={players.map(p => p.stats.penalties_committed)} isNegative />
              <ComparisonRow label="Erreurs→but" values={players.map(p => p.stats.mistakes_leading_to_goals)} isNegative />
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
        <GeneralCard />
        
        {!hasGoalkeeper && (
          <>
            <OffensiveCard />
            <CreativeCard />
            <DefensiveCard />
          </>
        )}
        
        {hasGoalkeeper && (
          <GoalkeeperCard />
        )}
      </div>
    </div>
  );
}