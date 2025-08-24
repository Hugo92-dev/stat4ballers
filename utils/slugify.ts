/**
 * Convertit un nom de joueur en slug URL-friendly
 * Exemples:
 * - "Pierre-Emerick Aubameyang" -> "pierre-emerick-aubameyang"
 * - "Kylian Mbappé" -> "kylian-mbappe"
 * - "João Félix" -> "joao-felix"
 */
export function slugifyPlayer(name: string): string {
  if (!name) return '';
  
  return name
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Supprimer les accents
    .replace(/[øØ]/g, 'o')
    .replace(/[æÆ]/g, 'ae')
    .replace(/[ßś]/g, 's')
    .replace(/[^a-z0-9\s-]/g, '') // Garder lettres, chiffres, espaces et tirets
    .replace(/\s+/g, '-') // Remplacer espaces par tirets
    .replace(/-+/g, '-') // Réduire les tirets multiples
    .replace(/^-|-$/g, ''); // Supprimer tirets début/fin
}