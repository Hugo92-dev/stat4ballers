'use client';

import { useState, useRef, useEffect } from 'react';
import { ClubColors } from '@/data/clubColors';

interface UltraModernSearchBarProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
  colors: ClubColors;
  resultCount?: number;
}

export default function UltraModernSearchBar({
  searchTerm,
  onSearchChange,
  colors,
  resultCount
}: UltraModernSearchBarProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  
  useEffect(() => {
    if (searchTerm) {
      setIsTyping(true);
      const timer = setTimeout(() => setIsTyping(false), 500);
      return () => clearTimeout(timer);
    }
  }, [searchTerm]);

  const handleClear = () => {
    onSearchChange('');
    inputRef.current?.focus();
  };

  return (
    <div className="relative max-w-2xl mx-auto mb-16">
      {/* Background glow effect */}
      <div className={`
        absolute inset-0 bg-gradient-to-r ${colors.gradient}
        rounded-full opacity-10 blur-2xl scale-110
        ${isFocused ? 'opacity-20 scale-125' : ''}
        transition-all duration-700
      `} />
      
      {/* Main search container */}
      <div className={`
        relative bg-white/5 backdrop-blur-2xl rounded-full
        border border-white/10 overflow-hidden
        ${isFocused ? 'border-white/30 bg-white/10' : ''}
        transition-all duration-500 ease-out
        group
      `}>
        
        {/* Animated border */}
        <div className={`
          absolute inset-0 rounded-full opacity-0
          bg-gradient-to-r ${colors.gradient} p-[1px]
          ${isFocused ? 'opacity-100' : ''}
          transition-opacity duration-300
        `}>
          <div className="w-full h-full rounded-full bg-transparent" />
        </div>
        
        {/* Search input */}
        <div className="relative flex items-center">
          {/* Search icon */}
          <div className={`
            absolute left-6 z-10 transition-all duration-300
            ${isFocused ? 'scale-110 text-white' : 'text-gray-400'}
          `}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          
          <input
            ref={inputRef}
            type="text"
            placeholder="Rechercher un joueur, position, nationalité..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            className={`
              w-full h-16 pl-16 pr-16 bg-transparent text-white text-lg
              placeholder-gray-400 focus:outline-none
              transition-all duration-300
              ${isFocused ? 'text-xl' : ''}
            `}
          />
          
          {/* Clear button */}
          {searchTerm && (
            <button
              onClick={handleClear}
              className={`
                absolute right-6 w-8 h-8 flex items-center justify-center
                rounded-full bg-white/10 text-gray-400 hover:text-white
                hover:bg-white/20 transition-all duration-300
                transform ${searchTerm ? 'scale-100 opacity-100' : 'scale-0 opacity-0'}
              `}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
          
          {/* Typing indicator */}
          {isTyping && (
            <div className="absolute right-16 flex items-center gap-1">
              <div className={`w-1 h-1 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse`} />
              <div className={`w-1 h-1 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse delay-100`} />
              <div className={`w-1 h-1 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse delay-200`} />
            </div>
          )}
        </div>
        
        {/* Shimmer effect on hover */}
        <div className={`
          absolute inset-0 shimmer opacity-0 group-hover:opacity-100
          transition-opacity duration-500 pointer-events-none
        `} />
      </div>
      
      {/* Search results indicator */}
      {searchTerm && typeof resultCount === 'number' && (
        <div className={`
          absolute top-full mt-4 left-1/2 transform -translate-x-1/2
          px-6 py-3 rounded-2xl glass-morphism
          text-white text-sm font-medium
          animate-fade-in-up
        `}>
          {resultCount > 0 ? (
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse`} />
              <span>
                {resultCount} résultat{resultCount > 1 ? 's' : ''} trouvé{resultCount > 1 ? 's' : ''}
              </span>
            </div>
          ) : (
            <div className="flex items-center gap-2 text-orange-400">
              <div className="w-2 h-2 rounded-full bg-orange-400 animate-pulse" />
              <span>Aucun résultat trouvé</span>
            </div>
          )}
        </div>
      )}
      
      {/* Floating search suggestions (could be expanded later) */}
      {isFocused && !searchTerm && (
        <div className={`
          absolute top-full mt-6 left-1/2 transform -translate-x-1/2
          w-full max-w-md p-6 rounded-2xl glass-morphism-strong
          animate-fade-in-up
        `}>
          <div className="text-center">
            <div className="text-gray-400 text-sm mb-4">Suggestions de recherche</div>
            <div className="flex flex-wrap gap-2 justify-center">
              {['Gardiens', 'Défenseurs', 'Milieux', 'Attaquants', 'France', 'Brésil'].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => onSearchChange(suggestion)}
                  className={`
                    px-4 py-2 rounded-full text-sm font-medium
                    bg-gradient-to-r ${colors.gradient} text-white opacity-80
                    hover:opacity-100 hover:scale-105
                    transition-all duration-300
                  `}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}