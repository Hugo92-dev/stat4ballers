'use client';

import { PlayerStatistics } from '@/services/sportmonks';

interface StatsCardsProps {
  stats: PlayerStatistics;
  position?: string;
}

// Composant pour afficher une statistique individuelle
function StatItem({ label, value, suffix = '' }: { label: string; value: number | string | undefined | null; suffix?: string }) {
  // Afficher "N/A" pour les valeurs null ou undefined
  const displayValue = value === undefined || value === null 
    ? 'N/A' 
    : typeof value === 'number' 
      ? value.toFixed(value % 1 === 0 ? 0 : 1) 
      : value;
  
  return (
    <div className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
      <span className="text-gray-600 text-sm">{label}</span>
      <span className={`font-semibold ${value === null || value === undefined ? 'text-gray-400' : 'text-gray-900'}`}>
        {displayValue}{value !== null && value !== undefined ? suffix : ''}
      </span>
    </div>
  );
}

// Carte Générale pour joueurs de champ
function GeneralCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🟦 Général</h3>
      <div className="space-y-1">
        <StatItem label="Appearances" value={stats.appearences} />
        <StatItem label="Lineups" value={stats.lineups} />
        <StatItem label="MinutesPlayed" value={stats.minutes} />
        <StatItem label="Captain" value={stats.captain} />
        <StatItem label="Rating" value={stats.rating} />
      </div>
    </div>
  );
}

// Carte Générale pour gardiens
function GeneralCardGoalkeeper({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">📊 Général</h3>
      <div className="space-y-1">
        <StatItem label="Note moyenne" value={stats.rating} />
        <StatItem label="Minutes jouées" value={stats.minutes} />
        <StatItem label="Titularisations" value={stats.lineups} />
        <StatItem label="Matchs joués" value={stats.appearences} />
        <StatItem label="Capitaine" value={stats.captain} />
        <StatItem label="Précision des passes" value={stats.passes_accuracy} suffix="%" />
        <StatItem label="Cartons jaunes" value={stats.yellow_cards} />
        <StatItem label="Cartons rouges" value={stats.red_cards} />
      </div>
    </div>
  );
}

// Carte Offensive
function OffensiveCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🔴 Offensif</h3>
      <div className="space-y-1">
        <StatItem label="Goals" value={stats.goals} />
        <StatItem label="Assists" value={stats.assists} />
        <StatItem label="ShotsTotal" value={stats.shots} />
        <StatItem label="ShotsOnTarget" value={stats.shots_on_target} />
        <StatItem label="HitWoodwork" value={stats.hit_woodwork} />
        <StatItem label="Offsides" value={stats.offsides} />
        <StatItem label="Hattricks" value={stats.hattricks} />
        <StatItem label="BigChancesMissed" value={stats.big_chances_missed} />
      </div>
    </div>
  );
}

// Carte Créative (passes & dribbles)
function CreativeCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🟢 Créatif</h3>
      <div className="space-y-1">
        <StatItem label="Passes" value={stats.passes_total || stats.passes} />
        <StatItem label="AccuratePassesPercentage" value={stats.passes_accuracy} suffix="%" />
        <StatItem label="SuccessfulPassesPercentage" value={stats.passes_accuracy} suffix="%" />
        <StatItem label="KeyPasses" value={stats.key_passes} />
        <StatItem label="BigChancesCreated" value={stats.big_chances_created} />
        <StatItem label="ThroughBalls" value={stats.through_balls} />
        <StatItem label="ThroughBallsWon" value={stats.through_balls_won} />
        <StatItem label="LongBalls" value={stats.long_balls} />
        <StatItem label="LongBallsWon" value={stats.long_balls_won} />
        <StatItem label="TotalCrosses" value={stats.crosses_total || stats.crosses} />
        <StatItem label="AccurateCrosses" value={stats.accurate_crosses} />
      </div>
    </div>
  );
}

// Carte Défensive & Discipline
function DefensiveCard({ stats }: { stats: PlayerStatistics }) {
  const totalRedCards = (stats.red_cards || 0) + (stats.yellowred_cards || 0);
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🛡️ Défensif & Discipline</h3>
      <div className="space-y-1">
        <StatItem label="TotalDuels" value={stats.duels} />
        <StatItem label="DuelsWon" value={stats.duels_won} />
        <StatItem label="AerialsWon" value={stats.aerial_duels_won} />
        <StatItem label="Tackles" value={stats.tackles} />
        <StatItem label="DribbledPast" value={stats.dribbled_past} />
        <StatItem label="ErrorLeadToGoal" value={stats.mistakes_leading_to_goals} />
        <StatItem label="Crosses Blocked" value={stats.crosses_blocked} />
        <StatItem label="Fouls" value={stats.fouls} />
        <StatItem label="FoulsDrawn" value={stats.fouls_drawn} />
        <StatItem label="Yellowcards" value={stats.yellow_cards} />
        <StatItem label="Redcards" value={totalRedCards} />
        <StatItem label="OwnGoals" value={stats.own_goals} />
      </div>
    </div>
  );
}

// Carte Spéciale Gardien
function GoalkeeperCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🧤 Gardien</h3>
      <div className="space-y-1">
        <StatItem label="GoalsConceded" value={stats.goals_conceded} />
        <StatItem label="Saves" value={stats.saves} />
        <StatItem label="SavesInsidebox" value={stats.inside_box_saves} />
      </div>
    </div>
  );
}

export default function StatsCards({ stats, position }: StatsCardsProps) {
  const isGoalkeeper = position?.toLowerCase().includes('gardien') || 
                       position?.toLowerCase().includes('goalkeeper') ||
                       position?.toLowerCase() === 'gk';
  
  // Si pas de stats, afficher un message
  if (!stats || (!stats.minutes && !stats.appearences)) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
        <p className="text-yellow-800">Aucune statistique disponible pour cette saison car le joueur n'a pas encore joué de match officiel</p>
      </div>
    );
  }
  
  // Ordre différent pour les gardiens (seulement 2 cartes)
  if (isGoalkeeper) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GeneralCardGoalkeeper stats={stats} />
        <GoalkeeperCard stats={stats} />
      </div>
    );
  }
  
  // Ordre normal pour les joueurs de champ (4 cartes)
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <GeneralCard stats={stats} />
      <OffensiveCard stats={stats} />
      <CreativeCard stats={stats} />
      <DefensiveCard stats={stats} />
    </div>
  );
}