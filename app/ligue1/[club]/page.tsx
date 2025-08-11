import Link from 'next/link';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Données de test pour PSG
  const joueurs = params.club === 'psg' ? [
    { id: 'donnarumma', nom: 'Gianluigi Donnarumma', poste: 'Gardien', numero: 99 },
    { id: 'hakimi', nom: 'Achraf Hakimi', poste: 'Défenseur', numero: 2 },
    { id: 'marquinhos', nom: 'Marquinhos', poste: 'Défenseur', numero: 5 },
    { id: 'vitinha', nom: 'Vitinha', poste: 'Milieu', numero: 17 },
    { id: 'dembele', nom: 'Ousmane Dembélé', poste: 'Attaquant', numero: 10 },
    { id: 'barcola', nom: 'Bradley Barcola', poste: 'Attaquant', numero: 29 },
  ] : [];

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/ligue1" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à la Ligue 1
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">
          Effectif {params.club.toUpperCase()}
        </h1>
        
        {joueurs.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {joueurs.map(joueur => (
              <div key={joueur.id} className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-blue-900">{joueur.nom}</h3>
                  <span className="text-2xl font-bold text-gray-400">#{joueur.numero}</span>
                </div>
                <p className="text-gray-600">{joueur.poste}</p>
                <Link 
                  href={`/ligue1/${params.club}/${joueur.id}`}
                  className="mt-4 text-blue-600 hover:underline inline-block"
                >
                  Voir les stats →
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600">Les données de ce club arrivent bientôt...</p>
        )}
      </div>
    </main>
  );
}