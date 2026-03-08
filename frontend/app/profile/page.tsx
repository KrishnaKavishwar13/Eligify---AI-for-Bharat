'use client';

import { useState } from 'react';
import { 
  Mail, 
  Phone, 
  MapPin, 
  Linkedin, 
  Github, 
  Globe, 
  GraduationCap,
  Briefcase,
  Award,
  Calendar,
  Building,
  ExternalLink,
  Edit,
  User,
  FileText
} from 'lucide-react';
import MainLayout from '@/components/Layout/MainLayout';
import ResumeUpload from '@/components/Profile/ResumeUpload';
import SkillGraph from '@/components/Skills/SkillGraph';
import EditProfileModal from '@/components/Profile/EditProfileModal';
import { useProfile } from '@/hooks/useProfile';
import { useSkillGraph } from '@/hooks/useSkillGraph';
import { notify } from '@/hooks/useNotifications';
import { getInitials } from '@/lib/utils';
import type { SkillCategory } from '@/types';

export default function ProfilePage() {
  const [showEditModal, setShowEditModal] = useState(false);
  const { profile, isLoading, updateProfile } = useProfile();
  const { skills, addSkill, isAddingSkill, skillGraph } = useSkillGraph();

  const handleAddSkill = async (skillName: string, category: SkillCategory) => {
    try {
      await addSkill({ skillName, category });
      notify.success('Skill added successfully!');
    } catch (error) {
      notify.error('Failed to add skill. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <MainLayout>
        <div className="space-y-6">
          <div className="skeleton h-10 w-64"></div>
          <div className="skeleton h-64"></div>
          <div className="skeleton h-96"></div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
        <div className="space-y-6 p-6">
          {/* Profile Header with Cover */}
          <div className="relative overflow-hidden rounded-2xl border-2 border-purple-100 bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 shadow-lg">
            {/* Cover Pattern */}
            <div className="absolute inset-0 opacity-10">
              <div className="absolute top-0 left-0 w-64 h-64 bg-purple-400 rounded-full blur-3xl"></div>
              <div className="absolute bottom-0 right-0 w-64 h-64 bg-orange-400 rounded-full blur-3xl"></div>
            </div>

          <div className="relative p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:gap-8">
              {/* Avatar */}
              <div className="flex-shrink-0">
                <div className="relative">
                  <div className="flex h-32 w-32 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 text-4xl font-bold text-white shadow-xl ring-4 ring-white">
                    {profile?.personalInfo.name ? getInitials(profile.personalInfo.name) : 'U'}
                  </div>
                  <div className="absolute -bottom-2 -right-2 rounded-full bg-white p-2 shadow-lg">
                    <Award className="h-6 w-6 text-purple-600" />
                  </div>
                </div>
              </div>

              {/* Profile Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <h1 className="text-3xl font-bold text-gray-900 truncate">
                      {profile?.personalInfo.name || 'User'}
                    </h1>
                    {profile?.education && profile.education.length > 0 && (
                      <p className="mt-1 text-lg text-gray-700">
                        {profile.education[0].degree} in {profile.education[0].field}
                      </p>
                    )}
                    {profile?.personalInfo.location && (
                      <div className="mt-2 flex items-center gap-2 text-gray-600">
                        <MapPin className="h-4 w-4" />
                        <span className="text-sm">{profile.personalInfo.location}</span>
                      </div>
                    )}
                  </div>
                  <button
                    onClick={() => setShowEditModal(true)}
                    className="flex items-center gap-2 rounded-lg border-2 border-blue-300 bg-white px-4 py-2 text-sm font-semibold text-blue-700 hover:bg-blue-50 transition-colors"
                  >
                    <Edit className="h-4 w-4" />
                    Edit Profile
                  </button>
                </div>

                {/* Quick Stats */}
                <div className="mt-6 grid grid-cols-3 gap-4">
                  <div className="rounded-xl bg-white/80 backdrop-blur-sm p-4 shadow-sm border border-blue-100">
                    <div className="flex items-center gap-2 text-sky-600">
                      <Award className="h-5 w-5" />
                      <span className="text-2xl font-bold">{skillGraph?.totalSkills || 0}</span>
                    </div>
                    <p className="mt-1 text-xs text-gray-600">Total Skills</p>
                  </div>
                  <div className="rounded-xl bg-white/80 backdrop-blur-sm p-4 shadow-sm border border-blue-100">
                    <div className="flex items-center gap-2 text-green-600">
                      <Award className="h-5 w-5" />
                      <span className="text-2xl font-bold">{skillGraph?.verifiedSkills || 0}</span>
                    </div>
                    <p className="mt-1 text-xs text-gray-600">Verified</p>
                  </div>
                  <div className="rounded-xl bg-white/80 backdrop-blur-sm p-4 shadow-sm border border-blue-100">
                    <div className="flex items-center gap-2 text-blue-600">
                      <Briefcase className="h-5 w-5" />
                      <span className="text-2xl font-bold">{profile?.experience?.length || 0}</span>
                    </div>
                    <p className="mt-1 text-xs text-gray-600">Experience</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Left Column - Contact & Links */}
          <div className="space-y-6 lg:col-span-1">
            {/* Contact Information */}
            <div className="card">
              <div className="flex items-center gap-2 mb-4">
                <User className="h-5 w-5 text-sky-600" />
                <h2 className="text-lg font-bold text-gray-900">Contact</h2>
              </div>
              <div className="space-y-4">
                <div className="flex items-start gap-3 group">
                  <Mail className="h-5 w-5 text-gray-400 mt-0.5 group-hover:text-sky-600 transition-colors" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-gray-500">Email</p>
                    <p className="font-medium text-gray-900 truncate text-sm">
                      {profile?.personalInfo.email}
                    </p>
                  </div>
                </div>

                {profile?.personalInfo.phone && (
                  <div className="flex items-start gap-3 group">
                    <Phone className="h-5 w-5 text-gray-400 mt-0.5 group-hover:text-sky-600 transition-colors" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-500">Phone</p>
                      <p className="font-medium text-gray-900 text-sm">
                        {profile.personalInfo.phone}
                      </p>
                    </div>
                  </div>
                )}

                {profile?.personalInfo.location && (
                  <div className="flex items-start gap-3 group">
                    <MapPin className="h-5 w-5 text-gray-400 mt-0.5 group-hover:text-sky-600 transition-colors" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-500">Location</p>
                      <p className="font-medium text-gray-900 text-sm">
                        {profile.personalInfo.location}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Social Links */}
            {(profile?.personalInfo.linkedinUrl || 
              profile?.personalInfo.githubUsername || 
              profile?.personalInfo.portfolioUrl) && (
              <div className="card">
                <div className="flex items-center gap-2 mb-4">
                  <Globe className="h-5 w-5 text-sky-600" />
                  <h2 className="text-lg font-bold text-gray-900">Links</h2>
                </div>
                <div className="space-y-3">
                  {profile?.personalInfo.linkedinUrl && (
                    <a
                      href={profile.personalInfo.linkedinUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between gap-3 rounded-lg border border-gray-200 bg-gray-50 p-3 hover:bg-blue-50 hover:border-blue-300 transition-all group"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                          <Linkedin className="h-5 w-5 text-white" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900">LinkedIn</p>
                          <p className="text-xs text-gray-500">View profile</p>
                        </div>
                      </div>
                      <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-blue-600 transition-colors" />
                    </a>
                  )}

                  {profile?.personalInfo.githubUsername && (
                    <a
                      href={`https://github.com/${profile.personalInfo.githubUsername}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between gap-3 rounded-lg border border-gray-200 bg-gray-50 p-3 hover:bg-gray-100 hover:border-gray-300 transition-all group"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-900">
                          <Github className="h-5 w-5 text-white" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900">GitHub</p>
                          <p className="text-xs text-gray-500">@{profile.personalInfo.githubUsername}</p>
                        </div>
                      </div>
                      <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-gray-900 transition-colors" />
                    </a>
                  )}

                  {profile?.personalInfo.portfolioUrl && (
                    <a
                      href={profile.personalInfo.portfolioUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-between gap-3 rounded-lg border border-gray-200 bg-gray-50 p-3 hover:bg-cyan-50 hover:border-cyan-300 transition-all group"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600">
                          <Globe className="h-5 w-5 text-white" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-gray-900">Portfolio</p>
                          <p className="text-xs text-gray-500">Visit website</p>
                        </div>
                      </div>
                      <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-cyan-600 transition-colors" />
                    </a>
                  )}
                </div>
              </div>
            )}

            {/* Resume Section */}
            <div className="card">
              <div className="flex items-center gap-2 mb-4">
                <FileText className="h-5 w-5 text-sky-600" />
                <h2 className="text-lg font-bold text-gray-900">Resume</h2>
              </div>
              <ResumeUpload />
            </div>
          </div>

          {/* Right Column - Education, Experience, Skills */}
          <div className="space-y-6 lg:col-span-2">
            {/* Education */}
            {profile?.education && profile.education.length > 0 && (
              <div className="card">
                <div className="flex items-center gap-2 mb-6">
                  <GraduationCap className="h-5 w-5 text-sky-600" />
                  <h2 className="text-lg font-bold text-gray-900">Education</h2>
                </div>
                <div className="space-y-6">
                  {profile.education.map((edu, index) => (
                    <div key={index} className="relative pl-8 pb-6 border-l-2 border-blue-200 last:pb-0">
                      <div className="absolute -left-2 top-0 h-4 w-4 rounded-full bg-gradient-to-br from-sky-500 to-blue-600 ring-4 ring-white"></div>
                      <div className="rounded-lg border border-blue-100 bg-gradient-to-br from-blue-50/50 to-white p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1 min-w-0">
                            <h3 className="font-bold text-gray-900 text-lg">
                              {edu.degree}
                            </h3>
                            <p className="mt-1 text-sky-700 font-medium">
                              {edu.field}
                            </p>
                            <div className="mt-2 flex items-center gap-2 text-gray-600">
                              <Building className="h-4 w-4" />
                              <span className="text-sm">{edu.institution}</span>
                            </div>
                          </div>
                          {edu.cgpa && (
                            <div className="flex-shrink-0 rounded-lg bg-green-100 px-3 py-2 text-center">
                              <div className="text-lg font-bold text-green-700">{edu.cgpa}</div>
                              <div className="text-xs text-green-600">CGPA</div>
                            </div>
                          )}
                        </div>
                        <div className="mt-3 flex items-center gap-2 text-sm text-gray-500">
                          <Calendar className="h-4 w-4" />
                          <span>
                            {new Date(edu.startDate).getFullYear()} -{' '}
                            {edu.current
                              ? 'Present'
                              : edu.endDate
                                ? new Date(edu.endDate).getFullYear()
                                : 'Present'}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Experience */}
            {profile?.experience && profile.experience.length > 0 && (
              <div className="card">
                <div className="flex items-center gap-2 mb-6">
                  <Briefcase className="h-5 w-5 text-sky-600" />
                  <h2 className="text-lg font-bold text-gray-900">Experience</h2>
                </div>
                <div className="space-y-6">
                  {profile.experience.map((exp, index) => (
                    <div key={index} className="relative pl-8 pb-6 border-l-2 border-green-200 last:pb-0">
                      <div className="absolute -left-2 top-0 h-4 w-4 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 ring-4 ring-white"></div>
                      <div className="rounded-lg border border-green-100 bg-gradient-to-br from-green-50/50 to-white p-4 hover:shadow-md transition-shadow">
                        <h3 className="font-bold text-gray-900 text-lg">{exp.role}</h3>
                        <div className="mt-1 flex items-center gap-2 text-green-700 font-medium">
                          <Building className="h-4 w-4" />
                          <span>{exp.company}</span>
                        </div>
                        <p className="mt-3 text-sm text-gray-700 leading-relaxed">
                          {exp.description}
                        </p>
                        <div className="mt-3 flex items-center gap-2 text-sm text-gray-500">
                          <Calendar className="h-4 w-4" />
                          <span>
                            {new Date(exp.startDate).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })} -{' '}
                            {exp.current
                              ? 'Present'
                              : exp.endDate
                                ? new Date(exp.endDate).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })
                                : 'Present'}
                          </span>
                        </div>
                        {exp.skills.length > 0 && (
                          <div className="mt-4 flex flex-wrap gap-2">
                            {exp.skills.map((skill) => (
                              <span key={skill} className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700 ring-1 ring-blue-200">
                                {skill}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Skills Section */}
            <SkillGraph skills={skills} onAddSkill={handleAddSkill} />
          </div>
        </div>
      </div>

      {/* Edit Profile Modal */}
      {showEditModal && profile && (
        <EditProfileModal
          profile={profile}
          onClose={() => setShowEditModal(false)}
          onSave={async (updates) => {
            await new Promise((resolve) => {
              updateProfile(updates, {
                onSuccess: resolve,
                onError: resolve,
              });
            });
          }}
        />
      )}
      </div>
    </MainLayout>
  );
}
