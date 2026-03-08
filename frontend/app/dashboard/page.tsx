'use client';

import Link from 'next/link';
import {
  Award,
  Briefcase,
  FolderKanban,
  Upload,
  TrendingUp,
  CheckCircle,
} from 'lucide-react';
import MainLayout from '@/components/Layout/MainLayout';
import { useProfile } from '@/hooks/useProfile';
import { useSkillGraph } from '@/hooks/useSkillGraph';
import { useInternships } from '@/hooks/useInternships';
import { useProjects } from '@/hooks/useProjects';
import { APP_ROUTES } from '@/lib/constants';
import { cn } from '@/lib/utils';
import SkillGraph from '@/components/Skills/SkillGraph';
import { SkillSpiderChart, JobRoleRadarChart, SkillPrioritiesWidget } from '@/components/Dashboard';

function StatCard({
  title,
  value,
  icon: Icon,
  color,
  href,
}: {
  title: string;
  value: string | number;
  icon: React.ElementType;
  color: string;
  href?: string;
}) {
  const content = (
    <>
      <div className={cn('rounded-lg p-3', color)}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="mt-1 text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </>
  );

  if (href) {
    return (
      <Link
        href={href}
        className="card-hover flex items-center gap-4 transition-transform hover:scale-105"
      >
        {content}
      </Link>
    );
  }

  return <div className="card flex items-center gap-4">{content}</div>;
}

function QuickAction({
  title,
  description,
  icon: Icon,
  href,
  color,
}: {
  title: string;
  description: string;
  icon: React.ElementType;
  href: string;
  color: string;
}) {
  return (
    <Link
      href={href}
      className="card-hover group flex items-start gap-4 transition-transform hover:scale-105"
    >
      <div className={cn('rounded-lg p-3', color)}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <div className="flex-1">
        <h3 className="font-semibold text-gray-900 group-hover:text-primary">
          {title}
        </h3>
        <p className="mt-1 text-sm text-gray-600">{description}</p>
      </div>
    </Link>
  );
}

