export interface Player {
  displayName?: string;
  id: number;
  name: string;
  fullName?: string;
  jersey?: number;
  position: string;
  dateOfBirth?: string;
  nationality?: string;
  height?: number;
  weight?: number;
  image?: string;
  age?: number;
  number?: number;
  playerSlug?: string;
  nom?: string;
  position_id?: number;
  numero?: number;
  nationalite?: string;
  taille?: number;
  poids?: number;
}

export interface Team {
  id: number;
  name: string;
  slug: string;
  players: Player[];
  stadium?: string;
  colors?: {
    primary?: string;
    secondary?: string;
  };
}