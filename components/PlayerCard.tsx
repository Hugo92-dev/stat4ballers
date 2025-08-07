```tsx
import Link from 'next/link';

interface PlayerCardProps {
  player: {
    id: string;
    name: string;
    position: string;
    club: string;
    clubSlug: string;
    number: number;
    stats: {
      goals: number;
      assists: number;
      minutes: number;
    };
  };
}

export default function PlayerCard({ player }: PlayerCardProps) {
  return (
    <Link 
      href={`/ligue1/${player.clubSlug}/${player.id}`}
      className="block bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold text-[--primary]">{player.name}</h3>
          <p className="text-gray-600">{player.position} • #{player.number}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">{player.club}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-4 text-center">
        <div>
          <p className="text-2xl font-bold text-[--primary]">{player.stats.goals}</p>
          <p className="text-xs text-gray-500">Buts</p>
        </div>
        <div>
          <p className="text-2xl font-bold text-[--primary]">{player.stats.assists}</p>
          <p className="text-xs text-gray-500">Passes D.</p>
        </div>
        <div>
          <p className="text-2xl font-bold text-[--primary]">{player.stats.minutes}</p>
          <p className="text-xs text-gray-500">Minutes</p>
        </div>
      </div>
    </Link>
  );
}
```