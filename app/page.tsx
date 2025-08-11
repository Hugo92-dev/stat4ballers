import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <section className="bg-blue-900 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Stat4Ballers
          </h1>
          <p className="text-xl mb-8 opacity-90">
            Toutes les statistiques des joueurs de Ligue 1
          </p>
          <Link 
            href="/ligue1" 
            className="bg-white text-blue-900 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition inline-block"
          >
            Explorer la Ligue 1
          </Link>
        </div>
      </section>

      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-blue-900">
            4 dimensions pour analyser chaque joueur
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2 text-blue-900">Stats Générales</h3>
              <p className="text-gray-600">Buts, passes décisives, temps de jeu</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2 text-blue-900">Stats Offensives</h3>
              <p className="text-gray-600">xG, tirs, dribbles réussis</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">🛡️</div>
              <h3 className="text-xl font-semibold mb-2 text-blue-900">Stats Défensives</h3>
              <p className="text-gray-600">Tacles, interceptions, duels</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2 text-blue-900">Stats Créatives</h3>
              <p className="text-gray-600">Passes clés, centres, touches</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}