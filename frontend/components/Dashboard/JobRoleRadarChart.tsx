'use client';

import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/lib/auth';
import api from '@/lib/api';
import { API_ROUTES } from '@/lib/constants';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts';

const JOB_ROLES = [
  'Software Engineer',
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'Data Scientist',
  'DevOps Engineer',
];

export default function JobRoleRadarChart() {
  const { user } = useAuthStore();

  // Fetch career readiness for all job roles
  const { data: readinessData, isLoading } = useQuery({
    queryKey: ['career-readiness', user?.userId],
    queryFn: async () => {
      if (!user?.userId) return null;

      const results = await Promise.allSettled(
        JOB_ROLES.map(async (role) => {
          try {
            const response = await api.get(
              API_ROUTES.PREDICT_CAREER_READINESS(user.userId, role)
            );
            return {
              role: role.replace(' Engineer', '').replace(' Developer', ' Dev'),
              readiness: response.data.data?.currentReadinessScore || 0,
              fullMark: 100,
              fullRole: role,
            };
          } catch (error) {
            return {
              role: role.replace(' Engineer', '').replace(' Developer', ' Dev'),
              readiness: 0,
              fullMark: 100,
              fullRole: role,
            };
          }
        })
      );

      return results
        .filter((result) => result.status === 'fulfilled')
        .map((result) => (result as PromiseFulfilledResult<any>).value);
    },
    enabled: !!user?.userId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const chartData = readinessData || [];
  const topMatches = chartData
    .sort((a, b) => b.readiness - a.readiness)
    .slice(0, 3)
    .map((item) => ({
      role: item.role,
      matchScore: item.readiness,
      missingSkills: Math.max(0, Math.ceil((100 - item.readiness) / 10)),
    }));

  if (isLoading) {
    return (
      <div className="card">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900">AI-Preferred Job Roles</h3>
          <p className="mt-1 text-sm text-gray-600">Loading career readiness data...</p>
        </div>
        <div className="flex h-[400px] items-center justify-center">
          <div className="text-gray-500">Analyzing your career readiness...</div>
        </div>
      </div>
    );
  }

  if (!chartData || chartData.length === 0) {
    return (
      <div className="card">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900">AI-Preferred Job Roles</h3>
          <p className="mt-1 text-sm text-gray-600">
            Complete your profile to see career readiness scores
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">AI-Preferred Job Roles</h3>
        <p className="mt-1 text-sm text-gray-600">
          Your readiness score for different career paths
        </p>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={chartData}>
          <PolarGrid stroke="#e5e7eb" />
          <PolarAngleAxis
            dataKey="role"
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: '#6b7280', fontSize: 10 }}
          />
          <Radar
            name="Readiness Score"
            dataKey="readiness"
            stroke="#f97316"
            fill="#f97316"
            fillOpacity={0.6}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '8px 12px',
            }}
            formatter={(value: number) => [`${value}%`, 'Readiness']}
          />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>

      <div className="mt-6 space-y-2">
        <h4 className="text-sm font-semibold text-gray-700">Top Matches</h4>
        {topMatches.map((match, index) => (
          <div
            key={match.role}
            className="flex items-center justify-between rounded-lg bg-gradient-to-r from-orange-50 to-purple-50 p-3"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-orange-400 text-sm font-bold text-white">
                {index + 1}
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-900">{match.role}</p>
                <p className="text-xs text-gray-600">
                  {match.missingSkills === 0
                    ? 'All skills matched'
                    : `${match.missingSkills} skill${match.missingSkills > 1 ? 's' : ''} to learn`}
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold text-gray-900">{match.matchScore}%</p>
              <p className="text-xs text-gray-600">Ready</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
