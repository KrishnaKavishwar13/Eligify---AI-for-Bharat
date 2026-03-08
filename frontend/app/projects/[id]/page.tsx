'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
  ArrowLeft,
  CheckCircle,
  Clock,
  Code,
  Target,
  BookOpen,
  Play,
  Check,
  XCircle,
} from 'lucide-react';
import MainLayout from '@/components/Layout/MainLayout';
import { useProject, useProjects } from '@/hooks/useProjects';
import { cn, getProjectStatusColor } from '@/lib/utils';
import { APP_ROUTES } from '@/lib/constants';
import { ProjectStatus } from '@/types';
import { GradientSkeleton } from '@/components/GradientSkeleton';

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;
  const { data: project, isLoading } = useProject(projectId);
  const { updateStatus, completeProject, isUpdatingStatus, isCompleting } =
    useProjects();
  const [showCompleteConfirm, setShowCompleteConfirm] = useState(false);

  const handleStatusChange = (status: ProjectStatus) => {
    updateStatus({ projectId, status });
  };

  const handleComplete = () => {
    completeProject(projectId, {
      onSuccess: () => {
        setShowCompleteConfirm(false);
      },
    });
  };

  if (isLoading) {
    return (
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="space-y-6 p-6">
            {/* Back Button Skeleton */}
            <GradientSkeleton size="sm" width="120px" />

            {/* Gradient Header Skeleton */}
            <div className="rounded-xl bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-6 shadow-lg">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="h-8 w-96 rounded bg-white/20 backdrop-blur-sm animate-pulse"></div>
                  <div className="mt-2 h-4 w-full max-w-2xl rounded bg-white/20 backdrop-blur-sm animate-pulse"></div>
                </div>
                <div className="h-8 w-24 rounded-full bg-white/20 backdrop-blur-sm animate-pulse"></div>
              </div>

              {/* Quick Stats Skeleton */}
              <div className="mt-6 grid gap-4 sm:grid-cols-4">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="rounded-lg bg-white/20 backdrop-blur-sm p-4">
                    <div className="h-5 w-5 rounded bg-white/20 animate-pulse mb-2"></div>
                    <div className="h-3 w-20 rounded bg-white/20 animate-pulse mb-1"></div>
                    <div className="h-6 w-12 rounded bg-white/20 animate-pulse"></div>
                  </div>
                ))}
              </div>

              {/* Action Buttons Skeleton */}
              <div className="mt-6 flex gap-3">
                <div className="h-12 w-40 rounded-lg bg-white/20 backdrop-blur-sm animate-pulse"></div>
              </div>
            </div>

            {/* Content Cards Skeleton */}
            <div className="space-y-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="card">
                  <GradientSkeleton size="md" width="200px" className="mb-4" />
                  <GradientSkeleton size="sm" className="mb-2" />
                  <GradientSkeleton size="sm" width="80%" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  if (!project) {
    return (
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-red-100">
                <XCircle className="h-10 w-10 text-red-600" />
              </div>
              <h2 className="mt-6 text-2xl font-bold text-gray-900">Project not found</h2>
              <p className="mt-2 text-gray-600">
                This project doesn't exist or has been removed
              </p>
              <button
                onClick={() => router.push(APP_ROUTES.PROJECTS)}
                className="mt-6 inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 px-6 py-3 font-semibold text-white shadow-lg hover:shadow-xl transition-all"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to Projects
              </button>
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
          {/* Back Button */}
          <button
            onClick={() => router.push(APP_ROUTES.PROJECTS)}
            className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Projects
          </button>

          {/* Gradient Header */}
          <div className="rounded-xl bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-6 text-white shadow-lg">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <h1 className="text-3xl font-bold">{project.title}</h1>
                <p className="mt-2 text-purple-100">{project.description}</p>
              </div>
              <span className={cn(
                'badge text-sm font-semibold px-4 py-2',
                project.status === 'completed' ? 'bg-green-500 text-white ring-2 ring-white' :
                project.status === 'in_progress' ? 'bg-yellow-500 text-white ring-2 ring-white' :
                'bg-white/30 text-white ring-2 ring-white/50'
              )}>
                {project.status.replace('_', ' ')}
              </span>
            </div>

            {/* Quick Stats */}
            <div className="mt-6 grid gap-4 sm:grid-cols-4">
              <div className="rounded-lg bg-white/20 backdrop-blur-sm p-4">
                <div className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-white" />
                  <div>
                    <p className="text-xs text-purple-100">Target Skills</p>
                    <p className="text-xl font-bold text-white">
                      {project.targetSkills.length}
                    </p>
                  </div>
                </div>
              </div>
              <div className="rounded-lg bg-white/20 backdrop-blur-sm p-4">
                <div className="flex items-center gap-2">
                  <Code className="h-5 w-5 text-white" />
                  <div>
                    <p className="text-xs text-purple-100">Difficulty</p>
                    <p className="text-xl font-bold capitalize text-white">
                      {project.difficulty}
                    </p>
                  </div>
                </div>
              </div>
              <div className="rounded-lg bg-white/20 backdrop-blur-sm p-4">
                <div className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-white" />
                  <div>
                    <p className="text-xs text-purple-100">Duration</p>
                    <p className="text-xl font-bold text-white">
                      {project.estimatedDuration}
                    </p>
                  </div>
                </div>
              </div>
              <div className="rounded-lg bg-white/20 backdrop-blur-sm p-4">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-white" />
                  <div>
                    <p className="text-xs text-purple-100">Milestones</p>
                    <p className="text-xl font-bold text-white">
                      {project.milestones.length}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-6 flex gap-3">
              {project.status === 'suggested' && (
                <button
                  onClick={() => handleStatusChange(ProjectStatus.ACCEPTED)}
                  disabled={isUpdatingStatus}
                  className="rounded-lg border-2 border-white/30 bg-white/20 backdrop-blur-sm px-6 py-3 font-semibold text-white hover:bg-white/30 transition-colors flex items-center gap-2"
                >
                  <Play className="h-5 w-5" />
                  Accept Project
                </button>
              )}
              {project.status === 'accepted' && (
                <button
                  onClick={() => handleStatusChange(ProjectStatus.IN_PROGRESS)}
                  disabled={isUpdatingStatus}
                  className="rounded-lg border-2 border-white/30 bg-white/20 backdrop-blur-sm px-6 py-3 font-semibold text-white hover:bg-white/30 transition-colors flex items-center gap-2"
                >
                  <Play className="h-5 w-5" />
                  Start Working
                </button>
              )}
              {project.status === 'in_progress' && (
                <button
                  onClick={() => setShowCompleteConfirm(true)}
                  disabled={isCompleting}
                  className="rounded-lg border-2 border-white/30 bg-white/20 backdrop-blur-sm px-6 py-3 font-semibold text-white hover:bg-white/30 transition-colors flex items-center gap-2"
                >
                  <Check className="h-5 w-5" />
                  Mark as Complete
                </button>
              )}
            </div>
          </div>

        {/* Objectives */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900">Learning Objectives</h2>
          <ul className="mt-4 space-y-2">
            {project.objectives.map((objective, index) => (
              <li key={index} className="flex items-start gap-3">
                <CheckCircle className="mt-0.5 h-5 w-5 flex-shrink-0 text-success" />
                <span className="text-gray-700">{objective}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Target Skills */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900">Skills You'll Build</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            {project.targetSkills.map((skill) => (
              <span key={skill} className="badge badge-primary">
                {skill}
              </span>
            ))}
          </div>
        </div>

        {/* Tech Stack */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900">Tech Stack</h2>
          <div className="mt-4 space-y-3">
            {project.techStack.map((tech, index) => (
              <div
                key={index}
                className="flex items-start gap-3 rounded-lg border border-gray-200 bg-gray-50 p-3"
              >
                <Code className="mt-0.5 h-5 w-5 flex-shrink-0 text-primary" />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <p className="font-semibold text-gray-900">
                      {tech.technology}
                    </p>
                    {tech.version && (
                      <span className="badge badge-neutral text-xs">
                        {tech.version}
                      </span>
                    )}
                  </div>
                  <p className="mt-1 text-sm text-gray-600">{tech.purpose}</p>
                </div>
                <span className="badge badge-primary capitalize">
                  {tech.category}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Milestones */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900">Project Milestones</h2>
          <div className="mt-6 space-y-6">
            {project.milestones.map((milestone, index) => (
              <div key={milestone.milestoneId || index} className="relative">
                {/* Connector Line */}
                {index < project.milestones.length - 1 && (
                  <div className="absolute left-6 top-12 h-full w-0.5 bg-gray-200" />
                )}

                <div className="flex gap-4">
                  {/* Number Badge */}
                  <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-white">
                    {index + 1}
                  </div>

                  {/* Content */}
                  <div className="flex-1 rounded-lg border border-gray-200 bg-white p-4 hover:shadow-md hover:border-purple-200 transition-all">
                    <h3 className="font-semibold text-gray-900">
                      {milestone.title}
                    </h3>
                    <p className="mt-2 text-sm text-gray-600">
                      {milestone.description}
                    </p>

                    {/* Tasks */}
                    <ul className="mt-4 space-y-2">
                      {milestone.tasks.map((task, taskIndex) => (
                        <li
                          key={taskIndex}
                          className="flex items-start gap-2 text-sm text-gray-700"
                        >
                          <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary" />
                          {task}
                        </li>
                      ))}
                    </ul>

                    {/* Estimated Hours */}
                    <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
                      <Clock className="h-4 w-4" />
                      <span>Estimated: {milestone.estimatedHours} hours</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Resources */}
        {project.resources.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900">
              Learning Resources
            </h2>
            <div className="mt-4 space-y-3">
              {project.resources.map((resource, index) => (
                <a
                  key={index}
                  href={resource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-start gap-3 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-all hover:bg-blue-50 hover:border-blue-300 hover:shadow-md"
                >
                  <BookOpen className="mt-0.5 h-5 w-5 flex-shrink-0 text-primary" />
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{resource.title}</p>
                    {resource.description && (
                      <p className="mt-1 text-sm text-gray-600">
                        {resource.description}
                      </p>
                    )}
                  </div>
                  <span className="badge badge-primary capitalize">
                    {resource.type}
                  </span>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Complete Confirmation Modal */}
      {showCompleteConfirm && (
        <div className="modal-overlay" onClick={() => setShowCompleteConfirm(false)}>
          <div
            className="modal-content max-w-md"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-xl font-bold text-gray-900">
              Complete Project?
            </h2>
            <p className="mt-4 text-gray-700">
              By marking this project as complete, your skills will be verified
              and your proficiency levels will be updated. This may unlock new
              internship opportunities!
            </p>
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setShowCompleteConfirm(false)}
                className="btn-secondary flex-1"
                disabled={isCompleting}
              >
                Cancel
              </button>
              <button
                onClick={handleComplete}
                className="btn-success flex-1"
                disabled={isCompleting}
              >
                {isCompleting ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                    Completing...
                  </span>
                ) : (
                  'Complete Project'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </MainLayout>
  );
}
