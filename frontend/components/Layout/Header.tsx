'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Menu,
  X,
  LayoutDashboard,
  User,
  Briefcase,
  FolderKanban,
  LogOut,
  Award,
  Linkedin,
  Github,
  FileText,
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useProfile } from '@/hooks/useProfile';
import { useSkillGraph } from '@/hooks/useSkillGraph';
import { APP_ROUTES } from '@/lib/constants';
import { cn, getInitials } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: APP_ROUTES.DASHBOARD, icon: LayoutDashboard },
  { name: 'Profile', href: APP_ROUTES.PROFILE, icon: User },
  { name: 'Internships', href: APP_ROUTES.INTERNSHIPS, icon: Briefcase },
  { name: 'Projects', href: APP_ROUTES.PROJECTS, icon: FolderKanban },
];

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const pathname = usePathname();
  const { user, signOut } = useAuth();
  const { profile } = useProfile();
  const { verifiedSkills } = useSkillGraph();

  return (
    <header className="sticky top-0 z-40 border-b-2 border-blue-100 bg-white/90 backdrop-blur-md shadow-sm">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <div className="flex items-center gap-8">
          <Link href={APP_ROUTES.DASHBOARD} className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-500 to-blue-600 shadow-lg">
              <span className="text-xl font-bold text-white">E</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-sky-600 to-blue-600 bg-clip-text text-transparent">Eligify</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden items-center gap-1 md:flex">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-sky-50 text-sky-600'
                      : 'text-gray-700 hover:bg-gray-100'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Right Side */}
        <div className="flex items-center gap-4">
          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              className="flex items-center gap-3 rounded-xl p-2 hover:bg-blue-50 transition-colors"
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-sky-500 to-blue-600 text-sm font-semibold text-white shadow-md">
                {user ? getInitials(user.name) : 'U'}
              </div>
              <div className="hidden text-left sm:block">
                <p className="text-sm font-semibold text-gray-900">
                  {user?.name || 'User'}
                </p>
                <p className="text-xs text-gray-500">
                  {verifiedSkills} verified skills
                </p>
              </div>
            </button>

            {/* Enhanced User Dropdown */}
            {userMenuOpen && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setUserMenuOpen(false)}
                />
                <div className="absolute right-0 z-20 mt-2 w-80 rounded-xl border border-gray-200 bg-white shadow-xl">
                  {/* Profile Header */}
                  <div className="border-b border-gray-200 bg-gradient-to-br from-sky-50 to-blue-50 p-4">
                    <div className="flex items-center gap-3">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-sky-500 to-blue-600 text-lg font-bold text-white">
                        {user ? getInitials(user.name) : 'U'}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-gray-900 truncate">
                          {profile?.personalInfo.name || user?.name || 'User'}
                        </p>
                        <p className="text-sm text-gray-600 truncate">
                          {profile?.personalInfo.email || user?.email}
                        </p>
                      </div>
                    </div>
                    
                    {/* Qualification */}
                    {profile?.education && profile.education.length > 0 && (
                      <div className="mt-3 text-xs text-gray-600">
                        {profile.education[0].degree} in {profile.education[0].field}
                      </div>
                    )}
                  </div>

                  {/* Skills Summary */}
                  <div className="border-b border-gray-200 p-4">
                    <div className="flex items-center gap-2 text-xs font-medium text-gray-700 mb-2">
                      <Award className="h-3.5 w-3.5 text-sky-600" />
                      Verified Skills
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-sky-500 to-blue-600"
                          style={{ width: `${Math.min((verifiedSkills / 10) * 100, 100)}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold text-gray-900">
                        {verifiedSkills}
                      </span>
                    </div>
                  </div>

                  {/* Links */}
                  <div className="p-2">
                    {profile?.personalInfo.linkedinUrl && (
                      <a
                        href={profile.personalInfo.linkedinUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                        onClick={() => setUserMenuOpen(false)}
                      >
                        <Linkedin className="h-4 w-4 text-blue-600" />
                        LinkedIn Profile
                      </a>
                    )}
                    {profile?.personalInfo.githubUsername && (
                      <a
                        href={`https://github.com/${profile.personalInfo.githubUsername}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                        onClick={() => setUserMenuOpen(false)}
                      >
                        <Github className="h-4 w-4 text-gray-900" />
                        GitHub Profile
                      </a>
                    )}
                    {profile?.resumeS3Uri && (
                      <Link
                        href={APP_ROUTES.PROFILE}
                        className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                        onClick={() => setUserMenuOpen(false)}
                      >
                        <FileText className="h-4 w-4 text-green-600" />
                        Resume Uploaded
                      </Link>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="border-t border-gray-200 p-2">
                    <Link
                      href={APP_ROUTES.PROFILE}
                      className="flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                      onClick={() => setUserMenuOpen(false)}
                    >
                      <User className="h-4 w-4" />
                      View Full Profile
                    </Link>
                    <button
                      onClick={() => {
                        setUserMenuOpen(false);
                        signOut();
                      }}
                      className="flex w-full items-center gap-3 px-3 py-2 text-sm text-danger hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <LogOut className="h-4 w-4" />
                      Sign Out
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="rounded-lg p-2 hover:bg-gray-100 md:hidden"
          >
            {mobileMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="border-t border-gray-200 bg-white px-4 py-4 md:hidden">
          <div className="space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium',
                    isActive
                      ? 'bg-sky-50 text-sky-600'
                      : 'text-gray-700 hover:bg-gray-100'
                  )}
                >
                  <Icon className="h-5 w-5" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
