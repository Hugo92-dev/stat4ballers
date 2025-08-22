'use client';

import { LayoutList, Radar } from 'lucide-react';

interface ViewSelectorProps {
  currentView: 'list' | 'radar';
  onViewChange: (view: 'list' | 'radar') => void;
}

export default function ViewSelector({ currentView, onViewChange }: ViewSelectorProps) {
  return (
    <div className="flex gap-2 mb-4">
      <button
        onClick={() => onViewChange('radar')}
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all
          ${currentView === 'radar' 
            ? 'bg-blue-600 text-white shadow-md' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }
        `}
      >
        <Radar className="w-4 h-4" />
        Vue Radar
      </button>
      <button
        onClick={() => onViewChange('list')}
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all
          ${currentView === 'list' 
            ? 'bg-blue-600 text-white shadow-md' 
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }
        `}
      >
        <LayoutList className="w-4 h-4" />
        Vue Liste
      </button>
    </div>
  );
}