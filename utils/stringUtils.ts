export function normalizeString(str: string): string {
  return str
    .toLowerCase()
    .replace(/ø/g, "o")
    .replace(/æ/g, "ae")
    .replace(/å/g, "a")
    .replace(/ß/g, "ss")
    .replace(/ñ/g, "n")
    .replace(/ç/g, "c")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

export function normalizeSearchQuery(query: string): string {
  return normalizeString(query.trim());
}

export function normalizePlayerName(name: string): string {
  return normalizeString(name);
}

export function fuzzyMatch(searchTerm: string, targetName: string): boolean {
  const normalizedSearch = normalizeSearchQuery(searchTerm);
  const normalizedTarget = normalizePlayerName(targetName);
  
  return normalizedTarget.includes(normalizedSearch) || 
         targetName.toLowerCase().includes(searchTerm.toLowerCase());
}