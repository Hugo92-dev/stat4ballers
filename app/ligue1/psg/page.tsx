import Link from 'next/link';

export default function PSGPage() {
  const joueurs = [
    { id: 'donnarumma', nom: 'Gianluigi Donnarumma', poste: 'Gardien', numero: 99, buts: 0, passes_decisives: 0, minutes: 2700 },
    { id: 'hakimi', nom: 'Achraf Hakimi', poste: 'Défenseur', numero: 2, buts: 4, passes_decisives: 7, minutes: 2500 },
    { id: 'marquinhos', nom: 'Marquinhos', poste: 'Défenseur', numero: 5, buts: 2, passes_decisives: 1, minutes: 2400 },
    { id: 'vitinha', nom: 'Vitinha', poste: 'Milieu', numero: 17, buts: 7, passes_decisives: 5, minutes: 2300 },
    { id: 'zaire-emery', nom: 'Warren Zaïre-Emery', poste: 'Milieu', numero: 33, buts: 4, passes_decisives: 6, minutes: 2100 },
    { id: 'dembele', nom: 'Ousmane Dembélé', poste: 'Attaquant', numero: 10, buts: 8, passes_decisives: 6, minutes: 2200 },
    { id: 'barcola', nom: 'Bradley Barcola', poste: 'Attaquant', numero: 29, buts: 10, passes_decisives: 4, minutes: 2000 },
    { id: 'ramos', nom: 'Gonçalo Ramos', poste: 'Attaquant', numero: 9, buts: 11, passes_decisives: 3, minutes: 1800 },
  ];

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/ligue1" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à la Ligue 1
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">
          Effectif Paris Saint-Germain
        </h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {joueurs.map(joueur => (
            <div key={joueur.id} className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-xl font-semibold text-blue-900">{joueur.nom}</h3>
                <span className="text-2xl font-bold text-gray-400">#{joueur.numero}</span>
              </div>
              <p className="text-gray-600">{joueur.poste}</p>
              <div className="mt-4 text-sm text-gray-500">
                <p>⚽ {joueur.buts} buts • 🅰️ {joueur.passes_decisives} assists</p>
                <p>⏱️ {joueur.minutes} minutes jouées</p>
              </div>
              <Link 
                href={`/ligue1/psg/${joueur.id}`}
                className="mt-4 text-blue-600 hover:underline inline-block"
              >
                Voir les stats complètes →
              </Link>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}