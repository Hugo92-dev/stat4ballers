import Link from 'next/link';

export default function JoueurPageTest({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  // Base de données des joueurs avec stats réalistes
  const joueursData: { [key: string]: any } = {
    'dembele': {
      nom: 'Ousmane Dembélé',
      poste: 'Attaquant',
      numero: 10,
      age: 27,
      valeur: 60,
      buts: 8, passes_decisives: 6, ppm: 2.1, minutes: 2200, titu: 24, absences: 15, cartons: 3,
    },
    'hakimi': {
      nom: 'Achraf Hakimi',
      poste: 'Défenseur',
      numero: 2,
      age: 26,
      valeur: 65,
      buts: 4, passes_decisives: 7, ppm: 2.1, minutes: 2500, titu: 28, absences: 0, cartons: 5,
    }
  };

  const defaultJoueur = {
    nom: 'Joueur',
    poste: 'N/A',
    numero: 0,
    age: 0,
    valeur: 0,
    buts: 0, passes_decisives: 0, ppm: 0, minutes: 0, titu: 0, absences: 0, cartons: 0,
  };

  const joueur = joueursData[params.joueur] || defaultJoueur;

  return (
    <main className="min-h-screen bg-gray-50 py-4 md:py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        <Link href={`/ligue1/${params.club}`} className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l'effectif
        </Link>
        
        <div className="bg-white rounded-lg shadow-md p-4 md:p-8 mb-6">
          <div className="flex flex-col md:flex-row justify-between items-start">
            <div>
              <h1 className="text-2xl md:text-4xl font-bold text-blue-900 mb-2">{joueur.nom}</h1>
              <p className="text-lg md:text-xl text-gray-600">{joueur.poste} • #{joueur.numero}</p>
              <div className="flex flex-wrap gap-2 md:gap-4 mt-4 text-sm md:text-base text-gray-600">
                <span>{joueur.age} ans</span>
                <span className="font-semibold text-green-600">{joueur.valeur}M €</span>
              </div>
            </div>
            <div className="text-4xl md:text-6xl font-bold text-gray-200 mt-4 md:mt-0">
              #{joueur.numero}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Statistiques de base</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-900">{joueur.buts}</div>
              <div className="text-sm text-gray-600">Buts</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-900">{joueur.passes_decisives}</div>
              <div className="text-sm text-gray-600">Passes décisives</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-900">{joueur.minutes}</div>
              <div className="text-sm text-gray-600">Minutes jouées</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-900">{joueur.titu}</div>
              <div className="text-sm text-gray-600">Titularisations</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}