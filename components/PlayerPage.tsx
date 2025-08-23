'use client';

import { Player } from '@/data/types';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

interface PlayerPageProps {
  player: Player;
  clubName: string;
  clubSlug: string;
  leagueSlug: string;
  leagueColor: string;
}

export default function PlayerPage({ 
  player, 
  clubName, 
  clubSlug, 
  leagueSlug,
  leagueColor 
}: PlayerPageProps) {
  // Calculer l'âge à partir de la date de naissance
  const calculateAge = (birthDate: string | undefined): number => {
    if (!birthDate) return 0;
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };

  const age = calculateAge(player.dateOfBirth);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className={`bg-gradient-to-r ${leagueColor} text-white py-8`}>
        <div className="max-w-7xl mx-auto px-4">
          <Link 
            href={`/${leagueSlug}/${clubSlug}`}
            className="inline-flex items-center gap-2 text-white/80 hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Retour à l'effectif
          </Link>
          
          <div className="flex items-center gap-4">
            <div className="relative">
              {player.image ? (
                <img
                  src={player.image}
                  alt={player.displayName || player.fullName || player.name}
                  className="w-24 h-24 rounded-full object-cover border-4 border-white/30"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                    const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                    if (fallback) fallback.style.display = 'flex';
                  }}
                />
              ) : null}
              <div 
                className={`w-24 h-24 bg-white/20 rounded-full flex items-center justify-center ${player.image ? 'hidden' : ''}`}
                style={player.image ? { display: 'none' } : {}}
              >
                <span className="text-3xl font-bold">{player.jersey || player.number || '?'}</span>
              </div>
              {(player.jersey || player.number) && (
                <div className="absolute -bottom-2 -right-2 w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg">
                  <span className="text-lg font-bold text-gray-800">{player.jersey || player.number}</span>
                </div>
              )}
            </div>
            <div>
              <h1 className="text-3xl font-bold">
                {player.displayName || player.fullName || player.name}
              </h1>
              <p className="text-xl text-white/80">{clubName}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Player Info */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Informations</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <p className="text-gray-600 text-sm">Position</p>
              <p className="text-lg font-semibold">{player.position}</p>
            </div>
            
            <div>
              <p className="text-gray-600 text-sm">Nationalité</p>
              <p className="text-lg font-semibold">{player.nationality}</p>
            </div>
            
            <div>
              <p className="text-gray-600 text-sm">Âge</p>
              <p className="text-lg font-semibold">{age > 0 ? `${age} ans` : 'N/A'}</p>
            </div>
            
            {player.height && (
              <div>
                <p className="text-gray-600 text-sm">Taille</p>
                <p className="text-lg font-semibold">{player.height} cm</p>
              </div>
            )}
            
            {player.weight && (
              <div>
                <p className="text-gray-600 text-sm">Poids</p>
                <p className="text-lg font-semibold">{player.weight} kg</p>
              </div>
            )}
            
            {player.dateOfBirth && (
              <div>
                <p className="text-gray-600 text-sm">Date de naissance</p>
                <p className="text-lg font-semibold">
                  {new Date(player.dateOfBirth).toLocaleDateString('fr-FR')}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Statistics placeholder */}
        <div className="bg-white rounded-lg shadow-lg p-8 mt-8">
          <h2 className="text-2xl font-bold mb-6">Statistiques</h2>
          <p className="text-gray-600">Les statistiques seront bientôt disponibles...</p>
        </div>
      </div>
    </div>
  );
}