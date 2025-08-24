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
  // Calculer la précision des tirs
  const shotsAccuracy = stats.shots && stats.shots > 0 && stats.shots_on_target !== null && stats.shots_on_target !== undefined
    ? ((stats.shots_on_target || 0) / stats.shots * 100) 
    : null;
    
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">📊 Général</h3>
      <div className="space-y-1">
        <StatItem label="Note moyenne" value={stats.rating} />
        <StatItem label="Minutes jouées" value={stats.minutes} />
        <StatItem label="Titularisations" value={stats.lineups} />
        <StatItem label="Matchs joués" value={stats.appearences} />
        <StatItem label="Capitaine" value={stats.captain} />
        <StatItem label="Touches de balle" value={stats.touches} />
        <StatItem label="Précision des tirs" value={shotsAccuracy} suffix="%" />
        <StatItem label="Précision des passes" value={stats.passes_accuracy} suffix="%" />
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
  const penaltyAccuracy = stats.penalties && stats.penalties > 0 && stats.penalties_scored !== null && stats.penalties_scored !== undefined
    ? ((stats.penalties_scored || 0) / stats.penalties * 100) 
    : null;
    
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">⚽ Offensif</h3>
      <div className="space-y-1">
        <StatItem label="Buts marqués" value={stats.goals} />
        <StatItem label="Expected Goals (xG)" value={stats.expected_goals} />
        <StatItem label="Passes décisives" value={stats.assists} />
        <StatItem label="Expected Assists (xA)" value={stats.expected_assists} />
        <StatItem label="Total tirs" value={stats.shots} />
        <StatItem label="Total penalties" value={stats.penalties} />
        <StatItem label="Précision des penalties" value={penaltyAccuracy} suffix="%" />
        <StatItem label="Poteaux+barres" value={stats.hit_woodwork} />
        <StatItem label="Hors-jeux" value={stats.offsides} />
        <StatItem label="Pertes de balle" value={stats.ball_losses} />
      </div>
    </div>
  );
}

// Carte Créative (passes & dribbles)
function CreativeCard({ stats }: { stats: PlayerStatistics }) {
  const dribbleAccuracy = stats.dribbles && stats.dribbles > 0 && stats.dribbles_succeeded !== null && stats.dribbles_succeeded !== undefined
    ? ((stats.dribbles_succeeded || 0) / stats.dribbles * 100)
    : null;
    
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🎯 Créatif</h3>
      <div className="space-y-1">
        <StatItem label="Total passes" value={stats.passes_total || stats.passes} />
        <StatItem label="Passes clés" value={stats.key_passes} />
        <StatItem label="Total centres" value={stats.crosses_total || stats.crosses} />
        <StatItem label="Précision des centres" value={stats.crosses_accuracy} suffix="%" />
        <StatItem label="Total dribbles" value={stats.dribbles} />
        <StatItem label="Précision des dribbles" value={dribbleAccuracy} suffix="%" />
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
        <StatItem label="Récupérations" value={stats.ball_recoveries} />
        <StatItem label="Tacles" value={stats.tackles} />
        <StatItem label="Interceptions" value={stats.interceptions} />
        <StatItem label="Total duels" value={stats.duels} />
        <StatItem label="Duels gagnés" value={stats.duels_won} />
        <StatItem label="Total duels aériens" value={stats.aerial_duels} />
        <StatItem label="Duels aériens gagnés" value={stats.aerial_duels_won} />
        <StatItem label="Fautes commises" value={stats.fouls} />
        <StatItem label="Fautes subies" value={stats.fouls_drawn} />
        <StatItem label="Cartons jaunes" value={stats.yellow_cards} />
        <StatItem label="Cartons rouges" value={totalRedCards} />
        <StatItem label="Penalties concédés" value={stats.penalties_committed} />
        <StatItem label="Erreurs entraînant un but" value={stats.mistakes_leading_to_goals} />
      </div>
    </div>
  );
}

// Carte Spéciale Gardien
function GoalkeeperCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🥅 Gardien</h3>
      <div className="space-y-1">
        <StatItem label="Arrêts" value={stats.saves} />
        <StatItem label="Arrêts dans la surface" value={stats.inside_box_saves} />
        <StatItem label="Penalties arrêtés" value={stats.penalties_saved} />
        <StatItem label="Clean sheets" value={stats.clean_sheets} />
        <StatItem label="Buts encaissés" value={stats.goals_conceded} />
        <StatItem label="Penalties concédés" value={stats.penalties_committed} />
        <StatItem label="Erreurs entraînant un but" value={stats.mistakes_leading_to_goals} />
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