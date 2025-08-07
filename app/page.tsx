```tsx
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-[--background]">
      {/* Hero Section */}
      <section className="bg-[--primary] text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Stat4Ballers
          </h1>
          <p className="text-xl mb-8 opacity-90">
            Toutes les statistiques des joueurs de Ligue 1 en un coup d'œil
          </p>
          <Link 
            href="/ligue1" 
            className="bg-white text-[--primary] px-8 py-4 rounded-lg font-semibold hover:bg-opacity-90 transition inline-block"
          >
            Explorer la Ligue 1
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-[--primary]">
            4 dimensions pour analyser chaque joueur
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: "Stats Générales", icon: "📊", desc: "Buts, passes décisives, temps de jeu" },
              { title: "Stats Offensives", icon: "⚡", desc: "xG, tirs, dribbles réussis" },
              { title: "Stats Défensives", icon: "🛡️", desc: "Tacles, interceptions, duels" },
              { title: "Stats Créatives", icon: "🎯", desc: "Passes clés, centres, touches" }
            ].map((feature, i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-2 text-[--primary]">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
```