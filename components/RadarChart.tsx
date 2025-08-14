'use client';

import { Radar, RadarChart as RechartsRadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { useEffect, useState } from 'react';

interface RadarChartProps {
  data: Array<{
    stat: string;
    value: number;
    fullMark: number;
  }>;
  title: string;
  color?: string;
}

// Labels courts pour l'affichage sur le graphique
const getShortLabel = (stat: string): string => {
  const labels: { [key: string]: string } = {
    // Statistiques générales
    'Buts': 'Buts',
    'Passes décisives': 'Passes décisives',
    'Points gagnés par match (quand le joueur joue)': 'PPM',
    'Minutes jouées': 'Minutes jouées',
    'Nombre de titularisation': 'Nombre de titularisation',
    'Nombre de jours absents/suspendus/blessés': 'Absences',
    'Valeur marchande': 'Valeur marchande',
    'Cartons (jaune + rouge)': 'Cartons',
    
    // Carte offensive
    'xG (expected goals)': 'xG',
    'xA (expected assists)': 'xA',
    'Total tirs': 'Total tirs',
    'Tirs cadrés (%)': 'Tirs cadrés (%)',
    'Ratio penalty marqué': 'Ratio penalty',
    'Courses vers l\'avant': 'Courses vers l\'avant',
    
    // Carte défensive
    'Interceptions': 'Interceptions',
    'Tacles réussis': 'Tacles réussis',
    'Duels aériens gagnés': 'Duels aériens',
    'Pressings réussis': 'Pressings',
    'Fautes subies': 'Fautes subies',
    'Fautes commises': 'Fautes commises',
    'Cartons jaunes': 'Cartons jaunes',
    'Cartons rouges': 'Cartons rouges',
    
    // Carte créative
    'Nombre de fois que le joueur touche la balle': 'Activité du joueur',
    'Dribbles réussis': 'Dribbles réussis',
    'Total passes': 'Total passes',
    'Passes clés': 'Passes clés',
    'Passes vers l\'avant': 'Passes vers l\'avant',
    'Passes courtes réussies (%)': 'Passes courtes (%)',
    'Passes longues réussies (%)': 'Passes longues (%)',
    'Centres réussis': 'Centres'
  };
  
  return labels[stat] || stat;
};

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload[0]) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-3 shadow-lg rounded-lg border border-gray-200 max-w-xs z-50">
        <p className="font-semibold text-sm mb-1 text-gray-900">{data.fullLabel}</p>
        <p className="text-sm">
          Valeur: <span className="font-bold text-blue-900">{data.originalValue}</span>
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Performance: {Math.round(data.value)}%
        </p>
      </div>
    );
  }
  return null;
};

export default function RadarChart({ data, title, color = '#1e3a8a' }: RadarChartProps) {
  const [isMobile, setIsMobile] = useState(false);
  
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Préparer les données avec labels courts et complets
  const preparedData = data.map(item => ({
    stat: getShortLabel(item.stat), // Label court pour affichage
    fullLabel: item.stat, // Label complet pour tooltip
    value: (item.value / item.fullMark) * 100,
    originalValue: item.value,
  }));

  return (
    <div className="bg-white p-3 md:p-6 rounded-lg shadow-md">
      <h3 className="text-base md:text-xl font-semibold mb-3 md:mb-4 text-center text-blue-900">
        {title}
      </h3>
      
      <ResponsiveContainer width="100%" height={isMobile ? 280 : 320}>
        <RechartsRadarChart data={preparedData}>
          <PolarGrid 
            stroke="#e0e0e0" 
            strokeWidth={0.5}
            radialLines={false}
          />
          <PolarAngleAxis 
            dataKey="stat"
            tick={{ 
              fill: '#555',
              fontSize: isMobile ? 9 : 11
            }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={false}
            axisLine={false}
          />
          <Radar 
            name={title} 
            dataKey="value" 
            stroke={color} 
            fill={color} 
            fillOpacity={0.4}
            strokeWidth={2}
          />
          <Tooltip 
            content={<CustomTooltip />}
            wrapperStyle={{ zIndex: 100 }}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>

      {/* Légende avec liste des stats complètes sur mobile */}
      {isMobile && (
        <details className="mt-4 text-xs">
          <summary className="text-gray-600 cursor-pointer">Voir les libellés complets</summary>
          <div className="mt-2 space-y-1">
            {data.map((item, index) => (
              <div key={index} className="flex justify-between text-gray-500">
                <span>{getShortLabel(item.stat)}:</span>
                <span className="text-gray-700">{item.stat}</span>
              </div>
            ))}
          </div>
        </details>
      )}

      <div className="mt-2 text-xs text-gray-500 text-center">
        {isMobile ? 'Touchez pour voir les détails' : 'Survolez pour voir les détails complets'}
      </div>
    </div>
  );
}