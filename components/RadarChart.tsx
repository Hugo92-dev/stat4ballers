```tsx
'use client';

import { Radar, RadarChart as RechartsRadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

interface RadarChartProps {
  data: Array<{
    stat: string;
    value: number;
    fullMark: number;
  }>;
  title: string;
  color?: string;
}

export default function RadarChart({ data, title, color = '#011B42' }: RadarChartProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-center text-[--primary]">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RechartsRadarChart data={data}>
          <PolarGrid stroke="#e0e0e0" />
          <PolarAngleAxis 
            dataKey="stat" 
            className="text-sm"
            tick={{ fill: '#666' }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={{ fill: '#666' }}
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
    </div>
  );
}
```