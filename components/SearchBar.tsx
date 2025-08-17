'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { searchDatabase } from '@/data/searchDatabase';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { leagueLogos } from '@/data/logos';
import Image from 'next/image';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<typeof searchDatabase>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

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
      const filtered = searchDatabase.filter(item => {
        const inName = item.name.toLowerCase().includes(searchQuery);
        const inTerms = item.searchTerms.some(term => term.toLowerCase().includes(searchQuery));
        return inName || inTerms;
      });
      
      // Sort results by relevance
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
        router.push(results[highlightedIndex].path);
        setQuery('');
        setIsOpen(false);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const getIcon = (result: typeof searchDatabase[0]) => {
    // Pour les ligues
    if (result.type === 'league') {
      const leagueId = result.path.substring(1); // Enlever le /
      if (leagueLogos[leagueId]) {
        return (
          <div className="w-10 h-10 flex items-center justify-center">
            <Image
              src={leagueLogos[leagueId]}
              alt={result.name}
              width={32}
              height={32}
              className="object-contain"
            />
          </div>
        );
      }
    }
    
    // Pour les clubs
    if (result.type === 'club' && result.league) {
      const pathParts = result.path.split('/');
      const leagueId = pathParts[1];
      const clubId = pathParts[2];
      
      return (
        <div className="w-10 h-10 flex items-center justify-center">
          <Image
            src={getClubLogoPath(leagueId, clubId)}
            alt={result.name}
            width={36}
            height={36}
            className="object-contain"
            onError={(e) => {
              const img = e.target as HTMLImageElement;
              img.style.display = 'none';
            }}
          />
        </div>
      );
    }
    
    // Pour les joueurs
    if (result.type === 'player') {
      return (
        <div className="w-10 h-10 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full flex items-center justify-center">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
      );
    }
    
    return null;
  };

  const highlightMatch = (text: string, query: string) => {
    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, index) => 
      part.toLowerCase() === query.toLowerCase() ? 
        <span key={index} className="font-semibold text-blue-600">{part}</span> : 
        part
    );
  };

  return (
    <div ref={searchRef} className="relative w-full max-w-2xl mx-auto">
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Rechercher une ligue, un club ou un joueur..."
          className="w-full px-6 py-4 pr-14 text-base bg-white/95 backdrop-blur-sm rounded-2xl border-2 border-white/20 focus:border-white/40 focus:outline-none transition-all duration-200 shadow-2xl placeholder-gray-400"
          style={{ fontFamily: 'Poppins' }}
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2 bg-white/20 backdrop-blur-sm p-2.5 rounded-xl">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {isOpen && results.length > 0 && (
        <div className="absolute top-full mt-3 w-full bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden z-50">
          <div className="py-2">
            {results.map((result, index) => (
              <Link
                key={`${result.type}-${result.name}-${index}`}
                href={result.path}
                onClick={() => {
                  setQuery('');
                  setIsOpen(false);
                }}
                className={`flex items-center px-4 py-3 transition-all duration-150 ${
                  index === highlightedIndex 
                    ? 'bg-gradient-to-r from-blue-50 to-purple-50 border-l-4 border-blue-500' 
                    : 'hover:bg-gray-50'
                }`}
              >
                <div className="mr-3">
                  {getIcon(result)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-gray-900 truncate">
                    {highlightMatch(result.name, query)}
                  </div>
                  {(result.league || result.club) && (
                    <div className="text-sm text-gray-500 truncate">
                      {result.league} {result.club && `• ${result.club}`}
                    </div>
                  )}
                </div>
                <div className="ml-2 text-xs text-gray-400 uppercase tracking-wider">
                  {result.type}
                </div>
              </Link>
            ))}
          </div>
          <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
            <p className="text-xs text-gray-500">
              Utilisez <kbd className="px-1.5 py-0.5 text-xs bg-white rounded border">↑</kbd> <kbd className="px-1.5 py-0.5 text-xs bg-white rounded border">↓</kbd> pour naviguer, <kbd className="px-1.5 py-0.5 text-xs bg-white rounded border">Enter</kbd> pour sélectionner
            </p>
          </div>
        </div>
      )}
    </div>
  );
}