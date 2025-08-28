'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import goatData from '@/data/goat/goat_stats.json';

interface SeasonStats {
  season_name: string;
  team_name: string;
  statistics: {
    matches_jouées: number;
    minutes_jouées: number;
    buts: number;
    passes_décisives: number;
    cartons_jaunes: number;
    cartons_rouges: number;
  };
}

interface CareerTotals {
  total_buts: number;
  total_passes_décisives: number;
  total_matches: number;
  total_minutes: number;
  total_cartons_jaunes: number;
  total_cartons_rouges: number;
  nombre_saisons: number;
  buts_par_match: number;
  passes_par_match: number;
}

interface PlayerData {
  player_id: number;
  name: string;
  seasons: SeasonStats[];
  career_totals: CareerTotals;
}

export default function CR7VsMessiPage() {
  const [selectedView, setSelectedView] = useState<'overview' | 'seasons' | 'comparison'>('overview');
  const [selectedSeason, setSelectedSeason] = useState<string | null>(null);

  const ronaldoData = goatData.ronaldo as PlayerData;
  const messiData = goatData.messi as PlayerData;

  // Fonction pour obtenir les couleurs de performance
  const getPerformanceColor = (value: number, max: number) => {
    const percentage = (value / max) * 100;
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-blue-500';
    if (percentage >= 40) return 'bg-yellow-500';
    return 'bg-gray-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900">
      {/* Header avec titre épique */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-red-900/20 via-transparent to-blue-900/20"></div>
        <div className="container mx-auto px-4 py-8 relative">
          <Link href="/" className="text-white hover:text-gray-300 mb-4 inline-block">
            ← Retour à l'accueil
          </Link>
          
          <div className="text-center mb-8">
            <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-red-500 via-white to-blue-500 bg-clip-text text-transparent">
              CR7 vs MESSI
            </h1>
            <p className="text-xl text-gray-300">Le débat éternel : Qui est le GOAT ?</p>
          </div>

          {/* Navigation des vues */}
          <div className="flex justify-center gap-4 mb-8">
            <button
              onClick={() => setSelectedView('overview')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedView === 'overview'
                  ? 'bg-gradient-to-r from-red-600 to-blue-600 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              Vue d'ensemble
            </button>
            <button
              onClick={() => setSelectedView('seasons')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedView === 'seasons'
                  ? 'bg-gradient-to-r from-red-600 to-blue-600 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              Saisons détaillées
            </button>
            <button
              onClick={() => setSelectedView('comparison')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                selectedView === 'comparison'
                  ? 'bg-gradient-to-r from-red-600 to-blue-600 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              }`}
            >
              Comparaison directe
            </button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 pb-12">
        {/* Vue d'ensemble - Statistiques carrière */}
        {selectedView === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Carte Ronaldo */}
            <div className="bg-gradient-to-br from-red-900/30 to-red-600/20 border border-red-500/30 rounded-xl p-6">
              <div className="text-center mb-6">
                <h2 className="text-4xl font-bold text-red-400 mb-2">Cristiano Ronaldo</h2>
                <p className="text-gray-400">Le Commandant</p>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Total Buts</p>
                  <p className="text-3xl font-bold text-white">{ronaldoData.career_totals.total_buts}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Passes Décisives</p>
                  <p className="text-3xl font-bold text-white">{ronaldoData.career_totals.total_passes_décisives}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Matchs Joués</p>
                  <p className="text-3xl font-bold text-white">{ronaldoData.career_totals.total_matches}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Buts/Match</p>
                  <p className="text-3xl font-bold text-white">{ronaldoData.career_totals.buts_par_match}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Minutes Jouées</p>
                  <p className="text-2xl font-bold text-white">{ronaldoData.career_totals.total_minutes.toLocaleString()}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Nombre de Saisons</p>
                  <p className="text-2xl font-bold text-white">{ronaldoData.career_totals.nombre_saisons}</p>
                </div>
              </div>

              <div className="bg-black/40 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-xs">
                  Statistiques de 2002/03 à 2025/26 - Championnats domestiques uniquement
                  <br />
                  (Hors coupes nationales, compétitions européennes et matchs internationaux)
                </p>
              </div>
            </div>

            {/* Carte Messi */}
            <div className="bg-gradient-to-br from-blue-900/30 to-blue-600/20 border border-blue-500/30 rounded-xl p-6">
              <div className="text-center mb-6">
                <h2 className="text-4xl font-bold text-blue-400 mb-2">Lionel Messi</h2>
                <p className="text-gray-400">La Pulga</p>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Total Buts</p>
                  <p className="text-3xl font-bold text-white">{messiData.career_totals.total_buts}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Passes Décisives</p>
                  <p className="text-3xl font-bold text-white">{messiData.career_totals.total_passes_décisives}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Matchs Joués</p>
                  <p className="text-3xl font-bold text-white">{messiData.career_totals.total_matches}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Buts/Match</p>
                  <p className="text-3xl font-bold text-white">{messiData.career_totals.buts_par_match}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Minutes Jouées</p>
                  <p className="text-2xl font-bold text-white">{messiData.career_totals.total_minutes.toLocaleString()}</p>
                </div>
                <div className="bg-black/40 rounded-lg p-4">
                  <p className="text-gray-400 text-sm">Nombre de Saisons</p>
                  <p className="text-2xl font-bold text-white">{messiData.career_totals.nombre_saisons}</p>
                </div>
              </div>

              <div className="bg-black/40 rounded-lg p-4 text-center">
                <p className="text-gray-400 text-xs">
                  Statistiques de 2004/05 à 2025/26 - Championnats domestiques uniquement
                  <br />
                  (Hors coupes nationales, compétitions européennes et matchs internationaux)
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Vue Saisons Détaillées */}
        {selectedView === 'seasons' && (
          <div>
            {/* Sélecteur de saison */}
            <div className="mb-8 bg-gray-800/50 rounded-xl p-4">
              <h3 className="text-xl font-semibold text-white mb-4">Sélectionner une saison</h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {ronaldoData.seasons.map((season) => (
                  <button
                    key={season.season_name}
                    onClick={() => setSelectedSeason(season.season_name)}
                    className={`p-3 rounded-lg transition-all ${
                      selectedSeason === season.season_name
                        ? 'bg-gradient-to-r from-red-600 to-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    {season.season_name}
                  </button>
                ))}
              </div>
            </div>

            {/* Comparaison de la saison sélectionnée */}
            {selectedSeason && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Stats Ronaldo pour la saison */}
                {(() => {
                  const ronaldoSeason = ronaldoData.seasons.find(s => s.season_name === selectedSeason);
                  const messiSeason = messiData.seasons.find(s => s.season_name === selectedSeason);
                  
                  return (
                    <>
                      {ronaldoSeason && (
                        <div className="bg-gradient-to-br from-red-900/30 to-red-600/20 border border-red-500/30 rounded-xl p-6">
                          <h3 className="text-2xl font-bold text-red-400 mb-2">Cristiano Ronaldo</h3>
                          <p className="text-gray-400 mb-4">{ronaldoSeason.team_name}</p>
                          
                          <div className="space-y-3">
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Matchs</span>
                              <span className="text-xl font-bold text-white">{ronaldoSeason.statistics.matches_jouées}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Buts</span>
                              <span className="text-xl font-bold text-white">{ronaldoSeason.statistics.buts}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Passes Décisives</span>
                              <span className="text-xl font-bold text-white">{ronaldoSeason.statistics.passes_décisives}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Minutes</span>
                              <span className="text-xl font-bold text-white">{ronaldoSeason.statistics.minutes_jouées}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Cartons Jaunes</span>
                              <span className="text-xl font-bold text-yellow-400">{ronaldoSeason.statistics.cartons_jaunes}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      {messiSeason && (
                        <div className="bg-gradient-to-br from-blue-900/30 to-blue-600/20 border border-blue-500/30 rounded-xl p-6">
                          <h3 className="text-2xl font-bold text-blue-400 mb-2">Lionel Messi</h3>
                          <p className="text-gray-400 mb-4">{messiSeason.team_name}</p>
                          
                          <div className="space-y-3">
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Matchs</span>
                              <span className="text-xl font-bold text-white">{messiSeason.statistics.matches_jouées}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Buts</span>
                              <span className="text-xl font-bold text-white">{messiSeason.statistics.buts}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Passes Décisives</span>
                              <span className="text-xl font-bold text-white">{messiSeason.statistics.passes_décisives}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Minutes</span>
                              <span className="text-xl font-bold text-white">{messiSeason.statistics.minutes_jouées}</span>
                            </div>
                            <div className="flex justify-between items-center bg-black/40 rounded-lg p-3">
                              <span className="text-gray-300">Cartons Jaunes</span>
                              <span className="text-xl font-bold text-yellow-400">{messiSeason.statistics.cartons_jaunes}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </>
                  );
                })()}
              </div>
            )}
          </div>
        )}

        {/* Vue Comparaison Directe */}
        {selectedView === 'comparison' && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-gray-800/50 rounded-xl p-6">
              <h2 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-red-500 to-blue-500 bg-clip-text text-transparent">
                Comparaison Face à Face
              </h2>

              {/* Statistiques comparatives */}
              <div className="space-y-6">
                {/* Buts */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-300 mb-3">Total Buts</h3>
                  <div className="flex items-center gap-4">
                    <div className="text-right flex-1">
                      <p className="text-2xl font-bold text-red-400">{ronaldoData.career_totals.total_buts}</p>
                      <p className="text-sm text-gray-400">Ronaldo</p>
                    </div>
                    <div className="flex-[2] bg-black/40 rounded-full h-12 overflow-hidden relative">
                      <div 
                        className="absolute left-0 h-full bg-gradient-to-r from-red-600 to-red-400"
                        style={{ width: `${(ronaldoData.career_totals.total_buts / (ronaldoData.career_totals.total_buts + messiData.career_totals.total_buts)) * 100}%` }}
                      />
                      <div 
                        className="absolute right-0 h-full bg-gradient-to-l from-blue-600 to-blue-400"
                        style={{ width: `${(messiData.career_totals.total_buts / (ronaldoData.career_totals.total_buts + messiData.career_totals.total_buts)) * 100}%` }}
                      />
                    </div>
                    <div className="flex-1">
                      <p className="text-2xl font-bold text-blue-400">{messiData.career_totals.total_buts}</p>
                      <p className="text-sm text-gray-400">Messi</p>
                    </div>
                  </div>
                </div>

                {/* Passes Décisives */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-300 mb-3">Total Passes Décisives</h3>
                  <div className="flex items-center gap-4">
                    <div className="text-right flex-1">
                      <p className="text-2xl font-bold text-red-400">{ronaldoData.career_totals.total_passes_décisives}</p>
                      <p className="text-sm text-gray-400">Ronaldo</p>
                    </div>
                    <div className="flex-[2] bg-black/40 rounded-full h-12 overflow-hidden relative">
                      <div 
                        className="absolute left-0 h-full bg-gradient-to-r from-red-600 to-red-400"
                        style={{ width: `${(ronaldoData.career_totals.total_passes_décisives / (ronaldoData.career_totals.total_passes_décisives + messiData.career_totals.total_passes_décisives)) * 100}%` }}
                      />
                      <div 
                        className="absolute right-0 h-full bg-gradient-to-l from-blue-600 to-blue-400"
                        style={{ width: `${(messiData.career_totals.total_passes_décisives / (ronaldoData.career_totals.total_passes_décisives + messiData.career_totals.total_passes_décisives)) * 100}%` }}
                      />
                    </div>
                    <div className="flex-1">
                      <p className="text-2xl font-bold text-blue-400">{messiData.career_totals.total_passes_décisives}</p>
                      <p className="text-sm text-gray-400">Messi</p>
                    </div>
                  </div>
                </div>

                {/* Buts par Match */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-300 mb-3">Buts par Match</h3>
                  <div className="flex items-center gap-4">
                    <div className="text-right flex-1">
                      <p className="text-2xl font-bold text-red-400">{ronaldoData.career_totals.buts_par_match}</p>
                      <p className="text-sm text-gray-400">Ronaldo</p>
                    </div>
                    <div className="flex-[2] bg-black/40 rounded-full h-12 overflow-hidden relative">
                      <div 
                        className="absolute left-0 h-full bg-gradient-to-r from-red-600 to-red-400"
                        style={{ width: `${(ronaldoData.career_totals.buts_par_match / (ronaldoData.career_totals.buts_par_match + messiData.career_totals.buts_par_match)) * 100}%` }}
                      />
                      <div 
                        className="absolute right-0 h-full bg-gradient-to-l from-blue-600 to-blue-400"
                        style={{ width: `${(messiData.career_totals.buts_par_match / (ronaldoData.career_totals.buts_par_match + messiData.career_totals.buts_par_match)) * 100}%` }}
                      />
                    </div>
                    <div className="flex-1">
                      <p className="text-2xl font-bold text-blue-400">{messiData.career_totals.buts_par_match}</p>
                      <p className="text-sm text-gray-400">Messi</p>
                    </div>
                  </div>
                </div>

                {/* Passes par Match */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-300 mb-3">Passes Décisives par Match</h3>
                  <div className="flex items-center gap-4">
                    <div className="text-right flex-1">
                      <p className="text-2xl font-bold text-red-400">{ronaldoData.career_totals.passes_par_match}</p>
                      <p className="text-sm text-gray-400">Ronaldo</p>
                    </div>
                    <div className="flex-[2] bg-black/40 rounded-full h-12 overflow-hidden relative">
                      <div 
                        className="absolute left-0 h-full bg-gradient-to-r from-red-600 to-red-400"
                        style={{ width: `${(ronaldoData.career_totals.passes_par_match / (ronaldoData.career_totals.passes_par_match + messiData.career_totals.passes_par_match)) * 100}%` }}
                      />
                      <div 
                        className="absolute right-0 h-full bg-gradient-to-l from-blue-600 to-blue-400"
                        style={{ width: `${(messiData.career_totals.passes_par_match / (ronaldoData.career_totals.passes_par_match + messiData.career_totals.passes_par_match)) * 100}%` }}
                      />
                    </div>
                    <div className="flex-1">
                      <p className="text-2xl font-bold text-blue-400">{messiData.career_totals.passes_par_match}</p>
                      <p className="text-sm text-gray-400">Messi</p>
                    </div>
                  </div>
                </div>

                {/* Matchs Joués */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-300 mb-3">Total Matchs</h3>
                  <div className="flex items-center gap-4">
                    <div className="text-right flex-1">
                      <p className="text-2xl font-bold text-red-400">{ronaldoData.career_totals.total_matches}</p>
                      <p className="text-sm text-gray-400">Ronaldo</p>
                    </div>
                    <div className="flex-[2] bg-black/40 rounded-full h-12 overflow-hidden relative">
                      <div 
                        className="absolute left-0 h-full bg-gradient-to-r from-red-600 to-red-400"
                        style={{ width: `${(ronaldoData.career_totals.total_matches / (ronaldoData.career_totals.total_matches + messiData.career_totals.total_matches)) * 100}%` }}
                      />
                      <div 
                        className="absolute right-0 h-full bg-gradient-to-l from-blue-600 to-blue-400"
                        style={{ width: `${(messiData.career_totals.total_matches / (ronaldoData.career_totals.total_matches + messiData.career_totals.total_matches)) * 100}%` }}
                      />
                    </div>
                    <div className="flex-1">
                      <p className="text-2xl font-bold text-blue-400">{messiData.career_totals.total_matches}</p>
                      <p className="text-sm text-gray-400">Messi</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Verdict */}
              <div className="mt-10 text-center p-6 bg-gradient-to-r from-red-900/20 to-blue-900/20 rounded-xl border border-gray-700">
                <h3 className="text-2xl font-bold mb-3 bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
                  Le Verdict
                </h3>
                <p className="text-gray-300">
                  Les deux légendes ont marqué l'histoire du football. Ronaldo excelle en puissance et régularité,
                  Messi brille par sa créativité et son efficacité. Le débat reste ouvert...
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}