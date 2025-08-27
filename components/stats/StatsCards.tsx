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
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">⚽ Carte Générale</h3>
      <div className="space-y-1">
        <StatItem label="Matchs joués" value={stats.appearences} />
        <StatItem label="Titularisations" value={stats.lineups} />
        <StatItem label="Minutes jouées" value={stats.minutes} />
        <StatItem label="Capitaine" value={stats.captain} />
        <StatItem label="Note moyenne" value={stats.rating} />
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
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">⚔️ Carte Offensive</h3>
      <div className="space-y-1">
        <StatItem label="Buts" value={stats.goals} />
        <StatItem label="Passes décisives" value={stats.assists} />
        <StatItem label="Tirs tentés" value={stats.shots} />
        <StatItem label="Tirs cadrés" value={stats.shots_on_target} />
        <StatItem label="Tirs sur les montants" value={stats.hit_woodwork} />
        <StatItem label="Hors-jeu" value={stats.offsides} />
      </div>
    </div>
  );
}

// Carte Créative
function CreativeCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🧑‍🎨 Carte Créative</h3>
      <div className="space-y-1">
        <StatItem label="Passes" value={stats.passes_total || stats.passes} />
        <StatItem label="Précision des passes" value={stats.passes_accuracy} suffix="%" />
        <StatItem label="Passes clés" value={stats.key_passes} />
        <StatItem label="Centres" value={stats.crosses_total || stats.crosses} />
      </div>
    </div>
  );
}

// Carte Défensive & Discipline
function DefensiveCard({ stats }: { stats: PlayerStatistics }) {
  const totalRedCards = (stats.red_cards || 0) + (stats.yellowred_cards || 0);
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🛡️ Carte Défensive & Discipline</h3>
      <div className="space-y-1">
        <StatItem label="Duels totaux" value={stats.duels} />
        <StatItem label="Duels gagnés" value={stats.duels_won} />
        <StatItem label="Duels aériens gagnés" value={stats.aerial_duels_won} />
        <StatItem label="Tacles" value={stats.tackles} />
        <StatItem label="Fautes commises" value={stats.fouls} />
        <StatItem label="Fautes subies" value={stats.fouls_drawn} />
        <StatItem label="Cartons jaunes" value={stats.yellow_cards} />
        <StatItem label="Cartons rouges" value={totalRedCards} />
      </div>
    </div>
  );
}

// Carte Spéciale Gardien
function GoalkeeperCard({ stats }: { stats: PlayerStatistics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">🧤 Carte Gardien</h3>
      <div className="space-y-1">
        <StatItem label="Buts encaissés" value={stats.goals_conceded} />
        <StatItem label="Arrêts" value={stats.saves} />
        <StatItem label="Arrêts dans la surface" value={stats.inside_box_saves} />
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