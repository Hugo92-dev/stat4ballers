'use client';

import { Radar, RadarChart as RechartsRadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts';

interface RadarChartProps {
  data: Array<{
    stat: string;
    value: number;
    fullMark: number;
  }>;
  title: string;
  color?: string;
}

export default function RadarChart({ data, title, color = '#1e3a8a' }: RadarChartProps) {
  // Normaliser les données sur 100
  const normalizedData = data.map(item => ({
    ...item,
    displayValue: item.value,
    value: (item.value / item.fullMark) * 100
  }));

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-center text-blue-900">{title}</h3>
      <ResponsiveContainer width="100%" height={350}>
        <RechartsRadarChart data={normalizedData}>
          <PolarGrid stroke="#e0e0e0" />
          <PolarAngleAxis 
            dataKey="stat" 
            className="text-sm"
            tick={{ fill: '#666', fontSize: 12 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={false}
          />
          <Radar 
            name={title} 
            dataKey="value" 
            stroke={color} 
            fill={color} 
            fillOpacity={0.6} 
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
      <div className="mt-4 text-xs text-gray-500 text-center">
        Valeurs normalisées sur 100
      </div>
    </div>
  );
}