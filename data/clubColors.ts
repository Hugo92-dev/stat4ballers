export interface ClubColors {
  primary: string;
  secondary: string;
  accent: string;
  gradient: string;
  cardGradient: string;
  hoverGradient: string;
  borderColor: string;
}

export const clubColors: Record<string, ClubColors> = {
  // Ligue 1
  'paris-saint-germain': {
    primary: '#004170',
    secondary: '#DA020E',
    accent: '#ffffff',
    gradient: 'from-[#004170] to-[#DA020E]',
    cardGradient: 'from-[#004170]/10 to-[#DA020E]/5',
    hoverGradient: 'from-[#004170]/20 to-[#DA020E]/10',
    borderColor: 'border-[#004170]/20'
  },
  'olympique-marseille': {
    primary: '#2FAEE0',
    secondary: '#ffffff',
    accent: '#0EA5E9',
    gradient: 'from-[#2FAEE0] to-[#0EA5E9]',
    cardGradient: 'from-[#2FAEE0]/10 to-[#0EA5E9]/5',
    hoverGradient: 'from-[#2FAEE0]/20 to-[#0EA5E9]/10',
    borderColor: 'border-[#2FAEE0]/20'
  },
  'as-monaco': {
    primary: '#E73427',
    secondary: '#ffffff',
    accent: '#FFD700',
    gradient: 'from-[#E73427] to-[#c41e3a]',
    cardGradient: 'from-[#E73427]/20 via-red-500/10 to-transparent',
    hoverGradient: 'from-[#E73427]/30 via-red-400/20 to-transparent',
    borderColor: 'border-[#E73427]/30'
  },
  'losc-lille': {
    primary: '#EE2737',
    secondary: '#004170',
    accent: '#ffffff',
    gradient: 'from-[#EE2737] to-[#004170]',
    cardGradient: 'from-[#EE2737]/20 via-[#004170]/10 to-transparent',
    hoverGradient: 'from-[#EE2737]/30 via-[#004170]/20 to-transparent',
    borderColor: 'border-[#EE2737]/30'
  },
  'olympique-lyonnais': {
    primary: '#000F9F',
    secondary: '#DA020E',
    accent: '#ffffff',
    gradient: 'from-[#000F9F] to-[#DA020E]',
    cardGradient: 'from-[#000F9F]/20 via-[#DA020E]/10 to-transparent',
    hoverGradient: 'from-[#000F9F]/30 via-[#DA020E]/20 to-transparent',
    borderColor: 'border-[#000F9F]/30'
  },
  'ogc-nice': {
    primary: '#CC0000',
    secondary: '#000000',
    accent: '#ffffff',
    gradient: 'from-[#CC0000] to-[#000000]',
    cardGradient: 'from-[#CC0000]/20 via-gray-800/10 to-transparent',
    hoverGradient: 'from-[#CC0000]/30 via-gray-700/20 to-transparent',
    borderColor: 'border-[#CC0000]/30'
  },
  'rc-lens': {
    primary: '#FFD700',
    secondary: '#FF0000',
    accent: '#000000',
    gradient: 'from-[#FFD700] to-[#FF0000]',
    cardGradient: 'from-[#FFD700]/20 via-[#FF0000]/10 to-transparent',
    hoverGradient: 'from-[#FFD700]/30 via-[#FF0000]/20 to-transparent',
    borderColor: 'border-[#FFD700]/30'
  },
  'stade-rennais-fc': {
    primary: '#E13327',
    secondary: '#000000',
    accent: '#ffffff',
    gradient: 'from-[#E13327] to-[#000000]',
    cardGradient: 'from-[#E13327]/20 via-gray-800/10 to-transparent',
    hoverGradient: 'from-[#E13327]/30 via-gray-700/20 to-transparent',
    borderColor: 'border-[#E13327]/30'
  },
  'fc-nantes': {
    primary: '#00913D',
    secondary: '#FCD405',
    accent: '#ffffff',
    gradient: 'from-[#00913D] to-[#FCD405]',
    cardGradient: 'from-[#00913D]/20 via-[#FCD405]/10 to-transparent',
    hoverGradient: 'from-[#00913D]/30 via-[#FCD405]/20 to-transparent',
    borderColor: 'border-[#00913D]/30'
  },
  
  // Premier League
  'manchester-city': {
    primary: '#6CABDD',
    secondary: '#001838',
    accent: '#ffffff',
    gradient: 'from-[#6CABDD] to-[#001838]',
    cardGradient: 'from-[#6CABDD]/20 via-[#001838]/10 to-transparent',
    hoverGradient: 'from-[#6CABDD]/30 via-[#001838]/20 to-transparent',
    borderColor: 'border-[#6CABDD]/30'
  },
  'arsenal': {
    primary: '#EF0107',
    secondary: '#063672',
    accent: '#ffffff',
    gradient: 'from-[#EF0107] to-[#063672]',
    cardGradient: 'from-[#EF0107]/20 via-[#063672]/10 to-transparent',
    hoverGradient: 'from-[#EF0107]/30 via-[#063672]/20 to-transparent',
    borderColor: 'border-[#EF0107]/30'
  },
  'liverpool': {
    primary: '#C8102E',
    secondary: '#00B2A9',
    accent: '#F6EB61',
    gradient: 'from-[#C8102E] to-[#00B2A9]',
    cardGradient: 'from-[#C8102E]/20 via-[#00B2A9]/10 to-transparent',
    hoverGradient: 'from-[#C8102E]/30 via-[#00B2A9]/20 to-transparent',
    borderColor: 'border-[#C8102E]/30'
  },
  'chelsea': {
    primary: '#034694',
    secondary: '#6A7AB5',
    accent: '#DBA111',
    gradient: 'from-[#034694] to-[#6A7AB5]',
    cardGradient: 'from-[#034694]/20 via-[#6A7AB5]/10 to-transparent',
    hoverGradient: 'from-[#034694]/30 via-[#6A7AB5]/20 to-transparent',
    borderColor: 'border-[#034694]/30'
  },
  'manchester-united': {
    primary: '#DA020E',
    secondary: '#FBE122',
    accent: '#000000',
    gradient: 'from-[#DA020E] to-[#FBE122]',
    cardGradient: 'from-[#DA020E]/20 via-[#FBE122]/10 to-transparent',
    hoverGradient: 'from-[#DA020E]/30 via-[#FBE122]/20 to-transparent',
    borderColor: 'border-[#DA020E]/30'
  },
  'tottenham': {
    primary: '#132257',
    secondary: '#ffffff',
    accent: '#1B3E87',
    gradient: 'from-[#132257] to-[#1B3E87]',
    cardGradient: 'from-[#132257]/20 via-[#1B3E87]/10 to-transparent',
    hoverGradient: 'from-[#132257]/30 via-[#1B3E87]/20 to-transparent',
    borderColor: 'border-[#132257]/30'
  },
  
  // Liga
  'real-madrid': {
    primary: '#ffffff',
    secondary: '#D7B66B',
    accent: '#004696',
    gradient: 'from-gray-100 to-[#D7B66B]',
    cardGradient: 'from-gray-200/20 via-[#D7B66B]/10 to-transparent',
    hoverGradient: 'from-gray-100/30 via-[#D7B66B]/20 to-transparent',
    borderColor: 'border-[#D7B66B]/30'
  },
  'fc-barcelone': {
    primary: '#004D98',
    secondary: '#A50044',
    accent: '#EDBB00',
    gradient: 'from-[#004D98] to-[#A50044]',
    cardGradient: 'from-[#004D98]/20 via-[#A50044]/10 to-transparent',
    hoverGradient: 'from-[#004D98]/30 via-[#A50044]/20 to-transparent',
    borderColor: 'border-[#004D98]/30'
  },
  'atletico-de-madrid': {
    primary: '#CB3524',
    secondary: '#272E61',
    accent: '#ffffff',
    gradient: 'from-[#CB3524] to-[#272E61]',
    cardGradient: 'from-[#CB3524]/20 via-[#272E61]/10 to-transparent',
    hoverGradient: 'from-[#CB3524]/30 via-[#272E61]/20 to-transparent',
    borderColor: 'border-[#CB3524]/30'
  },
  
  // Serie A
  'juventus': {
    primary: '#000000',
    secondary: '#ffffff',
    accent: '#FFD500',
    gradient: 'from-gray-900 to-gray-700',
    cardGradient: 'from-gray-800/20 via-gray-700/10 to-transparent',
    hoverGradient: 'from-gray-700/30 via-gray-600/20 to-transparent',
    borderColor: 'border-gray-600/30'
  },
  'milan': {
    primary: '#FB090B',
    secondary: '#000000',
    accent: '#ffffff',
    gradient: 'from-[#FB090B] to-[#000000]',
    cardGradient: 'from-[#FB090B]/20 via-gray-900/10 to-transparent',
    hoverGradient: 'from-[#FB090B]/30 via-gray-800/20 to-transparent',
    borderColor: 'border-[#FB090B]/30'
  },
  'inter': {
    primary: '#0068A9',
    secondary: '#000000',
    accent: '#FFD500',
    gradient: 'from-[#0068A9] to-[#000000]',
    cardGradient: 'from-[#0068A9]/20 via-gray-900/10 to-transparent',
    hoverGradient: 'from-[#0068A9]/30 via-gray-800/20 to-transparent',
    borderColor: 'border-[#0068A9]/30'
  },
  'napoli': {
    primary: '#12A5E0',
    secondary: '#003F77',
    accent: '#ffffff',
    gradient: 'from-[#12A5E0] to-[#003F77]',
    cardGradient: 'from-[#12A5E0]/20 via-[#003F77]/10 to-transparent',
    hoverGradient: 'from-[#12A5E0]/30 via-[#003F77]/20 to-transparent',
    borderColor: 'border-[#12A5E0]/30'
  },
  
  // Bundesliga
  'bayern-munchen': {
    primary: '#DC052D',
    secondary: '#0066B2',
    accent: '#ffffff',
    gradient: 'from-[#DC052D] to-[#0066B2]',
    cardGradient: 'from-[#DC052D]/20 via-[#0066B2]/10 to-transparent',
    hoverGradient: 'from-[#DC052D]/30 via-[#0066B2]/20 to-transparent',
    borderColor: 'border-[#DC052D]/30'
  },
  'borussia-dortmund': {
    primary: '#FDE100',
    secondary: '#000000',
    accent: '#ffffff',
    gradient: 'from-[#FDE100] to-[#000000]',
    cardGradient: 'from-[#FDE100]/20 via-gray-900/10 to-transparent',
    hoverGradient: 'from-[#FDE100]/30 via-gray-800/20 to-transparent',
    borderColor: 'border-[#FDE100]/30'
  },
  
  // Default colors
  'default': {
    primary: '#3B82F6',
    secondary: '#1E40AF',
    accent: '#ffffff',
    gradient: 'from-blue-500 to-blue-700',
    cardGradient: 'from-blue-500/20 via-blue-600/10 to-transparent',
    hoverGradient: 'from-blue-400/30 via-blue-500/20 to-transparent',
    borderColor: 'border-blue-500/30'
  }
};

export const getClubColors = (clubId: string): ClubColors => {
  return clubColors[clubId] || clubColors['default'];
};