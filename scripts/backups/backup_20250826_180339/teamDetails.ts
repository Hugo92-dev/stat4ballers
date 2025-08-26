// Détails complets de toutes les équipes des 5 grands championnats
// Inclut: stade, capacité, entraîneur, année de fondation et palmarès

export const teamDetails: Record<string, {
  stadium?: string;
  capacity?: number;
  coach?: string;
  founded?: number;
  trophies?: Record<string, number>;
}> = {
  // ========== LIGUE 1 ==========
  'olympique-marseille': {
    stadium: 'Stade Vélodrome',
    capacity: 67000,
    coach: 'Roberto De Zerbi',
    founded: 1899,
    trophies: {
      'Ligue 1': 9,
      'Coupe de France': 10,
      'Coupe de la Ligue': 3,
      'Trophée des Champions': 3,
      'Ligue des Champions': 1,
      'Coupe Intertoto': 1
    }
  },
  'paris-saint-germain': {
    stadium: 'Parc des Princes',
    capacity: 48000,
    coach: 'Luis Enrique',
    founded: 1970,
    trophies: {
      'Ligue 1': 12,
      'Coupe de France': 15,
      'Coupe de la Ligue': 9,
      'Trophée des Champions': 12,
      "Coupe d'Europe des Vainqueurs de Coupe": 1
    }
  },
  'olympique-lyonnais': {
    stadium: 'Groupama Stadium',
    capacity: 59186,
    coach: 'Pierre Sage',
    founded: 1950,
    trophies: {
      'Ligue 1': 7,
      'Coupe de France': 5,
      'Coupe de la Ligue': 1,
      'Trophée des Champions': 8
    }
  },
  'monaco': {
    stadium: 'Stade Louis-II',
    capacity: 18523,
    coach: 'Adi Hütter',
    founded: 1924,
    trophies: {
      'Ligue 1': 8,
      'Coupe de France': 5,
      'Coupe de la Ligue': 1,
      'Trophée des Champions': 4
    }
  },
  'losc-lille': {
    stadium: 'Stade Pierre-Mauroy',
    capacity: 50186,
    coach: 'Bruno Génésio',
    founded: 1944,
    trophies: {
      'Ligue 1': 4,
      'Coupe de France': 6,
      'Coupe de la Ligue': 2
    }
  },
  'nice': {
    stadium: 'Allianz Riviera',
    capacity: 36178,
    coach: 'Franck Haise',
    founded: 1904,
    trophies: {
      'Ligue 1': 4,
      'Coupe de France': 3
    }
  },
  'lens': {
    stadium: 'Stade Bollaert-Delelis',
    capacity: 38223,
    coach: 'Will Still',
    founded: 1906,
    trophies: {
      'Ligue 1': 1,
      'Coupe de France': 1,
      'Coupe de la Ligue': 1
    }
  },
  'rennes': {
    stadium: 'Roazhon Park',
    capacity: 29778,
    coach: 'Julien Stéphan',
    founded: 1901,
    trophies: {
      'Coupe de France': 3,
      'Coupe de la Ligue': 1
    }
  },
  'strasbourg': {
    stadium: 'Stade de la Meinau',
    capacity: 26109,
    coach: 'Patrick Vieira',
    founded: 1906,
    trophies: {
      'Ligue 1': 1,
      'Coupe de France': 3,
      'Coupe de la Ligue': 3
    }
  },
  'nantes': {
    stadium: 'Stade de la Beaujoire',
    capacity: 37473,
    coach: 'Antoine Kombouaré',
    founded: 1943,
    trophies: {
      'Ligue 1': 8,
      'Coupe de France': 4,
      'Trophée des Champions': 3
    }
  },
  'brest': {
    stadium: 'Stade Francis-Le Blé',
    capacity: 15220,
    coach: 'Éric Roy',
    founded: 1950,
    trophies: {}
  },
  'toulouse': {
    stadium: 'Stadium de Toulouse',
    capacity: 33150,
    coach: 'Carles Martínez Novell',
    founded: 1970,
    trophies: {
      'Coupe de France': 1
    }
  },
  'auxerre': {
    stadium: 'Stade Abbé-Deschamps',
    capacity: 18541,
    coach: 'Christophe Pélissier',
    founded: 1905,
    trophies: {
      'Ligue 1': 1,
      'Coupe de France': 4
    }
  },
  'angers-sco': {
    stadium: 'Stade Raymond-Kopa',
    capacity: 18000,
    coach: 'Alexandre Dujeux',
    founded: 1919,
    trophies: {}
  },
  'le-havre': {
    stadium: 'Stade Océane',
    capacity: 25178,
    coach: 'Luka Elsner',
    founded: 1872,
    trophies: {}
  },
  'metz': {
    stadium: 'Stade Saint-Symphorien',
    capacity: 30000,
    coach: 'László Bölöni',
    founded: 1932,
    trophies: {
      'Coupe de France': 2,
      'Coupe de la Ligue': 2
    }
  },
  'lorient': {
    stadium: 'Stade du Moustoir',
    capacity: 18890,
    coach: 'Régis Le Bris',
    founded: 1926,
    trophies: {
      'Coupe de France': 1
    }
  },
  'paris': {
    stadium: 'Stade Charléty',
    capacity: 20000,
    coach: 'Stéphane Gilli',
    founded: 1969,
    trophies: {}
  },

  // ========== PREMIER LEAGUE ==========
  'manchester-united': {
    stadium: 'Old Trafford',
    capacity: 74310,
    coach: 'Erik ten Hag',
    founded: 1878,
    trophies: {
      'Premier League': 20,
      'FA Cup': 13,
      'League Cup': 6,
      'Champions League': 3,
      'Europa League': 1,
      'Cup Winners Cup': 1,
      'UEFA Super Cup': 1,
      'FIFA Club World Cup': 1
    }
  },
  'manchester-city': {
    stadium: 'Etihad Stadium',
    capacity: 53400,
    coach: 'Pep Guardiola',
    founded: 1880,
    trophies: {
      'Premier League': 10,
      'FA Cup': 7,
      'League Cup': 8,
      'Champions League': 1,
      'Cup Winners Cup': 1,
      'FIFA Club World Cup': 1
    }
  },
  'liverpool': {
    stadium: 'Anfield',
    capacity: 61276,
    coach: 'Arne Slot',
    founded: 1892,
    trophies: {
      'Premier League': 19,
      'FA Cup': 8,
      'League Cup': 10,
      'Champions League': 6,
      'Europa League': 3,
      'UEFA Super Cup': 4,
      'FIFA Club World Cup': 1
    }
  },
  'chelsea': {
    stadium: 'Stamford Bridge',
    capacity: 40341,
    coach: 'Enzo Maresca',
    founded: 1905,
    trophies: {
      'Premier League': 6,
      'FA Cup': 8,
      'League Cup': 5,
      'Champions League': 2,
      'Europa League': 2,
      'Cup Winners Cup': 2,
      'UEFA Super Cup': 2,
      'FIFA Club World Cup': 1
    }
  },
  'arsenal': {
    stadium: 'Emirates Stadium',
    capacity: 60704,
    coach: 'Mikel Arteta',
    founded: 1886,
    trophies: {
      'Premier League': 13,
      'FA Cup': 14,
      'League Cup': 2,
      'Cup Winners Cup': 1
    }
  },
  'tottenham-hotspur': {
    stadium: 'Tottenham Hotspur Stadium',
    capacity: 62850,
    coach: 'Ange Postecoglou',
    founded: 1882,
    trophies: {
      'First Division': 2,
      'FA Cup': 8,
      'League Cup': 4,
      'Cup Winners Cup': 1,
      'UEFA Cup': 2
    }
  },
  'newcastle-united': {
    stadium: "St James' Park",
    capacity: 52305,
    coach: 'Eddie Howe',
    founded: 1892,
    trophies: {
      'First Division': 4,
      'FA Cup': 6,
      'Inter-Cities Fairs Cup': 1
    }
  },
  'west-ham-united': {
    stadium: 'London Stadium',
    capacity: 62500,
    coach: 'Julen Lopetegui',
    founded: 1895,
    trophies: {
      'FA Cup': 3,
      'Cup Winners Cup': 1,
      'Conference League': 1
    }
  },
  'everton': {
    stadium: 'Goodison Park',
    capacity: 39572,
    coach: 'Sean Dyche',
    founded: 1878,
    trophies: {
      'First Division': 9,
      'FA Cup': 5,
      'Cup Winners Cup': 1
    }
  },
  'brighton-hove-albion': {
    stadium: 'American Express Stadium',
    capacity: 31876,
    coach: 'Fabian Hürzeler',
    founded: 1901,
    trophies: {}
  },
  'aston-villa': {
    stadium: 'Villa Park',
    capacity: 42657,
    coach: 'Unai Emery',
    founded: 1874,
    trophies: {
      'First Division': 7,
      'FA Cup': 7,
      'League Cup': 5,
      'European Cup': 1,
      'UEFA Super Cup': 1
    }
  },
  'nottingham-forest': {
    stadium: 'City Ground',
    capacity: 30332,
    coach: 'Nuno Espírito Santo',
    founded: 1865,
    trophies: {
      'First Division': 1,
      'FA Cup': 2,
      'League Cup': 4,
      'European Cup': 2,
      'UEFA Super Cup': 1
    }
  },
  'crystal-palace': {
    stadium: 'Selhurst Park',
    capacity: 25486,
    coach: 'Oliver Glasner',
    founded: 1905,
    trophies: {}
  },
  'fulham': {
    stadium: 'Craven Cottage',
    capacity: 29600,
    coach: 'Marco Silva',
    founded: 1879,
    trophies: {
      'UEFA Intertoto Cup': 1
    }
  },
  'brentford': {
    stadium: 'Brentford Community Stadium',
    capacity: 17250,
    coach: 'Thomas Frank',
    founded: 1889,
    trophies: {}
  },
  'wolverhampton-wanderers': {
    stadium: 'Molineux Stadium',
    capacity: 31750,
    coach: "Gary O'Neil",
    founded: 1877,
    trophies: {
      'First Division': 3,
      'FA Cup': 4,
      'League Cup': 2
    }
  },
  'afc-bournemouth': {
    stadium: 'Vitality Stadium',
    capacity: 11307,
    coach: 'Andoni Iraola',
    founded: 1899,
    trophies: {}
  },
  'leeds-united': {
    stadium: 'Elland Road',
    capacity: 37792,
    coach: 'Daniel Farke',
    founded: 1919,
    trophies: {
      'First Division': 3,
      'FA Cup': 1,
      'League Cup': 1,
      'Inter-Cities Fairs Cup': 2
    }
  },
  'sunderland': {
    stadium: 'Stadium of Light',
    capacity: 49000,
    coach: 'Régis Le Bris',
    founded: 1879,
    trophies: {
      'First Division': 6,
      'FA Cup': 2
    }
  },
  'burnley': {
    stadium: 'Turf Moor',
    capacity: 21944,
    coach: 'Scott Parker',
    founded: 1882,
    trophies: {
      'First Division': 2,
      'FA Cup': 1
    }
  },

  // ========== LA LIGA ==========
  'real-madrid': {
    stadium: 'Santiago Bernabéu',
    capacity: 85000,
    coach: 'Carlo Ancelotti',
    founded: 1902,
    trophies: {
      'La Liga': 36,
      'Copa del Rey': 20,
      'Supercopa de España': 13,
      'Champions League': 15,
      'Europa League': 2,
      'UEFA Super Cup': 5,
      'FIFA Club World Cup': 8
    }
  },
  'fc-barcelona': {
    stadium: 'Spotify Camp Nou',
    capacity: 99354,
    coach: 'Hansi Flick',
    founded: 1899,
    trophies: {
      'La Liga': 27,
      'Copa del Rey': 31,
      'Supercopa de España': 14,
      'Champions League': 5,
      'Cup Winners Cup': 4,
      'UEFA Super Cup': 5,
      'FIFA Club World Cup': 3
    }
  },
  'atletico-madrid': {
    stadium: 'Cívitas Metropolitano',
    capacity: 70460,
    coach: 'Diego Simeone',
    founded: 1903,
    trophies: {
      'La Liga': 11,
      'Copa del Rey': 10,
      'Supercopa de España': 2,
      'Europa League': 3,
      'UEFA Super Cup': 3,
      'Cup Winners Cup': 1
    }
  },
  'sevilla': {
    stadium: 'Ramón Sánchez Pizjuán',
    capacity: 43883,
    coach: 'Francisco García Pimienta',
    founded: 1890,
    trophies: {
      'La Liga': 1,
      'Copa del Rey': 5,
      'Europa League': 7,
      'UEFA Super Cup': 1
    }
  },
  'valencia': {
    stadium: 'Mestalla',
    capacity: 48600,
    coach: 'Rubén Baraja',
    founded: 1919,
    trophies: {
      'La Liga': 6,
      'Copa del Rey': 8,
      'UEFA Cup': 1,
      'Cup Winners Cup': 1,
      'UEFA Super Cup': 2
    }
  },
  'villarreal': {
    stadium: 'Estadio de la Cerámica',
    capacity: 23500,
    coach: 'Marcelino García Toral',
    founded: 1923,
    trophies: {
      'Europa League': 1,
      'UEFA Intertoto Cup': 2
    }
  },
  'athletic-club': {
    stadium: 'San Mamés',
    capacity: 53289,
    coach: 'Ernesto Valverde',
    founded: 1898,
    trophies: {
      'La Liga': 8,
      'Copa del Rey': 24,
      'Supercopa de España': 3
    }
  },
  'real-sociedad': {
    stadium: 'Reale Arena',
    capacity: 39500,
    coach: 'Imanol Alguacil',
    founded: 1909,
    trophies: {
      'La Liga': 2,
      'Copa del Rey': 3,
      'Supercopa de España': 1
    }
  },
  'real-betis': {
    stadium: 'Benito Villamarín',
    capacity: 60721,
    coach: 'Manuel Pellegrini',
    founded: 1907,
    trophies: {
      'La Liga': 1,
      'Copa del Rey': 3
    }
  },
  'osasuna': {
    stadium: 'El Sadar',
    capacity: 23576,
    coach: 'Vicente Moreno',
    founded: 1920,
    trophies: {}
  },
  'celta-de-vigo': {
    stadium: 'Balaídos',
    capacity: 24870,
    coach: 'Claudio Giráldez',
    founded: 1923,
    trophies: {
      'UEFA Intertoto Cup': 1
    }
  },
  'rayo-vallecano': {
    stadium: 'Campo de Fútbol de Vallecas',
    capacity: 14708,
    coach: 'Iñigo Pérez',
    founded: 1924,
    trophies: {}
  },
  'getafe': {
    stadium: 'Coliseum',
    capacity: 17393,
    coach: 'José Bordalás',
    founded: 1946,
    trophies: {}
  },
  'mallorca': {
    stadium: 'Estadi Mallorca Son Moix',
    capacity: 23142,
    coach: 'Jagoba Arrasate',
    founded: 1916,
    trophies: {
      'Copa del Rey': 1
    }
  },
  'deportivo-alaves': {
    stadium: 'Mendizorrotza',
    capacity: 19840,
    coach: 'Luis García Plaza',
    founded: 1921,
    trophies: {}
  },
  'espanyol': {
    stadium: 'RCDE Stadium',
    capacity: 40000,
    coach: 'Manolo González',
    founded: 1900,
    trophies: {
      'Copa del Rey': 4
    }
  },
  'girona': {
    stadium: 'Estadi Montilivi',
    capacity: 14624,
    coach: 'Míchel',
    founded: 1930,
    trophies: {}
  },
  'levante': {
    stadium: 'Ciutat de València',
    capacity: 26354,
    coach: 'Julián Calero',
    founded: 1909,
    trophies: {}
  },
  'elche': {
    stadium: 'Martínez Valero',
    capacity: 36017,
    coach: 'Eder Sarabia',
    founded: 1923,
    trophies: {}
  },
  'real-oviedo': {
    stadium: 'Carlos Tartiere',
    capacity: 30500,
    coach: 'Javi Calleja',
    founded: 1926,
    trophies: {}
  },

  // ========== SERIE A ==========
  'juventus': {
    stadium: 'Allianz Stadium',
    capacity: 41507,
    coach: 'Thiago Motta',
    founded: 1897,
    trophies: {
      'Serie A': 36,
      'Coppa Italia': 15,
      'Supercoppa Italiana': 9,
      'Champions League': 2,
      'Europa League': 3,
      'Cup Winners Cup': 1,
      'UEFA Super Cup': 2
    }
  },
  'milan': {
    stadium: 'San Siro',
    capacity: 80018,
    coach: 'Paulo Fonseca',
    founded: 1899,
    trophies: {
      'Serie A': 19,
      'Coppa Italia': 5,
      'Supercoppa Italiana': 7,
      'Champions League': 7,
      'Cup Winners Cup': 2,
      'UEFA Super Cup': 5,
      'FIFA Club World Cup': 4
    }
  },
  'inter': {
    stadium: 'San Siro',
    capacity: 80018,
    coach: 'Simone Inzaghi',
    founded: 1908,
    trophies: {
      'Serie A': 20,
      'Coppa Italia': 9,
      'Supercoppa Italiana': 8,
      'Champions League': 3,
      'Europa League': 3,
      'FIFA Club World Cup': 3
    }
  },
  'napoli': {
    stadium: 'Stadio Diego Armando Maradona',
    capacity: 54726,
    coach: 'Antonio Conte',
    founded: 1926,
    trophies: {
      'Serie A': 3,
      'Coppa Italia': 6,
      'Supercoppa Italiana': 2,
      'UEFA Cup': 1
    }
  },
  'roma': {
    stadium: 'Stadio Olimpico',
    capacity: 70634,
    coach: 'Ivan Jurić',
    founded: 1927,
    trophies: {
      'Serie A': 3,
      'Coppa Italia': 9,
      'Supercoppa Italiana': 2,
      'Conference League': 1
    }
  },
  'lazio': {
    stadium: 'Stadio Olimpico',
    capacity: 70634,
    coach: 'Marco Baroni',
    founded: 1900,
    trophies: {
      'Serie A': 2,
      'Coppa Italia': 7,
      'Supercoppa Italiana': 5,
      'Cup Winners Cup': 1,
      'UEFA Super Cup': 1
    }
  },
  'fiorentina': {
    stadium: 'Artemio Franchi',
    capacity: 43147,
    coach: 'Raffaele Palladino',
    founded: 1926,
    trophies: {
      'Serie A': 2,
      'Coppa Italia': 6,
      'Cup Winners Cup': 1
    }
  },
  'atalanta': {
    stadium: 'Gewiss Stadium',
    capacity: 21747,
    coach: 'Gian Piero Gasperini',
    founded: 1907,
    trophies: {
      'Coppa Italia': 1,
      'Europa League': 1
    }
  },
  'bologna': {
    stadium: "Stadio Renato Dall'Ara",
    capacity: 38279,
    coach: 'Vincenzo Italiano',
    founded: 1909,
    trophies: {
      'Serie A': 7,
      'Coppa Italia': 2,
      'UEFA Intertoto Cup': 1
    }
  },
  'torino': {
    stadium: 'Stadio Olimpico Grande Torino',
    capacity: 28177,
    coach: 'Paolo Vanoli',
    founded: 1906,
    trophies: {
      'Serie A': 7,
      'Coppa Italia': 5
    }
  },
  'udinese': {
    stadium: 'Bluenergy Stadium',
    capacity: 25144,
    coach: 'Kosta Runjaić',
    founded: 1896,
    trophies: {}
  },
  'genoa': {
    stadium: 'Luigi Ferraris',
    capacity: 36599,
    coach: 'Alberto Gilardino',
    founded: 1893,
    trophies: {
      'Serie A': 9,
      'Coppa Italia': 1
    }
  },
  'como': {
    stadium: 'Stadio Giuseppe Sinigaglia',
    capacity: 13602,
    coach: 'Cesc Fàbregas',
    founded: 1907,
    trophies: {}
  },
  'hellas-verona': {
    stadium: "Stadio Marc'Antonio Bentegodi",
    capacity: 39211,
    coach: 'Paolo Zanetti',
    founded: 1903,
    trophies: {
      'Serie A': 1
    }
  },
  'parma': {
    stadium: 'Stadio Ennio Tardini',
    capacity: 22352,
    coach: 'Fabio Pecchia',
    founded: 1913,
    trophies: {
      'Coppa Italia': 3,
      'Cup Winners Cup': 1,
      'UEFA Cup': 2,
      'UEFA Super Cup': 1
    }
  },
  'cagliari': {
    stadium: 'Unipol Domus',
    capacity: 16416,
    coach: 'Davide Nicola',
    founded: 1920,
    trophies: {
      'Serie A': 1
    }
  },
  'lecce': {
    stadium: 'Via del Mare',
    capacity: 31533,
    coach: 'Luca Gotti',
    founded: 1908,
    trophies: {}
  },
  'sassuolo': {
    stadium: 'Mapei Stadium',
    capacity: 21584,
    coach: 'Fabio Grosso',
    founded: 1920,
    trophies: {}
  },
  'cremonese': {
    stadium: 'Giovanni Zini',
    capacity: 16003,
    coach: 'Giovanni Stroppa',
    founded: 1903,
    trophies: {}
  },
  'pisa': {
    stadium: 'Arena Garibaldi',
    capacity: 10000,
    coach: 'Filippo Inzaghi',
    founded: 1909,
    trophies: {}
  },

  // ========== BUNDESLIGA ==========
  'fc-bayern-munchen': {
    stadium: 'Allianz Arena',
    capacity: 75024,
    coach: 'Vincent Kompany',
    founded: 1900,
    trophies: {
      'Bundesliga': 33,
      'DFB-Pokal': 20,
      'DFL-Supercup': 11,
      'Champions League': 6,
      'Europa League': 1,
      'Cup Winners Cup': 1,
      'UEFA Super Cup': 2,
      'FIFA Club World Cup': 2
    }
  },
  'borussia-dortmund': {
    stadium: 'Signal Iduna Park',
    capacity: 81365,
    coach: 'Nuri Şahin',
    founded: 1909,
    trophies: {
      'Bundesliga': 8,
      'DFB-Pokal': 5,
      'DFL-Supercup': 6,
      'Champions League': 1,
      'Cup Winners Cup': 1,
      'FIFA Club World Cup': 1
    }
  },
  'bayer-04-leverkusen': {
    stadium: 'BayArena',
    capacity: 30210,
    coach: 'Xabi Alonso',
    founded: 1904,
    trophies: {
      'Bundesliga': 1,
      'DFB-Pokal': 1,
      'UEFA Cup': 1
    }
  },
  'rb-leipzig': {
    stadium: 'Red Bull Arena',
    capacity: 47069,
    coach: 'Marco Rose',
    founded: 2009,
    trophies: {
      'DFB-Pokal': 2,
      'DFL-Supercup': 1
    }
  },
  'eintracht-frankfurt': {
    stadium: 'Deutsche Bank Park',
    capacity: 58000,
    coach: 'Dino Toppmöller',
    founded: 1899,
    trophies: {
      'Bundesliga': 1,
      'DFB-Pokal': 5,
      'UEFA Cup': 1,
      'Europa League': 1
    }
  },
  'vfb-stuttgart': {
    stadium: 'Mercedes-Benz Arena',
    capacity: 60449,
    coach: 'Sebastian Hoeneß',
    founded: 1893,
    trophies: {
      'Bundesliga': 5,
      'DFB-Pokal': 3,
      'UEFA Intertoto Cup': 1
    }
  },
  'vfl-wolfsburg': {
    stadium: 'Volkswagen Arena',
    capacity: 30000,
    coach: 'Ralph Hasenhüttl',
    founded: 1945,
    trophies: {
      'Bundesliga': 1,
      'DFB-Pokal': 1,
      'DFL-Supercup': 1
    }
  },
  'sc-freiburg': {
    stadium: 'Europa-Park Stadion',
    capacity: 34700,
    coach: 'Julian Schuster',
    founded: 1904,
    trophies: {}
  },
  'fsv-mainz-05': {
    stadium: 'Mewa Arena',
    capacity: 33305,
    coach: 'Bo Henriksen',
    founded: 1905,
    trophies: {}
  },
  'werder-bremen': {
    stadium: 'Weserstadion',
    capacity: 42100,
    coach: 'Ole Werner',
    founded: 1899,
    trophies: {
      'Bundesliga': 4,
      'DFB-Pokal': 6,
      'Cup Winners Cup': 1
    }
  },
  'tsg-hoffenheim': {
    stadium: 'PreZero Arena',
    capacity: 30150,
    coach: 'Pellegrino Matarazzo',
    founded: 1899,
    trophies: {}
  },
  'fc-augsburg': {
    stadium: 'WWK Arena',
    capacity: 30660,
    coach: 'Jess Thorup',
    founded: 1907,
    trophies: {}
  },
  'borussia-monchengladbach': {
    stadium: 'Borussia-Park',
    capacity: 54042,
    coach: 'Gerardo Seoane',
    founded: 1900,
    trophies: {
      'Bundesliga': 5,
      'DFB-Pokal': 3,
      'UEFA Cup': 2
    }
  },
  'fc-union-berlin': {
    stadium: 'Stadion An der Alten Försterei',
    capacity: 22012,
    coach: 'Bo Svensson',
    founded: 1966,
    trophies: {}
  },
  'fc-koln': {
    stadium: 'RheinEnergieStadion',
    capacity: 50000,
    coach: 'Gerhard Struber',
    founded: 1948,
    trophies: {
      'Bundesliga': 2,
      'DFB-Pokal': 4
    }
  },
  'heidenheim': {
    stadium: 'Voith-Arena',
    capacity: 15000,
    coach: 'Frank Schmidt',
    founded: 1846,
    trophies: {}
  },
  'st-pauli': {
    stadium: 'Millerntor-Stadion',
    capacity: 29546,
    coach: 'Alexander Blessin',
    founded: 1910,
    trophies: {}
  },
  'hamburger-sv': {
    stadium: 'Volksparkstadion',
    capacity: 57000,
    coach: 'Steffen Baumgart',
    founded: 1887,
    trophies: {
      'Bundesliga': 6,
      'DFB-Pokal': 3,
      'European Cup': 1,
      'Cup Winners Cup': 1
    }
  }
};