'use client';

import { PlayerStatistics } from '@/services/sportmonks';
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

interface PlayerStrengthsProps {
  players: PlayerWithStats[];
}

// Configuration des statistiques pour l'analyse
const STATS_CONFIG = [
  { label: 'Minutes jouées', key: 'minutes' },
  { label: 'Apparitions', key: 'appearences' },
  { label: 'Buts', key: 'goals' },
  { label: 'Passes décisives', key: 'assists' },
  { label: 'Buts attendus (xG)', key: 'expected_goals' },
  { label: 'Passes décisives attendues (xA)', key: 'expected_assists' },
  { label: 'Tirs', key: 'shots' },
  { label: 'Tirs cadrés', key: 'shots_on_target' },
  { label: 'Penalties marqués', key: 'penalties_scored' },
  { label: 'Passes réussies', key: 'passes' },
  { label: 'Précision passes (%)', key: 'passes_accuracy' },
  { label: 'Passes clés', key: 'key_passes' },
  { label: 'Centres réussis', key: 'crosses' },
  { label: 'Dribbles réussis', key: 'dribbles_succeeded' },
  { label: 'Touches de balle', key: 'touches' },
  { label: 'Ballons récupérés', key: 'ball_recoveries' },
  { label: 'Tacles', key: 'tackles' },
  { label: 'Interceptions', key: 'interceptions' },
  { label: 'Dégagements', key: 'clearances' },
  { label: 'Tirs bloqués', key: 'blocks' },
  { label: 'Duels gagnés', key: 'duels_won' },
  { label: 'Duels aériens gagnés', key: 'aerial_duels_won' },
  { label: 'Arrêts', key: 'saves' },
  { label: 'Arrêts dans la surface', key: 'inside_box_saves' },
  { label: 'Penalties arrêtés', key: 'penalties_saved' },
  { label: 'Clean sheets', key: 'clean_sheets' },
];

// Stats négatives (moins c'est mieux)
const NEGATIVE_STATS = [
  'yellow_cards', 'red_cards', 'fouls', 'penalties_missed', 
  'dribbles_failed', 'ball_losses', 'goals_conceded', 'offsides',
  'yellowred_cards', 'mistakes_leading_to_goals', 'penalties_committed'
];

export default function PlayerStrengths({ players }: PlayerStrengthsProps) {
  const isNegativeStat = (key: string) => NEGATIVE_STATS.includes(key);

  const getPlayerStrengths = (player: PlayerWithStats) => {
    const strengths: string[] = [];
    
    STATS_CONFIG.forEach(stat => {
      const playerValue = player.stats[stat.key as keyof PlayerStatistics] as number | undefined;
      if (playerValue === undefined || playerValue === null || playerValue === 0) return;
      
      const otherValues = players
        .filter(p => p.id !== player.id)
        .map(p => p.stats[stat.key as keyof PlayerStatistics] as number | undefined)
        .filter(v => v !== undefined && v !== null) as number[];
      
      if (otherValues.length === 0) return;
      
      const isNegative = isNegativeStat(stat.key);
      const maxOther = Math.max(...otherValues);
      const minOther = Math.min(...otherValues);
      
      if (!isNegative && playerValue > maxOther) {
        strengths.push(stat.label);
      } else if (isNegative && playerValue < minOther) {
        strengths.push(stat.label);
      }
    });
    
    return strengths;
  };

  const playersCount = players.length;
  const comparisonText = playersCount === 2 
    ? "Points forts de chaque joueur par rapport à l'autre"
    : "Points forts de chaque joueur par rapport aux autres";

  return (
    <div className="bg-gray-50 rounded-lg p-6 mb-8">
      <h3 className="text-xl font-bold mb-4">{comparisonText}</h3>
      <div className={`grid ${playersCount <= 2 ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-' + Math.min(playersCount, 4)} gap-6`}>
        {players.map((player) => {
          const strengths = getPlayerStrengths(player);
          
          return (
            <div key={player.id} className="bg-white rounded-lg p-4 border border-gray-200">
              <Link 
                href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                className="font-semibold text-gray-900 mb-2 hover:text-blue-600 hover:underline block"
              >
                {player.displayName || player.fullName || player.name}
              </Link>
              <p className="text-sm text-gray-500 mb-3">
                <Link 
                  href={`/${player.leagueSlug}/${player.clubSlug}`}
                  className="hover:text-blue-600 hover:underline"
                >
                  {player.club}
                </Link>
                <span> • {player.position}</span>
              </p>
              {strengths.length > 0 ? (
                <ul className="space-y-1 max-h-48 overflow-y-auto">
                  {strengths.map((strength, index) => (
                    <li key={index} className="text-sm text-green-600 flex items-start">
                      <span className="mr-2 flex-shrink-0">✓</span>
                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-500">Performances équilibrées</p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}