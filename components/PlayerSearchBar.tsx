'use client';

import { useState, useEffect, useRef } from 'react';
import { fullSearchDatabase as searchDatabase } from '@/data/searchDatabase';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import Image from 'next/image';

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

interface PlayerSearchBarProps {
  onPlayerSelect: (player: Player | null) => void;
  placeholder?: string;
  selectedPlayer?: Player | null;
}

export default function PlayerSearchBar({ onPlayerSelect, placeholder = "Rechercher un joueur...", selectedPlayer }: PlayerSearchBarProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (query.length > 0) {
      const searchQuery = query.toLowerCase();
      
      // Filtrer uniquement les joueurs
      const filtered = searchDatabase
        .filter(item => item.type === 'player')
        .filter(item => {
          const inName = item.name.toLowerCase().includes(searchQuery);
          const inTerms = item.searchTerms.some(term => term.toLowerCase().includes(searchQuery));
          return inName || inTerms;
        });
      
      // Trier par pertinence
      filtered.sort((a, b) => {
        const aExact = a.searchTerms.some(term => term.toLowerCase() === searchQuery);
        const bExact = b.searchTerms.some(term => term.toLowerCase() === searchQuery);
        if (aExact && !bExact) return -1;
        if (!aExact && bExact) return 1;
        
        const aStarts = a.name.toLowerCase().startsWith(searchQuery);
        const bStarts = b.name.toLowerCase().startsWith(searchQuery);
        if (aStarts && !bStarts) return -1;
        if (!aStarts && bStarts) return 1;
        
        return 0;
      });
      
      setResults(filtered.slice(0, 8));
      setIsOpen(true);
      setHighlightedIndex(0);
    } else {
      setResults([]);
      setIsOpen(false);
    }
  }, [query]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen || results.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev + 1) % results.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev - 1 + results.length) % results.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[highlightedIndex]) {
        handleSelectPlayer(results[highlightedIndex]);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const handleSelectPlayer = (result: any) => {
    // Extraire les informations du joueur depuis le résultat de recherche
    const pathParts = result.path.split('/');
    const leagueSlug = pathParts[1];
    const clubSlug = pathParts[2];
    const playerSlug = pathParts[3];

    // Créer l'objet joueur à partir des informations disponibles
    const player: Player = {
      id: result.id || Math.random(), // Utiliser l'ID si disponible, sinon générer un ID temporaire
      name: result.name,
      fullName: result.fullName,
      displayName: result.displayName,
      position: result.position || 'Unknown',
      club: result.club || 'Unknown Club',
      league: result.league || 'Unknown League',
      clubSlug,
      leagueSlug,
      playerSlug
    };

    onPlayerSelect(player);
    setQuery(result.name);
    setIsOpen(false);
  };

  const highlightMatch = (text: string, query: string) => {
    if (!query) return text;
    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, index) => 
      part.toLowerCase() === query.toLowerCase() ? 
        <span key={index} className="font-semibold text-blue-600">{part}</span> : 
        part
    );
  };

  const displayValue = selectedPlayer 
    ? (selectedPlayer.displayName || selectedPlayer.fullName || selectedPlayer.name)
    : query;

  return (
    <div ref={searchRef} className="relative w-full">
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={displayValue}
          onChange={(e) => {
            setQuery(e.target.value);
            if (selectedPlayer && e.target.value !== (selectedPlayer.displayName || selectedPlayer.fullName || selectedPlayer.name)) {
              onPlayerSelect(null);
            }
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (query.length > 0) {
              setIsOpen(true);
            }
          }}
          placeholder={placeholder}
          className="w-full px-4 py-3 pr-12 text-base bg-white rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:outline-none transition-all duration-200 shadow-sm"
        />
        
        {selectedPlayer ? (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 bg-green-100 p-1.5 rounded-lg">
            <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        ) : (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 bg-gray-100 p-1.5 rounded-lg">
            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        )}
      </div>

      {isOpen && results.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-xl shadow-xl border border-gray-200 overflow-hidden z-50 max-h-80 overflow-y-auto">
          <div className="py-2">
            {results.map((result, index) => (
              <button
                key={`player-${result.name}-${index}`}
                onClick={() => handleSelectPlayer(result)}
                className={`w-full flex items-center px-4 py-3 text-left transition-all duration-150 ${
                  index === highlightedIndex 
                    ? 'bg-blue-50 border-l-4 border-blue-500' 
                    : 'hover:bg-gray-50'
                }`}
              >
                {/* Avatar joueur */}
                <div className="mr-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full flex items-center justify-center">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-gray-900 truncate">
                    {highlightMatch(result.name, query)}
                  </div>
                  <div className="text-sm text-gray-500 truncate">
                    {result.league} • {result.club}
                  </div>
                </div>
                
                {/* Logo du club */}
                {result.club && (
                  <div className="ml-2 flex-shrink-0">
                    <div className="w-8 h-8 flex items-center justify-center">
                      <Image
                        src={getClubLogoPath(result.path.split('/')[1], result.path.split('/')[2])}
                        alt={result.club}
                        width={24}
                        height={24}
                        className="object-contain"
                        onError={(e) => {
                          const img = e.target as HTMLImageElement;
                          img.style.display = 'none';
                        }}
                      />
                    </div>
                  </div>
                )}
              </button>
            ))}
          </div>
          
          {results.length === 8 && (
            <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
              <p className="text-xs text-gray-500">
                Affichage des 8 premiers résultats. Affinez votre recherche pour plus de précision.
              </p>
            </div>
          )}
        </div>
      )}
      
      {query.length > 0 && results.length === 0 && isOpen && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-xl shadow-xl border border-gray-200 overflow-hidden z-50">
          <div className="px-4 py-6 text-center text-gray-500">
            <svg className="w-12 h-12 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-sm">Aucun joueur trouvé</p>
            <p className="text-xs text-gray-400 mt-1">Essayez avec un autre nom</p>
          </div>
        </div>
      )}
    </div>
  );
}