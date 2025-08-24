// Détails des équipes (stade, coach, palmarès)
// Ces données sont statiques car elles changent rarement

export const teamDetails: Record<string, {
  stadium?: string;
  capacity?: number;
  coach?: string;
  founded?: number;
  trophies?: Record<string, number>;
}> = {
  // Ligue 1
  'marseille': {
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
  'psg': {
    stadium: 'Parc des Princes',
    capacity: 48000,
    coach: 'Luis Enrique',
    founded: 1970,
    trophies: {
      'Ligue 1': 12,
      'Coupe de France': 14,
      'Coupe de la Ligue': 9,
      'Trophée des Champions': 11,
      'Coupe des Coupes': 1
    }
  },
  'lyon': {
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
  'lille': {
    stadium: 'Stade Pierre-Mauroy',
    capacity: 50000,
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
    capacity: 35624,
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
  'angers': {
    stadium: 'Stade Raymond-Kopa',
    capacity: 18752,
    coach: 'Alexandre Dujeux',
    founded: 1919,
    trophies: {}
  },
  'le-havre': {
    stadium: 'Stade Océane',
    capacity: 25178,
    coach: 'Didier Digard',
    founded: 1872,
    trophies: {}
  },
  
  // Premier League
  'manchester-united': {
    stadium: 'Old Trafford',
    capacity: 74879,
    coach: 'Erik ten Hag',
    founded: 1878,
    trophies: {
      'Premier League': 20,
      'FA Cup': 13,
      'League Cup': 6,
      'Champions League': 3,
      'Europa League': 1,
      'Cup Winners Cup': 1,
      'Super Cup': 1,
      'Club World Cup': 1
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
      'Club World Cup': 1
    }
  },
  'liverpool': {
    stadium: 'Anfield',
    capacity: 61015,
    coach: 'Arne Slot',
    founded: 1892,
    trophies: {
      'Premier League': 19,
      'FA Cup': 8,
      'League Cup': 10,
      'Champions League': 6,
      'Europa League': 3,
      'Super Cup': 4,
      'Club World Cup': 1
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
      'Super Cup': 2,
      'Club World Cup': 1
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
  'tottenham': {
    stadium: 'Tottenham Hotspur Stadium',
    capacity: 62850,
    coach: 'Ange Postecoglou',
    founded: 1882,
    trophies: {
      'Premier League': 2,
      'FA Cup': 8,
      'League Cup': 4,
      'Cup Winners Cup': 1,
      'UEFA Cup': 2
    }
  },
  
  // La Liga
  'real-madrid': {
    stadium: 'Santiago Bernabéu',
    capacity: 81044,
    coach: 'Carlo Ancelotti',
    founded: 1902,
    trophies: {
      'La Liga': 36,
      'Copa del Rey': 20,
      'Supercopa': 13,
      'Champions League': 15,
      'Europa League': 2,
      'Super Cup': 5,
      'Club World Cup': 8
    }
  },
  'barcelona': {
    stadium: 'Camp Nou',
    capacity: 99354,
    coach: 'Hansi Flick',
    founded: 1899,
    trophies: {
      'La Liga': 27,
      'Copa del Rey': 31,
      'Supercopa': 14,
      'Champions League': 5,
      'Cup Winners Cup': 4,
      'Super Cup': 5,
      'Club World Cup': 3
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
      'Supercopa': 2,
      'Europa League': 3,
      'Super Cup': 3,
      'Cup Winners Cup': 1
    }
  },
  
  // Serie A
  'juventus': {
    stadium: 'Allianz Stadium',
    capacity: 41507,
    coach: 'Thiago Motta',
    founded: 1897,
    trophies: {
      'Serie A': 36,
      'Coppa Italia': 14,
      'Supercoppa': 9,
      'Champions League': 2,
      'Europa League': 3,
      'Cup Winners Cup': 1,
      'Super Cup': 2
    }
  },
  'milan': {
    stadium: 'San Siro',
    capacity: 75923,
    coach: 'Paulo Fonseca',
    founded: 1899,
    trophies: {
      'Serie A': 19,
      'Coppa Italia': 5,
      'Supercoppa': 7,
      'Champions League': 7,
      'Cup Winners Cup': 2,
      'Super Cup': 5,
      'Club World Cup': 4
    }
  },
  'inter': {
    stadium: 'San Siro',
    capacity: 75923,
    coach: 'Simone Inzaghi',
    founded: 1908,
    trophies: {
      'Serie A': 20,
      'Coppa Italia': 9,
      'Supercoppa': 8,
      'Champions League': 3,
      'Europa League': 3,
      'Club World Cup': 3
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
      'Supercoppa': 2,
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
      'Supercoppa': 2,
      'Conference League': 1
    }
  },
  
  // Bundesliga
  'bayern': {
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
      'Super Cup': 2,
      'Club World Cup': 2
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
      'Club World Cup': 1
    }
  },
  'bayer-leverkusen': {
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
  'leipzig': {
    stadium: 'Red Bull Arena',
    capacity: 47069,
    coach: 'Marco Rose',
    founded: 2009,
    trophies: {
      'DFB-Pokal': 2,
      'DFL-Supercup': 1
    }
  }
};