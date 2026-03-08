'use client';

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { SkillNode } from '@/types';

interface SkillSpiderChartProps {
  skills: SkillNode[];
}

export default function SkillSpiderChart({ skills }: SkillSpiderChartProps) {
  const categoryData = skills.reduce((acc, skill) => {
    const category = skill.category.replace(/_/g, ' ');
    if (!acc[category]) {
      acc[category] = { total: 0, count: 0 };
    }
    acc[category].total += skill.proficiencyLevel;
    acc[category].count += 1;
    return acc;
  }, {} as Record<string, { total: number; count: number }>);

  const chartData = Object.entries(categoryData).map(([category, data]) => ({
    category,
    proficiency: Math.round(data.total / data.count),
    fullMark: 100,
  }));

  if (chartData.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900">Skill Proficiency Map</h3>
        <div className="mt-6 flex h-64 items-center justify-center text-gray-500">
          No skills to display
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Skill Proficiency Map</h3>
        <p className="mt-1 text-sm text-gray-600">
          Your skill proficiency across different categories
        </p>
      </div>
      
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={chartData}>
          <PolarGrid stroke="#e5e7eb" />
          <PolarAngleAxis 
            dataKey="category" 
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]}
            tick={{ fill: '#6b7280', fontSize: 10 }}
          />
          <Radar
            name="Proficiency"
            dataKey="proficiency"
            stroke="#8b5cf6"
            fill="#8b5cf6"
            fillOpacity={0.6}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '8px 12px',
            }}
            formatter={(value: number) => [`${value}%`, 'Proficiency']}
          />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
