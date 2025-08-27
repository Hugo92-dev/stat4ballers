import Link from 'next/link';
import Image from 'next/image';
import SearchBar from '@/components/SearchBar';
import PlayerComparison from '@/components/PlayerComparison';
import { leagueLogos } from '@/data/logos';

const leagues = [
  { 
    id: 'ligue1', 
    name: 'Ligue 1', 
    gradient: 'from-blue-600 via-blue-700 to-indigo-800',
    teams: 18,
    description: 'Le championnat de France',
    highlight: '#dae025'
  },
  { 
    id: 'premier-league', 
    name: 'Premier League', 
    gradient: 'from-purple-700 via-purple-800 to-indigo-900',
    teams: 20,
    description: 'Le championnat d\'Angleterre',
    highlight: '#00ff85'
  },
  { 
    id: 'liga', 
    name: 'La Liga', 
    gradient: 'from-red-600 via-orange-600 to-red-700',
    teams: 20,
    description: 'Le championnat d\'Espagne',
    highlight: '#ffffff'
  },
  { 
    id: 'serie-a', 
    name: 'Serie A', 
    gradient: 'from-green-600 via-emerald-700 to-teal-800',
    teams: 20,
    description: 'Le championnat d\'Italie',
    highlight: '#ffffff'
  },
  { 
    id: 'bundesliga', 
    name: 'Bundesliga', 
    gradient: 'from-gray-800 via-gray-900 to-black',
    teams: 18,
    description: 'Le championnat d\'Allemagne',
    highlight: '#d20515'
  }
];

