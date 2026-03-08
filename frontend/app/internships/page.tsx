'use client';

import { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import MainLayout from '@/components/Layout/MainLayout';
import InternshipCard from '@/components/Internships/InternshipCard';
import { useInternships } from '@/hooks/useInternships';
import { cn } from '@/lib/utils';

type Tab = 'eligible' | 'almostEligible' | 'notEligible';

export default function InternshipsPage() {
  const { eligible, almostEligible, notEligible, isLoading } =
    useInternships();
  const [activeTab, setActiveTab] = useState<Tab>('eligible');
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');

  const tabs = [
    {
      id: 'eligible' as Tab,
      label: 'Eligible',
      count: eligible.length,
      color: 'text-success border-success',
    },
    {
      id: 'almostEligible' as Tab,
      label: 'Almost Eligible',
      count: almostEligible.length,
      color: 'text-warning border-warning',
    },
    {
      id: 'notEligible' as Tab,
      label: 'Not Eligible',
      count: notEligible.length,
      color: 'text-neutral border-neutral',
    },
  ];

  const getActiveInternships = () => {
    let internships =
      activeTab === 'eligible'
        ? eligible
        : activeTab === 'almostEligible'
          ? almostEligible
          : notEligible;

    // Apply search filter
    if (searchQuery) {
      internships = internships.filter(
        (match) =>
          match.internship.title
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          match.internship.company
            .toLowerCase()
            .includes(searchQuery.toLowerCase())
      );
    }

    // Apply type filter
    if (typeFilter !== 'all') {
      internships = internships.filter(
        (match) => match.internship.type === typeFilter
      );
    }

    return internships;
  };

  const filteredInternships = getActiveInternships();

  if (isLoading) {
    return (
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="space-y-6 p-6">
            <div className="skeleton h-10 w-64"></div>
            <div className="skeleton h-12 w-full"></div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="skeleton h-48"></div>
              ))}
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
        <div className="space-y-6 p-6">
          {/* Header */}
          <div className="rounded-xl bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-6 text-white shadow-lg">
            <h1 className="text-3xl font-bold">
              Internship Opportunities
            </h1>
            <p className="mt-2 text-purple-100">
              Discover opportunities matched to your skills
            </p>
            <div className="mt-4 flex gap-4">
              <div className="rounded-lg bg-white/20 backdrop-blur-sm px-4 py-2">
                <p className="text-2xl font-bold">{eligible.length}</p>
                <p className="text-xs text-purple-100">Eligible Now</p>
              </div>
              <div className="rounded-lg bg-white/20 backdrop-blur-sm px-4 py-2">
                <p className="text-2xl font-bold">{almostEligible.length}</p>
                <p className="text-xs text-purple-100">Almost There</p>
              </div>
            </div>
          </div>

          {/* Tabs */}
        <div className="border-b border-gray-200">
          <div className="flex gap-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  'border-b-2 pb-4 text-sm font-medium transition-colors',
                  activeTab === tab.id
                    ? tab.color
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                )}
              >
                {tab.label}
                <span
                  className={cn(
                    'ml-2 rounded-full px-2.5 py-0.5 text-xs font-medium',
                    activeTab === tab.id
                      ? tab.id === 'eligible'
                        ? 'bg-green-100 text-green-800'
                        : tab.id === 'almostEligible'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      : 'bg-gray-100 text-gray-600'
                  )}
                >
                  {tab.count}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col gap-4 sm:flex-row">
          {/* Search */}
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search by company or role..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input w-full pl-10"
            />
          </div>

          {/* Type Filter */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="input w-full pl-10 sm:w-auto"
            >
              <option value="all">All Types</option>
              <option value="remote">Remote</option>
              <option value="onsite">On-site</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </div>
        </div>

        {/* Internships List */}
        {filteredInternships.length === 0 ? (
          <div className="rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
            <p className="text-lg font-medium text-gray-900">
              No internships found
            </p>
            <p className="mt-2 text-sm text-gray-500">
              Try adjusting your filters or check other tabs
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredInternships.map((match) => (
              <InternshipCard
                key={match.internship.internshipId}
                match={match}
                category={activeTab}
              />
            ))}
          </div>
        )}
        </div>
      </div>
    </MainLayout>
  );
}
