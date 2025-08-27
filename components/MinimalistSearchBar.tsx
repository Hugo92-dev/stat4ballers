'use client';

import { ClubColors } from '@/data/clubColors';

interface MinimalistSearchBarProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
  colors: ClubColors;
  resultCount?: number;
}

export default function MinimalistSearchBar({
  searchTerm,
  onSearchChange,
  colors,
  resultCount
}: MinimalistSearchBarProps) {
  const handleClear = () => {
    onSearchChange('');
  };

  return (
    <div className="max-w-md mx-auto mb-8">
      <div className="relative">
        {/* Search input */}
        <div className="relative">
          <input
            type="text"
            placeholder="Rechercher un joueur..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full h-10 pl-10 pr-10 text-sm bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-300 focus:border-transparent transition-all duration-200"
          />
          
          {/* Search icon */}
          <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          
          {/* Clear button */}
          {searchTerm && (
            <button
              onClick={handleClear}
              className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        
        {/* Subtle accent line */}
        {searchTerm && (
          <div className={`absolute bottom-0 left-0 h-0.5 bg-gradient-to-r ${colors.gradient} transition-all duration-300`} 
               style={{ width: `${Math.min((searchTerm.length / 20) * 100, 100)}%` }} />
        )}
      </div>
      
      {/* Result count */}
      {searchTerm && typeof resultCount === 'number' && (
        <div className="mt-3 text-center">
          <span className="text-xs text-gray-500">
            {resultCount > 0 ? (
              `${resultCount} résultat${resultCount > 1 ? 's' : ''}`
            ) : (
              'Aucun résultat'
            )}
          </span>
        </div>
      )}
    </div>
  );
}