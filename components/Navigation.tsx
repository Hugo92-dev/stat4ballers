'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { leagueLogos } from '@/data/logos';

const leagues = [
  { id: 'ligue1', name: 'Ligue 1' },
  { id: 'premier-league', name: 'Premier League' },
  { id: 'liga', name: 'La Liga' },
  { id: 'serie-a', name: 'Serie A' },
  { id: 'bundesliga', name: 'Bundesliga' }
];

export default function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-lg' : 'bg-white/95 backdrop-blur-md shadow-md'
    }`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl">⚽</span>
            <span className="font-bold text-xl bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Stat4Ballers
            </span>
          </Link>

          <div className="hidden md:flex items-center space-x-1">
            {leagues.map((league) => (
              <Link
                key={league.id}
                href={`/${league.id}`}
                className={`px-4 py-2 rounded-lg transition-all duration-200 flex items-center space-x-1 ${
                  pathname?.startsWith(`/${league.id}`)
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Image
                  src={leagueLogos[league.id]}
                  alt={league.name}
                  width={20}
                  height={20}
                  className="object-contain"
                />
                <span className="font-medium ml-1">{league.name}</span>
              </Link>
            ))}
          </div>

          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            {leagues.map((league) => (
              <Link
                key={league.id}
                href={`/${league.id}`}
                onClick={() => setIsMenuOpen(false)}
                className={`block px-4 py-3 rounded-lg mb-2 transition-all ${
                  pathname?.startsWith(`/${league.id}`)
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <div className="flex items-center">
                  <Image
                    src={leagueLogos[league.id]}
                    alt={league.name}
                    width={24}
                    height={24}
                    className="object-contain mr-2"
                  />
                  <span>{league.name}</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}