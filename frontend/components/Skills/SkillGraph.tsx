'use client';

import { useState } from 'react';
import { CheckCircle, Clock, Circle, Plus, Filter } from 'lucide-react';
import { cn } from '@/lib/utils';
import { SkillStatus } from '@/types';
import type { SkillNode, SkillCategory } from '@/types';
import AddSkillModal from './AddSkillModal';

interface SkillGraphProps {
  skills: SkillNode[];
  onAddSkill?: (skillName: string, category: SkillCategory) => void;
}

const statusConfig: Record<SkillStatus, {
  icon: typeof CheckCircle;
  color: string;
  bg: string;
  border: string;
  label: string;
}> = {
  [SkillStatus.VERIFIED]: {
    icon: CheckCircle,
    color: 'text-success',
    bg: 'bg-green-50',
    border: 'border-success',
    label: 'Verified',
  },
  [SkillStatus.IN_PROGRESS]: {
    icon: Clock,
    color: 'text-warning',
    bg: 'bg-yellow-50',
    border: 'border-warning',
    label: 'In Progress',
  },
  [SkillStatus.CLAIMED]: {
    icon: Circle,
    color: 'text-gray-400',
    bg: 'bg-gray-50',
    border: 'border-gray-300',
    label: 'Claimed',
  },
};

export default function SkillGraph({ skills, onAddSkill }: SkillGraphProps) {
  const [showAddModal, setShowAddModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<SkillStatus | 'all'>('all');
  const [filterCategory, setFilterCategory] = useState<SkillCategory | 'all'>('all');

  const filteredSkills = skills.filter((skill) => {
    if (filterStatus !== 'all' && skill.status !== filterStatus) return false;
    if (filterCategory !== 'all' && skill.category !== filterCategory) return false;
    return true;
  });

  const categories = Array.from(new Set(skills.map((s) => s.category)));
  const verifiedCount = skills.filter((s) => s.status === SkillStatus.VERIFIED).length;

  return (
    <div className="card">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Your Skills</h3>
          <p className="mt-1 text-sm text-gray-600">
            {verifiedCount} verified out of {skills.length} total skills
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          Add Skill
        </button>
      </div>

      {/* Filters */}
      <div className="mt-6 flex flex-wrap gap-3">
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-gray-500" />
          <span className="text-sm font-medium text-gray-700">Filter:</span>
        </div>
        
        {/* Status Filter */}
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as SkillStatus | 'all')}
          className="rounded-lg border border-gray-300 px-3 py-1 text-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="all">All Status</option>
          <option value={SkillStatus.VERIFIED}>Verified</option>
          <option value={SkillStatus.IN_PROGRESS}>In Progress</option>
          <option value={SkillStatus.CLAIMED}>Claimed</option>
        </select>

        {/* Category Filter */}
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value as SkillCategory | 'all')}
          className="rounded-lg border border-gray-300 px-3 py-1 text-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="all">All Categories</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat.replace(/_/g, ' ')}
            </option>
          ))}
        </select>
      </div>

      {/* Skills Grid */}
      {filteredSkills.length > 0 ? (
        <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {filteredSkills.map((skill) => {
            const config = statusConfig[skill.status];
            const Icon = config.icon;

            return (
              <div
                key={skill.skillId}
                className={cn(
                  'rounded-lg border-2 p-4 transition-all hover:shadow-md',
                  config.bg,
                  config.border
                )}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900">
                      {skill.name}
                    </h4>
                    <p className="mt-1 text-xs text-gray-600">
                      {skill.category.replace(/_/g, ' ')}
                    </p>
                  </div>
                  <Icon className={cn('h-5 w-5', config.color)} />
                </div>

                {/* Proficiency Bar */}
                <div className="mt-3">
                  <div className="flex items-center justify-between text-xs text-gray-600">
                    <span>Proficiency</span>
                    <span className="font-medium">{skill.proficiencyLevel}%</span>
                  </div>
                  <div className="relative mt-1 h-1 w-full overflow-hidden bg-gray-200">
                    <div
                      className={cn(
                        'h-full transition-all relative',
                        skill.status === SkillStatus.VERIFIED
                          ? 'bg-success'
                          : skill.status === SkillStatus.IN_PROGRESS
                            ? 'bg-warning'
                            : 'bg-gray-400'
                      )}
                      style={{ width: `${skill.proficiencyLevel}%` }}
                    >
                      {skill.proficiencyLevel > 0 && (
                        <div className="absolute right-0 top-1/2 -translate-y-1/2">
                          <div className="relative">
                            <div className="h-1.5 w-1.5 rounded-full bg-white shadow-lg"></div>
                            <div className="absolute inset-0 h-1.5 w-1.5 rounded-full bg-white animate-ping"></div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="mt-3 flex items-center justify-between">
                  <span className={cn('text-xs font-medium', config.color)}>
                    {config.label}
                  </span>
                  {skill.verifiedAt && (
                    <span className="text-xs text-gray-500">
                      {new Date(skill.verifiedAt).toLocaleDateString()}
                    </span>
                  )}
                </div>

                {/* Source */}
                <div className="mt-2 text-xs text-gray-500">
                  Source: {skill.source.replace(/_/g, ' ')}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="mt-6 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
          <Circle className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-4 text-sm font-medium text-gray-900">
            No skills found
          </p>
          <p className="mt-1 text-sm text-gray-600">
            Try adjusting your filters or add a new skill
          </p>
        </div>
      )}

      {/* Add Skill Modal */}
      {showAddModal && (
        <AddSkillModal
          onClose={() => setShowAddModal(false)}
          onAdd={onAddSkill}
        />
      )}
    </div>
  );
}
