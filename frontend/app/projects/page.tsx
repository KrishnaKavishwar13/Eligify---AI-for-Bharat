'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { Sparkles, FolderKanban } from 'lucide-react';
import MainLayout from '@/components/Layout/MainLayout';
import ProjectCard from '@/components/Projects/ProjectCard';
import GenerateProjectModal from '@/components/Projects/GenerateProjectModal';
import { useProjects } from '@/hooks/useProjects';
import { cn } from '@/lib/utils';
import { ProjectStatus } from '@/types';
import { SkeletonList } from '@/components/GradientSkeleton';

export const dynamic = 'force-dynamic';

type Tab = 'all' | ProjectStatus;

export default function ProjectsPage() {
  const searchParams = useSearchParams();
  const [showGenerateModal, setShowGenerateModal] = useState(false);
  const [activeTab, setActiveTab] = useState<Tab>('all');
  const [preselectedSkills, setPreselectedSkills] = useState<string[]>([]);

  const { projects, isLoading } = useProjects();

  // Check for preselected skills from URL
  useEffect(() => {
    const skillsParam = searchParams.get('skills');
    if (skillsParam) {
      setPreselectedSkills(skillsParam.split(','));
      setShowGenerateModal(true);
    }
  }, [searchParams]);

  const tabs: { id: Tab; label: string }[] = [
    { id: 'all', label: 'All Projects' },
    { id: ProjectStatus.SUGGESTED, label: 'Suggested' },
    { id: ProjectStatus.IN_PROGRESS, label: 'In Progress' },
    { id: ProjectStatus.COMPLETED, label: 'Completed' },
  ];

  const filteredProjects =
    activeTab === 'all'
      ? projects
      : projects.filter((p) => p.status === activeTab);

  if (isLoading) {
    return (
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="space-y-6 p-6">
            {/* Gradient Header Skeleton */}
            <div className="rounded-xl bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-6 shadow-lg">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="h-8 w-64 rounded bg-white/20 backdrop-blur-sm animate-pulse"></div>
                  <div className="mt-2 h-4 w-96 rounded bg-white/20 backdrop-blur-sm animate-pulse"></div>
                </div>
                <div className="h-10 w-40 rounded-lg bg-white/20 backdrop-blur-sm animate-pulse"></div>
              </div>
              <div className="mt-4 flex gap-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="rounded-lg bg-white/20 backdrop-blur-sm px-4 py-2 w-32">
                    <div className="h-6 w-12 rounded bg-white/20 animate-pulse mb-1"></div>
                    <div className="h-3 w-20 rounded bg-white/20 animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Tabs Skeleton */}
            <div className="border-b border-gray-200">
              <div className="flex gap-8">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="h-10 w-32 rounded bg-gray-200 animate-pulse"></div>
                ))}
              </div>
            </div>

            {/* Projects List Skeleton */}
            <SkeletonList count={3} />
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <>
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="space-y-6 p-6">
            {/* Gradient Header */}
            <div className="rounded-xl bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-6 text-white shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold">Learning Projects</h1>
                  <p className="mt-2 text-purple-100">
                    AI-generated roadmaps to build your skills
                  </p>
                </div>
                <button
                  onClick={() => setShowGenerateModal(true)}
                  className="rounded-lg border-2 border-white/30 bg-white/20 backdrop-blur-sm px-4 py-2 font-semibold text-white hover:bg-white/30 transition-colors flex items-center gap-2"
                >
                  <Sparkles className="h-4 w-4" />
                  Generate Project
                </button>
              </div>
              <div className="mt-4 flex gap-4">
                <div className="rounded-lg bg-white/20 backdrop-blur-sm px-4 py-2">
                  <p className="text-2xl font-bold">{projects.length}</p>
                  <p className="text-xs text-purple-100">Total Projects</p>
                </div>
                <div className="rounded-lg bg-white/20 backdrop-blur-sm px-4 py-2">
                  <p className="text-2xl font-bold">
                    {projects.filter((p) => p.status === ProjectStatus.IN_PROGRESS).length}
                  </p>
                  <p className="text-xs text-purple-100">In Progress</p>
                </div>
                <div className="rounded-lg bg-white/20 backdrop-blur-sm px-4 py-2">
                  <p className="text-2xl font-bold">
                    {projects.filter((p) => p.status === ProjectStatus.COMPLETED).length}
                  </p>
                  <p className="text-xs text-purple-100">Completed</p>
                </div>
              </div>
            </div>

          {/* Tabs */}
          <div className="border-b border-gray-200">
            <div className="flex gap-8">
              {tabs.map((tab) => {
                const count =
                  tab.id === 'all'
                    ? projects.length
                    : projects.filter((p) => p.status === tab.id).length;

                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={cn(
                      'border-b-2 pb-4 text-sm font-medium transition-colors',
                      activeTab === tab.id
                        ? 'border-primary text-primary'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    )}
                  >
                    {tab.label}
                    <span
                      className={cn(
                        'ml-2 rounded-full px-2.5 py-0.5 text-xs font-medium',
                        activeTab === tab.id
                          ? 'bg-primary/10 text-primary'
                          : 'bg-gray-100 text-gray-600'
                      )}
                    >
                      {count}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Projects List */}
          {filteredProjects.length === 0 ? (
            <div className="rounded-xl border border-gray-200 bg-white p-12 text-center shadow-sm">
              <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-purple-100 to-pink-100">
                <FolderKanban className="h-10 w-10 text-purple-600" />
              </div>
              <h2 className="mt-6 text-2xl font-bold text-gray-900">
                {activeTab === 'all' ? 'No projects yet' : `No ${tabs.find(t => t.id === activeTab)?.label.toLowerCase()} projects`}
              </h2>
              <p className="mt-2 text-gray-600">
                {activeTab === 'all' 
                  ? 'Generate your first AI-powered learning project to start building skills'
                  : 'Try switching to a different tab or generate a new project'}
              </p>
              <button
                onClick={() => setShowGenerateModal(true)}
                className="mt-6 inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 px-6 py-3 font-semibold text-white shadow-lg hover:shadow-xl transition-all"
              >
                <Sparkles className="h-5 w-5" />
                Generate Project
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredProjects.map((project) => (
                <ProjectCard key={project.projectId} project={project} />
              ))}
            </div>
          )}
        </div>
      </div>
      </MainLayout>

      {showGenerateModal && (
        <GenerateProjectModal
          onClose={() => {
            setShowGenerateModal(false);
            setPreselectedSkills([]);
          }}
          preselectedSkills={preselectedSkills}
        />
      )}
    </>
  );
}
