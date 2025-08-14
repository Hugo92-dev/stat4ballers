'use client';

import { useState } from 'react';

interface RadarChartData {
  stat: string;
  value: number;
  fullMark: number;
}

interface CSSRadarChartProps {
  data: RadarChartData[];
  title: string;
  color?: string;
}

// Fonction pour convertir les coordonnées polaires en cartésiennes
function polarToCartesian(centerX: number, centerY: number, radius: number, angleInDegrees: number) {
  const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
  return {
    x: centerX + (radius * Math.cos(angleInRadians)),
    y: centerY + (radius * Math.sin(angleInRadians))
  };
}

// Labels courts pour l'affichage
function getShortLabel(stat: string): string {
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
}

export default function CSSRadarChart({ data, title, color = '#1e3a8a' }: CSSRadarChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  
  const centerX = 150;
  const centerY = 150;
  const maxRadius = 120;
  const numPoints = data.length;
  
  // Calculer les points pour chaque niveau (grille)
  const gridLevels = [0.2, 0.4, 0.6, 0.8, 1.0];
  
  // Calculer les points du polygone de données
  const dataPoints = data.map((item, index) => {
    const angle = (360 / numPoints) * index;
    const normalizedValue = item.value / item.fullMark;
    const radius = Math.min(normalizedValue, 1) * maxRadius;
    return {
      ...polarToCartesian(centerX, centerY, radius, angle),
      originalValue: item.value,
      normalizedValue: normalizedValue * 100,
      stat: item.stat,
      shortLabel: getShortLabel(item.stat)
    };
  });
  
  // Calculer les points des axes et labels
  const axisPoints = data.map((item, index) => {
    const angle = (360 / numPoints) * index;
    const endPoint = polarToCartesian(centerX, centerY, maxRadius, angle);
    const labelPoint = polarToCartesian(centerX, centerY, maxRadius + 20, angle);
    return {
      endPoint,
      labelPoint,
      shortLabel: getShortLabel(item.stat),
      fullLabel: item.stat
    };
  });
  
  // Créer le path du polygone de données
  const polygonPath = dataPoints.map((point, index) => 
    `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`
  ).join(' ') + ' Z';

  return (
    <div className="bg-white p-3 md:p-6 rounded-lg shadow-md">
      <h3 className="text-base md:text-xl font-semibold mb-3 md:mb-4 text-center text-blue-900">
        {title}
      </h3>
      
      <div className="relative">
        <svg width="300" height="300" viewBox="0 0 300 300" className="w-full h-auto max-w-sm mx-auto">
          {/* Grille circulaire */}
          {gridLevels.map((level, levelIndex) => {
            const radius = level * maxRadius;
            const gridPoints = axisPoints.map((_, index) => {
              const angle = (360 / numPoints) * index;
              return polarToCartesian(centerX, centerY, radius, angle);
            });
            
            const gridPath = gridPoints.map((point, index) => 
              `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`
            ).join(' ') + ' Z';
            
            return (
              <path 
                key={levelIndex}
                d={gridPath}
                fill="none"
                stroke="#e0e0e0"
                strokeWidth="1"
                opacity={0.5}
              />
            );
          })}
          
          {/* Axes radiaux */}
          {axisPoints.map((axis, index) => (
            <line
              key={index}
              x1={centerX}
              y1={centerY}
              x2={axis.endPoint.x}
              y2={axis.endPoint.y}
              stroke="#e0e0e0"
              strokeWidth="1"
              opacity={0.5}
            />
          ))}
          
          {/* Labels des axes */}
          {axisPoints.map((axis, index) => (
            <g key={index}>
              <text
                x={axis.labelPoint.x}
                y={axis.labelPoint.y}
                textAnchor="middle"
                dominantBaseline="middle"
                className="fill-gray-600 text-xs md:text-sm font-medium"
                style={{ fontSize: '10px' }}
              >
                {axis.shortLabel}
              </text>
            </g>
          ))}
          
          {/* Polygone de données */}
          <path
            d={polygonPath}
            fill={color}
            fillOpacity="0.3"
            stroke={color}
            strokeWidth="2"
          />
          
          {/* Points de données avec hover */}
          {dataPoints.map((point, index) => (
            <g key={index}>
              <circle
                cx={point.x}
                cy={point.y}
                r="4"
                fill={color}
                stroke="white"
                strokeWidth="2"
                className="cursor-pointer transition-all duration-200 hover:r-6"
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              />
              
              {/* Tooltip */}
              {hoveredIndex === index && (
                <g>
                  <rect
                    x={point.x - 60}
                    y={point.y - 45}
                    width="120"
                    height="35"
                    fill="white"
                    stroke="#ccc"
                    strokeWidth="1"
                    rx="4"
                    className="drop-shadow-md"
                  />
                  <text
                    x={point.x}
                    y={point.y - 30}
                    textAnchor="middle"
                    className="fill-gray-900 text-xs font-semibold"
                  >
                    {point.stat}
                  </text>
                  <text
                    x={point.x}
                    y={point.y - 15}
                    textAnchor="middle"
                    className="fill-blue-900 text-xs font-bold"
                  >
                    Valeur: {point.originalValue}
                  </text>
                </g>
              )}
            </g>
          ))}
        </svg>
      </div>
      
      <div className="mt-2 text-xs text-gray-500 text-center">
        Survolez les points pour voir les détails complets
      </div>
    </div>
  );
}