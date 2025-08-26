// Détails simplifiés de toutes les équipes (sans palmarès)
// Stade, capacité, entraîneur et année de fondation uniquement

export const teamDetails: Record<string, {
  stadium?: string;
  capacity?: number;
  coach?: string;
  founded?: number;
}> = {
  // ========== LIGUE 1 ==========
  'olympique-marseille': {
    stadium: 'Stade Vélodrome',
    capacity: 67394,
    coach: 'Roberto De Zerbi',
    founded: 1899
  },
  'paris-saint-germain': {
    stadium: 'Parc des Princes',
    capacity: 47929,
    coach: 'Luis Enrique',
    founded: 1970
  },
  'olympique-lyonnais': {
    stadium: 'Groupama Stadium',
    capacity: 59186,
    coach: 'Pierre Sage',
    founded: 1950
  },
  'monaco': {
    stadium: 'Stade Louis-II',
    capacity: 18523,
    coach: 'Adi Hütter',
    founded: 1924
  },
  'losc-lille': {
    stadium: 'Stade Pierre-Mauroy',
    capacity: 50157,
    coach: 'Bruno Génésio',
    founded: 1944
  },
  'nice': {
    stadium: 'Allianz Riviera',
    capacity: 36178,
    coach: 'Franck Haise',
    founded: 1904
  },
  'lens': {
    stadium: 'Stade Bollaert-Delelis',
    capacity: 38223,
    coach: 'Will Still',
    founded: 1906
  },
  'rennes': {
    stadium: 'Roazhon Park',
    capacity: 29778,
    coach: 'Julien Stéphan',
    founded: 1901
  },
  'strasbourg': {
    stadium: 'Stade de la Meinau',
    capacity: 26109,
    coach: 'Patrick Vieira',
    founded: 1906
  },
  'nantes': {
    stadium: 'Stade de la Beaujoire',
    capacity: 37473,
    coach: 'Antoine Kombouaré',
    founded: 1943
  },
  'brest': {
    stadium: 'Stade Francis-Le Blé',
    capacity: 15220,
    coach: 'Éric Roy',
    founded: 1950
  },
  'toulouse': {
    stadium: 'Stadium de Toulouse',
    capacity: 33150,
    coach: 'Carles Martínez Novell',
    founded: 1970
  },
  'auxerre': {
    stadium: 'Stade Abbé-Deschamps',
    capacity: 18541,
    coach: 'Christophe Pélissier',
    founded: 1905
  },
  'angers-sco': {
    stadium: 'Stade Raymond-Kopa',
    capacity: 18000,
    coach: 'Alexandre Dujeux',
    founded: 1919
  },
  'le-havre': {
    stadium: 'Stade Océane',
    capacity: 25178,
    coach: 'Luka Elsner',
    founded: 1872
  },
  'metz': {
    stadium: 'Stade Saint-Symphorien',
    capacity: 30000,
    coach: 'László Bölöni',
    founded: 1932
  },
  'lorient': {
    stadium: 'Stade du Moustoir',
    capacity: 18890,
    coach: 'Régis Le Bris',
    founded: 1926
  },
  'paris': {
    stadium: 'Stade Charléty',
    capacity: 20000,
    coach: 'Stéphane Gilli',
    founded: 1969
  },

  // ========== PREMIER LEAGUE ==========
  'manchester-united': {
    stadium: 'Old Trafford',
    capacity: 74310,
    coach: 'Erik ten Hag',
    founded: 1878
  },
  'manchester-city': {
    stadium: 'Etihad Stadium',
    capacity: 53400,
    coach: 'Pep Guardiola',
    founded: 1880
  },
  'liverpool': {
    stadium: 'Anfield',
    capacity: 61276,
    coach: 'Arne Slot',
    founded: 1892
  },
  'chelsea': {
    stadium: 'Stamford Bridge',
    capacity: 40341,
    coach: 'Enzo Maresca',
    founded: 1905
  },
  'arsenal': {
    stadium: 'Emirates Stadium',
    capacity: 60704,
    coach: 'Mikel Arteta',
    founded: 1886
  },
  'tottenham-hotspur': {
    stadium: 'Tottenham Hotspur Stadium',
    capacity: 62850,
    coach: 'Ange Postecoglou',
    founded: 1882
  },
  'newcastle-united': {
    stadium: "St James' Park",
    capacity: 52305,
    coach: 'Eddie Howe',
    founded: 1892
  },
  'west-ham-united': {
    stadium: 'London Stadium',
    capacity: 62500,
    coach: 'Julen Lopetegui',
    founded: 1895
  },
  'everton': {
    stadium: 'Goodison Park',
    capacity: 39572,
    coach: 'Sean Dyche',
    founded: 1878
  },
  'brighton-hove-albion': {
    stadium: 'American Express Stadium',
    capacity: 31876,
    coach: 'Fabian Hürzeler',
    founded: 1901
  },
  'aston-villa': {
    stadium: 'Villa Park',
    capacity: 42657,
    coach: 'Unai Emery',
    founded: 1874
  },
  'nottingham-forest': {
    stadium: 'City Ground',
    capacity: 30332,
    coach: 'Nuno Espírito Santo',
    founded: 1865
  },
  'crystal-palace': {
    stadium: 'Selhurst Park',
    capacity: 25486,
    coach: 'Oliver Glasner',
    founded: 1905
  },
  'fulham': {
    stadium: 'Craven Cottage',
    capacity: 29600,
    coach: 'Marco Silva',
    founded: 1879
  },
  'brentford': {
    stadium: 'Brentford Community Stadium',
    capacity: 17250,
    coach: 'Thomas Frank',
    founded: 1889
  },
  'wolverhampton-wanderers': {
    stadium: 'Molineux Stadium',
    capacity: 31750,
    coach: "Gary O'Neil",
    founded: 1877
  },
  'afc-bournemouth': {
    stadium: 'Vitality Stadium',
    capacity: 11307,
    coach: 'Andoni Iraola',
    founded: 1899
  },
  'leeds-united': {
    stadium: 'Elland Road',
    capacity: 37792,
    coach: 'Daniel Farke',
    founded: 1919
  },
  'sunderland': {
    stadium: 'Stadium of Light',
    capacity: 49000,
    coach: 'Régis Le Bris',
    founded: 1879
  },
  'burnley': {
    stadium: 'Turf Moor',
    capacity: 21944,
    coach: 'Scott Parker',
    founded: 1882
  },

  // ========== LA LIGA ==========
  'real-madrid': {
    stadium: 'Santiago Bernabéu',
    capacity: 85000,
    coach: 'Carlo Ancelotti',
    founded: 1902
  },
  'fc-barcelona': {
    stadium: 'Spotify Camp Nou',
    capacity: 99354,
    coach: 'Hansi Flick',
    founded: 1899
  },
  'atletico-madrid': {
    stadium: 'Cívitas Metropolitano',
    capacity: 70460,
    coach: 'Diego Simeone',
    founded: 1903
  },
  'sevilla': {
    stadium: 'Ramón Sánchez Pizjuán',
    capacity: 43883,
    coach: 'Francisco García Pimienta',
    founded: 1890
  },
  'valencia': {
    stadium: 'Mestalla',
    capacity: 48600,
    coach: 'Rubén Baraja',
    founded: 1919
  },
  'villarreal': {
    stadium: 'Estadio de la Cerámica',
    capacity: 23500,
    coach: 'Marcelino García Toral',
    founded: 1923
  },
  'athletic-club': {
    stadium: 'San Mamés',
    capacity: 53289,
    coach: 'Ernesto Valverde',
    founded: 1898
  },
  'real-sociedad': {
    stadium: 'Reale Arena',
    capacity: 39500,
    coach: 'Imanol Alguacil',
    founded: 1909
  },
  'real-betis': {
    stadium: 'Benito Villamarín',
    capacity: 60721,
    coach: 'Manuel Pellegrini',
    founded: 1907
  },
  'osasuna': {
    stadium: 'El Sadar',
    capacity: 23576,
    coach: 'Vicente Moreno',
    founded: 1920
  },
  'celta-de-vigo': {
    stadium: 'Balaídos',
    capacity: 24870,
    coach: 'Claudio Giráldez',
    founded: 1923
  },
  'rayo-vallecano': {
    stadium: 'Campo de Fútbol de Vallecas',
    capacity: 14708,
    coach: 'Iñigo Pérez',
    founded: 1924
  },
  'getafe': {
    stadium: 'Coliseum',
    capacity: 17393,
    coach: 'José Bordalás',
    founded: 1946
  },
  'mallorca': {
    stadium: 'Estadi Mallorca Son Moix',
    capacity: 23142,
    coach: 'Jagoba Arrasate',
    founded: 1916
  },
  'deportivo-alaves': {
    stadium: 'Mendizorrotza',
    capacity: 19840,
    coach: 'Luis García Plaza',
    founded: 1921
  },
  'espanyol': {
    stadium: 'RCDE Stadium',
    capacity: 40000,
    coach: 'Manolo González',
    founded: 1900
  },
  'girona': {
    stadium: 'Estadi Montilivi',
    capacity: 14624,
    coach: 'Míchel',
    founded: 1930
  },
  'levante': {
    stadium: 'Ciutat de València',
    capacity: 26354,
    coach: 'Julián Calero',
    founded: 1909
  },
  'elche': {
    stadium: 'Martínez Valero',
    capacity: 36017,
    coach: 'Eder Sarabia',
    founded: 1923
  },
  'real-oviedo': {
    stadium: 'Carlos Tartiere',
    capacity: 30500,
    coach: 'Javi Calleja',
    founded: 1926
  },

  // ========== SERIE A ==========
  'juventus': {
    stadium: 'Allianz Stadium',
    capacity: 41507,
    coach: 'Thiago Motta',
    founded: 1897
  },
  'milan': {
    stadium: 'San Siro',
    capacity: 80018,
    coach: 'Paulo Fonseca',
    founded: 1899
  },
  'inter': {
    stadium: 'San Siro',
    capacity: 80018,
    coach: 'Simone Inzaghi',
    founded: 1908
  },
  'napoli': {
    stadium: 'Stadio Diego Armando Maradona',
    capacity: 54726,
    coach: 'Antonio Conte',
    founded: 1926
  },
  'roma': {
    stadium: 'Stadio Olimpico',
    capacity: 70634,
    coach: 'Ivan Jurić',
    founded: 1927
  },
  'lazio': {
    stadium: 'Stadio Olimpico',
    capacity: 70634,
    coach: 'Marco Baroni',
    founded: 1900
  },
  'fiorentina': {
    stadium: 'Artemio Franchi',
    capacity: 43147,
    coach: 'Raffaele Palladino',
    founded: 1926
  },
  'atalanta': {
    stadium: 'Gewiss Stadium',
    capacity: 21747,
    coach: 'Gian Piero Gasperini',
    founded: 1907
  },
  'bologna': {
    stadium: "Stadio Renato Dall'Ara",
    capacity: 38279,
    coach: 'Vincenzo Italiano',
    founded: 1909
  },
  'torino': {
    stadium: 'Stadio Olimpico Grande Torino',
    capacity: 28177,
    coach: 'Paolo Vanoli',
    founded: 1906
  },
  'udinese': {
    stadium: 'Bluenergy Stadium',
    capacity: 25144,
    coach: 'Kosta Runjaić',
    founded: 1896
  },
  'genoa': {
    stadium: 'Luigi Ferraris',
    capacity: 36599,
    coach: 'Alberto Gilardino',
    founded: 1893
  },
  'como': {
    stadium: 'Stadio Giuseppe Sinigaglia',
    capacity: 13602,
    coach: 'Cesc Fàbregas',
    founded: 1907
  },
  'hellas-verona': {
    stadium: "Stadio Marc'Antonio Bentegodi",
    capacity: 39211,
    coach: 'Paolo Zanetti',
    founded: 1903
  },
  'parma': {
    stadium: 'Stadio Ennio Tardini',
    capacity: 22352,
    coach: 'Fabio Pecchia',
    founded: 1913
  },
  'cagliari': {
    stadium: 'Unipol Domus',
    capacity: 16416,
    coach: 'Davide Nicola',
    founded: 1920
  },
  'lecce': {
    stadium: 'Via del Mare',
    capacity: 31533,
    coach: 'Luca Gotti',
    founded: 1908
  },
  'sassuolo': {
    stadium: 'Mapei Stadium',
    capacity: 21584,
    coach: 'Fabio Grosso',
    founded: 1920
  },
  'cremonese': {
    stadium: 'Giovanni Zini',
    capacity: 16003,
    coach: 'Giovanni Stroppa',
    founded: 1903
  },
  'pisa': {
    stadium: 'Arena Garibaldi',
    capacity: 10000,
    coach: 'Filippo Inzaghi',
    founded: 1909
  },

  // ========== BUNDESLIGA ==========
  'fc-bayern-munchen': {
    stadium: 'Allianz Arena',
    capacity: 75024,
    coach: 'Vincent Kompany',
    founded: 1900
  },
  'borussia-dortmund': {
    stadium: 'Signal Iduna Park',
    capacity: 81365,
    coach: 'Nuri Şahin',
    founded: 1909
  },
  'bayer-04-leverkusen': {
    stadium: 'BayArena',
    capacity: 30210,
    coach: 'Xabi Alonso',
    founded: 1904
  },
  'rb-leipzig': {
    stadium: 'Red Bull Arena',
    capacity: 47069,
    coach: 'Marco Rose',
    founded: 2009
  },
  'eintracht-frankfurt': {
    stadium: 'Deutsche Bank Park',
    capacity: 58000,
    coach: 'Dino Toppmöller',
    founded: 1899
  },
  'vfb-stuttgart': {
    stadium: 'Mercedes-Benz Arena',
    capacity: 60449,
    coach: 'Sebastian Hoeneß',
    founded: 1893
  },
  'vfl-wolfsburg': {
    stadium: 'Volkswagen Arena',
    capacity: 30000,
    coach: 'Ralph Hasenhüttl',
    founded: 1945
  },
  'sc-freiburg': {
    stadium: 'Europa-Park Stadion',
    capacity: 34700,
    coach: 'Julian Schuster',
    founded: 1904
  },
  'fsv-mainz-05': {
    stadium: 'Mewa Arena',
    capacity: 33305,
    coach: 'Bo Henriksen',
    founded: 1905
  },
  'werder-bremen': {
    stadium: 'Weserstadion',
    capacity: 42100,
    coach: 'Ole Werner',
    founded: 1899
  },
  'tsg-hoffenheim': {
    stadium: 'PreZero Arena',
    capacity: 30150,
    coach: 'Pellegrino Matarazzo',
    founded: 1899
  },
  'fc-augsburg': {
    stadium: 'WWK Arena',
    capacity: 30660,
    coach: 'Jess Thorup',
    founded: 1907
  },
  'borussia-monchengladbach': {
    stadium: 'Borussia-Park',
    capacity: 54042,
    coach: 'Gerardo Seoane',
    founded: 1900
  },
  'fc-union-berlin': {
    stadium: 'Stadion An der Alten Försterei',
    capacity: 22012,
    coach: 'Bo Svensson',
    founded: 1966
  },
  'fc-koln': {
    stadium: 'RheinEnergieStadion',
    capacity: 50000,
    coach: 'Gerhard Struber',
    founded: 1948
  },
  'heidenheim': {
    stadium: 'Voith-Arena',
    capacity: 15000,
    coach: 'Frank Schmidt',
    founded: 1846
  },
  'st-pauli': {
    stadium: 'Millerntor-Stadion',
    capacity: 29546,
    coach: 'Alexander Blessin',
    founded: 1910
  },
  'hamburger-sv': {
    stadium: 'Volksparkstadion',
    capacity: 57000,
    coach: 'Steffen Baumgart',
    founded: 1887
  }
};