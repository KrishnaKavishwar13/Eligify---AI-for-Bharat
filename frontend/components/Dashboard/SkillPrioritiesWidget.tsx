'use client';

import { TrendingUp, Target, Zap } from 'lucide-react';
import { useSkillPriorities } from '@/hooks/useIntelligence';

export default function SkillPrioritiesWidget() {
  const { data: priorities, isLoading } = useSkillPriorities(5);

  if (isLoading) {
    return (
      <div className="card">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Skills to Focus On</h3>
          <p className="mt-1 text-sm text-gray-600">Loading recommendations...</p>
        </div>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="skeleton h-20"></div>
          ))}
        </div>
      </div>
    );
  }

  if (!priorities || priorities.length === 0) {
    return (
      <div className="card">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Skills to Focus On</h3>
          <p className="mt-1 text-sm text-gray-600">
            Complete your profile to get personalized recommendations
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Skills to Focus On</h3>
          <p className="mt-1 text-sm text-gray-600">AI-prioritized learning path</p>
        </div>
        <Target className="h-5 w-5 text-purple-600" />
      </div>

      <div className="space-y-3">
        {priorities.map((skill: any, index: number) => (
          <div
            key={skill.skillName}
            className="group relative overflow-hidden rounded-lg border border-gray-200 bg-gradient-to-r from-white to-purple-50/30 p-4 transition-all hover:shadow-md hover:border-purple-300"
          >
            <div className="flex items-start gap-3">
              <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-pink-500 text-sm font-bold text-white">
                {index + 1}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h4 className="font-semibold text-gray-900">{skill.skillName}</h4>
                  {skill.mandatory && (
                    <span className="badge badge-error text-xs">Required</span>
                  )}
                </div>
                <p className="mt-1 text-xs text-gray-600 line-clamp-2">
                  {skill.reasoning || 'High impact skill for your career goals'}
                </p>
                <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
                  <div className="flex items-center gap-1">
                    <Zap className="h-3 w-3 text-orange-500" />
                    <span>Priority: {skill.priorityScore || 0}</span>
                  </div>
                  {skill.internshipsUnlocked > 0 && (
                    <div className="flex items-center gap-1">
                      <TrendingUp className="h-3 w-3 text-green-500" />
                      <span>{skill.internshipsUnlocked} internships</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