const features = [
  {
    title: '⚽ Carte Générale',
    description: 'Statistiques globales du joueur sur la saison',
    gradient: 'from-blue-500 to-indigo-600',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    )
  },
  {
    title: '⚔️ Carte Offensive',
    description: 'Performance et statistiques offensives détaillées',
    gradient: 'from-red-500 to-pink-600',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    )
  },
  {
    title: '🧑‍🎨 Carte Créative',
    description: 'Capacités de création, de vista et de passes',
    gradient: 'from-purple-500 to-violet-600',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
      </svg>
    )
  },
  {
    title: '🛡️ Carte Défensive',
    description: 'Impact défensif et nombre de cartons',
    gradient: 'from-green-500 to-emerald-600',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      </svg>
    )
  },
  {
    title: '🧤 Carte Gardien',
    description: 'Statistiques spécifiques pour les gardiens de but',
    gradient: 'from-orange-500 to-amber-600',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    )
  }
];

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 via-white to-gray-50">
      {/* Hero Section Premium */}
      <section className="relative min-h-[80vh] overflow-hidden bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
          <div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/20 rounded-full filter blur-3xl animate-pulse"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500/20 rounded-full filter blur-3xl animate-pulse delay-1000"></div>
        </div>
        
        <div className="relative container mx-auto px-4 py-32">
          <div className="text-center max-w-5xl mx-auto">
            {/* Premium Logo */}
            <div className="inline-flex items-center justify-center mb-8">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-600 rounded-full blur-2xl opacity-50 animate-pulse"></div>
                <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 p-6 rounded-3xl border border-white/10 backdrop-blur-xl">
                  <div className="text-6xl font-black bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                    S4B
                  </div>
                </div>
              </div>
            </div>
            
            <h1 className="text-6xl md:text-8xl font-black text-white mb-6 tracking-tight">
              Stat<span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">4</span>Ballers
            </h1>
            
            <p className="text-xl md:text-2xl text-blue-100/90 mb-12 font-light max-w-3xl mx-auto leading-relaxed">
              La plateforme premium d'analyse statistique des plus grands talents du football européen
            </p>
            
            {/* Search Bar */}
            <div className="mb-8">
              <SearchBar />
            </div>
            
            {/* Player Comparison Section */}
            <div className="max-w-4xl mx-auto">
              <PlayerComparison />
            </div>
            
            {/* Stats Pills */}
            <div className="flex flex-wrap gap-4 justify-center">
              {[
                { label: 'Joueurs analysés', value: '2500+' },
                { label: 'Clubs couverts', value: '98' },
                { label: 'Championnats', value: '5' },
                { label: 'Statistiques', value: '40+' }
              ].map((stat, index) => (
                <div key={index} className="group relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all"></div>
                  <div className="relative bg-white/5 backdrop-blur-md border border-white/10 px-6 py-3 rounded-2xl hover:bg-white/10 transition-all">
                    <span className="text-3xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                      {stat.value}
                    </span>
                    <span className="ml-2 text-blue-200/70 text-sm font-medium">
                      {stat.label}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Wave Separator */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg className="w-full h-20" viewBox="0 0 1440 100" fill="none">
            <path d="M0,50 C360,100 720,0 1440,50 L1440,100 L0,100 Z" fill="rgb(249 250 251)" />
          </svg>
        </div>
      </section>

      {/* Leagues Section Premium */}
      <section className="py-24 px-4 bg-gradient-to-b from-gray-50 to-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-black mb-4 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
              Les 5 Grands Championnats
            </h2>
            <p className="text-gray-600 text-lg font-light">
              Sélectionnez votre championnat pour explorer les statistiques détaillées
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
            {leagues.map((league) => (
              <Link
                key={league.id}
                href={`/${league.id}`}
                className="group relative"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl transform transition-all duration-300 group-hover:scale-105"></div>
                <div className={`relative bg-gradient-to-br ${league.gradient} rounded-3xl p-1 transform transition-all duration-300 group-hover:scale-105`}>
                  <div className="bg-white rounded-3xl p-6 h-full">
                    {/* League Logo */}
                    <div className="h-20 w-20 mx-auto mb-4 relative">
                      <Image
                        src={leagueLogos[league.id]}
                        alt={league.name}
                        width={80}
                        height={80}
                        className="object-contain"
                      />
                    </div>
                    
                    <h3 className="text-xl font-bold mb-2 text-gray-900">
                      {league.name}
                    </h3>
                    <p className="text-sm text-gray-600 mb-4">
                      {league.description}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-700 bg-gray-100 px-3 py-1 rounded-full">
                        {league.teams} clubs
                      </span>
                      <div className={`w-10 h-10 bg-gradient-to-br ${league.gradient} rounded-full flex items-center justify-center text-white transform group-hover:translate-x-1 transition-transform`}>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section Premium */}
      <section className="py-24 bg-gradient-to-b from-white to-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-black mb-4 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
              5 Dimensions d'Analyse
            </h2>
            <p className="text-gray-600 text-lg font-light max-w-2xl mx-auto">
              Une vision complète et détaillée des performances de chaque joueur
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group relative h-full"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-gray-100 to-gray-200 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity transform scale-105"></div>
                <div className="relative bg-white rounded-3xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300 border border-gray-100 h-full flex flex-col">
                  <div className={`inline-flex p-4 bg-gradient-to-br ${feature.gradient} rounded-2xl text-white mb-4 group-hover:scale-110 transition-transform self-center`}>
                    {feature.icon}
                  </div>
                  
                  <h3 className="text-lg font-bold mb-2 text-gray-900 text-center min-h-[3rem] flex items-center justify-center">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 text-sm leading-relaxed text-center flex-1 flex items-center justify-center">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section Premium */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900"></div>
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        
        <div className="relative container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-black text-white mb-6">
            Prêt à analyser les meilleurs ?
          </h2>
          <p className="text-xl text-blue-100/90 mb-10 max-w-2xl mx-auto font-light">
            Explorez les statistiques détaillées de plus de 2500 joueurs professionnels
          </p>
          <Link
            href="/ligue1"
            className="inline-flex items-center bg-white text-gray-900 px-10 py-5 rounded-2xl font-bold text-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-200 group"
          >
            <span>Commencer l'exploration</span>
            <svg className="w-6 h-6 ml-3 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </section>
    </main>
  );
}