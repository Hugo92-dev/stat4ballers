export function slugifyPlayer(name: string): string {
  return name
    .replace(/ø/g, 'o') // Remplacer ø par o
    .replace(/Ø/g, 'O') // Remplacer Ø par O
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Supprimer les accents
    .replace(/[^a-zA-Z0-9]/g, '') // Garder seulement lettres et chiffres
    .replace(/\s+/g, ''); // Supprimer tous les espaces
}