export default function DashboardPage() {
  const { profile, isLoading: profileLoading } = useProfile();
  const { skillGraph, isLoading: skillsLoading } = useSkillGraph();
  const { eligible, almostEligible, notEligible, isLoading: internshipsLoading } =
    useInternships();
  const { projects, isLoading: projectsLoading } = useProjects();

  const isLoading =
    profileLoading || skillsLoading || internshipsLoading || projectsLoading;

  if (isLoading) {
    return (
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="space-y-6 p-6">
            <div className="skeleton h-10 w-64"></div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="skeleton h-32"></div>
              ))}
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  // First-time user onboarding
  const isFirstTime = !profile?.resumeS3Uri && skillGraph?.totalSkills === 0;

  if (isFirstTime) {
    return (
      <MainLayout>
        <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
          <div className="flex min-h-[600px] items-center justify-center p-6">
            <div className="w-full max-w-2xl text-center">
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-primary/10">
              <Upload className="h-10 w-10 text-primary" />
            </div>
            <h1 className="mt-6 text-3xl font-bold text-gray-900">
              Welcome to Eligify!
            </h1>
            <p className="mt-4 text-lg text-gray-600">
              Let's get started by uploading your resume. Our AI will extract your 
              skills and match you with relevant internship opportunities.
            </p>
            
            <div className="mt-8 rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-12">
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-4 text-sm font-medium text-gray-900">
                Upload your resume to get started
              </p>
              <p className="mt-1 text-xs text-gray-500">
                PDF, DOCX, or TXT (max 10MB)
              </p>
              <Link
                href={APP_ROUTES.PROFILE}
                className="btn-primary mt-6 inline-flex items-center gap-2"
              >
                <Upload className="h-4 w-4" />
                Upload Resume
              </Link>
            </div>

            <div className="mt-8 grid gap-4 text-left sm:grid-cols-3">
              <div className="rounded-lg border border-gray-200 bg-white p-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100">
                  <span className="text-lg font-bold text-primary">1</span>
                </div>
                <p className="mt-3 text-sm font-medium text-gray-900">
                  Upload Resume
                </p>
                <p className="mt-1 text-xs text-gray-600">
                  AI extracts your skills automatically
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100">
                  <span className="text-lg font-bold text-primary">2</span>
                </div>
                <p className="mt-3 text-sm font-medium text-gray-900">
                  View Matches
                </p>
                <p className="mt-1 text-xs text-gray-600">
                  See eligible internships instantly
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-4">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100">
                  <span className="text-lg font-bold text-primary">3</span>
                </div>
                <p className="mt-3 text-sm font-medium text-gray-900">
                  Fill Gaps
                </p>
                <p className="mt-1 text-xs text-gray-600">
                  Build missing skills with AI projects
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
        <div className="space-y-8 p-6">
          {/* Welcome Section */}
          <div className="rounded-xl bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 p-6 text-white shadow-lg">
            <h1 className="text-3xl font-bold">
              Welcome back, {profile?.personalInfo.name?.split(' ')[0] || 'there'}!
            </h1>
            <p className="mt-2 text-purple-100">
              Here&apos;s your learning progress and opportunities
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Total Skills"
              value={skillGraph?.totalSkills || 0}
              icon={Award}
              color="bg-gradient-to-br from-purple-500 to-pink-500"
              href={APP_ROUTES.PROFILE}
            />
            <StatCard
              title="Verified Skills"
              value={skillGraph?.verifiedSkills || 0}
              icon={CheckCircle}
              color="bg-gradient-to-br from-pink-500 to-orange-400"
              href={APP_ROUTES.PROFILE}
            />
            <StatCard
              title="Eligible Internships"
              value={eligible.length}
              icon={Briefcase}
              color="bg-gradient-to-br from-orange-400 to-pink-400"
              href={APP_ROUTES.INTERNSHIPS}
            />
            <StatCard
              title="Almost Eligible"
              value={almostEligible.length}
              icon={TrendingUp}
              color="bg-gradient-to-br from-purple-500 to-orange-400"
              href={APP_ROUTES.INTERNSHIPS}
            />
          </div>

          {/* Data Visualizations */}
          <div className="grid gap-6 lg:grid-cols-2">
            <SkillSpiderChart skills={skillGraph?.skills || []} />
            <JobRoleRadarChart />
          </div>

          {/* Skill Priorities */}
          <SkillPrioritiesWidget />

          {/* Skill Graph */}
          <SkillGraph skills={skillGraph?.skills || []} />

          {/* Quick Actions */}
          <div>
            <h2 className="text-xl font-bold text-gray-900">Quick Actions</h2>
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {!profile?.resumeS3Uri && (
                <QuickAction
                  title="Upload Resume"
                  description="Let AI extract your skills and experience"
                  icon={Upload}
                  href={APP_ROUTES.PROFILE}
                  color="bg-gradient-to-br from-purple-500 to-pink-500"
                />
              )}
              <QuickAction
                title="Browse Internships"
                description="Discover opportunities matched to your skills"
                icon={Briefcase}
                href={APP_ROUTES.INTERNSHIPS}
                color="bg-gradient-to-br from-pink-500 to-orange-400"
              />
              <QuickAction
                title="Generate Project"
                description="Build skills with AI-powered project roadmaps"
                icon={FolderKanban}
                href={APP_ROUTES.PROJECTS}
                color="bg-gradient-to-br from-orange-400 to-pink-400"
              />
            </div>
          </div>

          {/* Learning Projects */}
          {projects.length > 0 && (
            <div>
              <h2 className="text-xl font-bold text-gray-900">Learning Projects</h2>
              <div className="mt-4 space-y-3">
                {projects.slice(0, 3).map((project) => {
                  const completedMilestones = 0;
                  const progressPercentage = (completedMilestones / project.milestones.length) * 100;
                  
                  return (
                    <Link
                      key={project.projectId}
                      href={APP_ROUTES.PROJECT_DETAIL(project.projectId)}
                      className="card-hover block"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 group-hover:text-primary">
                            {project.title}
                          </h3>
                          <p className="mt-1 text-sm text-gray-600 line-clamp-2">
                            {project.description}
                          </p>
                        </div>
                        <span
                          className={cn(
                            'badge ml-4',
                            project.status === 'completed'
                              ? 'badge-success'
                              : project.status === 'in_progress'
                                ? 'badge-warning'
                                : 'badge-neutral'
                          )}
                        >
                          {project.status.replace('_', ' ')}
                        </span>
                      </div>

                      <div className="mt-3 flex flex-wrap gap-2">
                        {project.targetSkills.slice(0, 5).map((skill) => (
                          <span key={skill} className="badge badge-primary text-xs">
                            {skill}
                          </span>
                        ))}
                        {project.targetSkills.length > 5 && (
                          <span className="badge badge-neutral text-xs">
                            +{project.targetSkills.length - 5} more
                          </span>
                        )}
                      </div>

                      <div className="mt-3">
                        <div className="flex items-center justify-between text-xs text-gray-600 mb-2">
                          <span>Progress</span>
                          <span>
                            {completedMilestones} / {project.milestones.length} milestones
                          </span>
                        </div>
                        <div className="relative h-1 w-full overflow-hidden bg-gray-200">
                          <div
                            className="h-full bg-blue-500 transition-all duration-500 ease-out relative"
                            style={{ width: `${progressPercentage}%` }}
                          >
                            {progressPercentage > 0 && (
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
                    </Link>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
}
