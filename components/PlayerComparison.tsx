'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import PlayerSearchBar from './PlayerSearchBar';

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

export default function PlayerComparison() {
  const [selectedPlayers, setSelectedPlayers] = useState<(Player | null)[]>([null, null]);
  const [maxPlayers, setMaxPlayers] = useState(2);
  const router = useRouter();

  const addPlayerSlot = () => {
    if (maxPlayers < 4) {
      setSelectedPlayers([...selectedPlayers, null]);
      setMaxPlayers(maxPlayers + 1);
    }
  };

  const removePlayerSlot = (index: number) => {
    if (maxPlayers > 2) {
      const newPlayers = selectedPlayers.filter((_, i) => i !== index);
      setSelectedPlayers(newPlayers);
      setMaxPlayers(maxPlayers - 1);
    }
  };

  const handlePlayerSelect = (index: number, player: Player | null) => {
    const newPlayers = [...selectedPlayers];
    newPlayers[index] = player;
    setSelectedPlayers(newPlayers);
  };

  const clearPlayer = (index: number) => {
    handlePlayerSelect(index, null);
  };

  const canCompare = selectedPlayers.filter(p => p !== null).length >= 2;

  const handleCompare = () => {
    const validPlayers = selectedPlayers.filter(p => p !== null) as Player[];
    if (validPlayers.length >= 2) {
      // Construire l'URL de comparaison avec les IDs des joueurs
      const playerIds = validPlayers.map(p => p.id).join(',');
      router.push(`/compare?players=${playerIds}`);
    }
  };

  return (
    <div className="w-full">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold mb-2 text-white">
          Comparateur de Joueurs
        </h3>
        <p className="text-blue-100/80 text-sm">
          Comparez les performances de 2 à 4 joueurs
        </p>
      </div>

      {/* Barres de recherche des joueurs */}
      <div className="space-y-3 mb-4">
        {selectedPlayers.map((player, index) => (
          <div key={index} className="relative">
            <div className="flex items-center gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md">
                {index + 1}
              </div>
              
              <div className="flex-1">
                <PlayerSearchBar
                  onPlayerSelect={(selectedPlayer) => handlePlayerSelect(index, selectedPlayer)}
                  placeholder={`Rechercher le joueur ${index + 1}...`}
                  selectedPlayer={player}
                />
              </div>

              {/* Bouton supprimer (uniquement pour les slots > 2) */}
              {index >= 2 && (
                <button
                  onClick={() => removePlayerSlot(index)}
                  className="flex-shrink-0 w-8 h-8 bg-red-100 hover:bg-red-200 rounded-full flex items-center justify-center text-red-600 transition-colors"
                  title="Supprimer ce joueur"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}

              {/* Bouton clear */}
              {player && (
                <button
                  onClick={() => clearPlayer(index)}
                  className="flex-shrink-0 w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center text-gray-600 transition-colors"
                  title="Effacer la sélection"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Boutons d'action */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-center mb-4">
        {/* Bouton Comparer - Plus visible */}
        <button
          onClick={handleCompare}
          disabled={!canCompare}
          className={`inline-flex items-center gap-3 px-10 py-4 rounded-xl font-bold text-base transition-all duration-300 transform shadow-xl ${
            canCompare
              ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white hover:shadow-2xl hover:scale-105 animate-pulse'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-50'
          }`}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span className="text-lg">Comparer</span>
          {canCompare && (
            <span className="text-sm font-normal opacity-90 bg-white/20 px-2 py-1 rounded-full">
              {selectedPlayers.filter(p => p !== null).length} joueurs
            </span>
          )}
        </button>
        
        {/* Bouton ajouter un joueur */}
        {maxPlayers < 4 && (
          <button
            onClick={addPlayerSlot}
            className="inline-flex items-center gap-2 px-6 py-3 bg-white/90 backdrop-blur hover:bg-white rounded-xl text-gray-700 font-medium transition-all transform hover:scale-105 shadow-lg"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>Ajouter un joueur</span>
          </button>
        )}
      </div>
      
      {!canCompare && (
        <p className="text-center text-white/70 text-sm animate-pulse">
          ⚠️ Sélectionnez au moins 2 joueurs pour démarrer la comparaison
        </p>
      )}

      {/* Affichage des joueurs sélectionnés - Plus compact */}
      {selectedPlayers.some(p => p !== null) && (
        <div className="mt-6">
          <div className="flex flex-wrap gap-2 justify-center">
            {selectedPlayers.map((player, index) => (
              player ? (
                <div key={index} className="bg-white/10 backdrop-blur rounded-lg px-3 py-2 flex items-center gap-2">
                  <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xs">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-medium text-white text-sm">
                      {player.displayName || player.fullName || player.name}
                    </div>
                    <div className="text-xs text-white/60">
                      {player.club}
                    </div>
                  </div>
                </div>
              ) : null
            ))}
          </div>
        </div>
      )}
    </div>
  );
}