'use client';

import { X, CheckCircle, XCircle, ExternalLink } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { cn, formatCurrency, formatDate } from '@/lib/utils';
import { APP_ROUTES } from '@/lib/constants';
import type { InternshipMatch } from '@/types';

interface InternshipDetailModalProps {
  match: InternshipMatch;
  onClose: () => void;
}

export default function InternshipDetailModal({
  match,
  onClose,
}: InternshipDetailModalProps) {
  const router = useRouter();
  const { internship, matchScore, missingSkills, matchedSkills } = match;

  const handleUnlockWithSkillGenie = () => {
    // Navigate to SkillGenie assessment with missing skills
    const skillsParam = missingSkills.map((s) => s.skillName).join(',');
    router.push(`${APP_ROUTES.SKILLGENIE_ASSESSMENT}?skills=${encodeURIComponent(skillsParam)}`);
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content max-w-3xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">
              {internship.title}
            </h2>
            <p className="mt-1 text-lg text-gray-700">{internship.company}</p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 hover:bg-gray-100"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Match Score */}
        <div className="mt-6 rounded-lg bg-gradient-to-r from-primary/10 to-success/10 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Match Score</p>
              <p className="mt-1 text-4xl font-bold text-gray-900">
                {matchScore}%
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-gray-600">
                Skills Matched
              </p>
              <p className="mt-1 text-2xl font-bold text-gray-900">
                {matchedSkills.length} / {internship.requiredSkills.length}
              </p>
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="mt-6">
          <h3 className="font-semibold text-gray-900">About the Role</h3>
          <p className="mt-2 text-gray-700">{internship.description}</p>
        </div>

        {/* Details Grid */}
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm font-medium text-gray-600">Location</p>
            <p className="mt-1 text-gray-900">{internship.location}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">Type</p>
            <p className="mt-1 capitalize text-gray-900">{internship.type}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">Duration</p>
            <p className="mt-1 text-gray-900">{internship.duration}</p>
          </div>
          {internship.stipend && (
            <div>
              <p className="text-sm font-medium text-gray-600">Stipend</p>
              <p className="mt-1 text-gray-900">
                {formatCurrency(internship.stipend.amount)}/
                {internship.stipend.period}
              </p>
            </div>
          )}
          <div>
            <p className="text-sm font-medium text-gray-600">Start Date</p>
            <p className="mt-1 text-gray-900">
              {formatDate(internship.startDate)}
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">
              Application Deadline
            </p>
            <p className="mt-1 text-gray-900">
              {formatDate(internship.applicationDeadline)}
            </p>
          </div>
        </div>

        {/* Matched Skills */}
        {matchedSkills.length > 0 && (
          <div className="mt-6">
            <h3 className="flex items-center gap-2 font-semibold text-gray-900">
              <CheckCircle className="h-5 w-5 text-success" />
              Skills You Have
            </h3>
            <div className="mt-3 flex flex-wrap gap-2">
              {matchedSkills.map((skill) => (
                <span key={skill} className="badge badge-success">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Skills */}
        {missingSkills.length > 0 && (
          <div className="mt-6">
            <h3 className="flex items-center gap-2 font-semibold text-gray-900">
              <XCircle className="h-5 w-5 text-danger" />
              Skills to Build
            </h3>
            <div className="mt-3 space-y-3">
              {missingSkills.map((skill) => (
                <div
                  key={skill.skillName}
                  className="flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 p-3"
                >
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">
                      {skill.skillName}
                      {skill.required && (
                        <span className="ml-2 text-xs text-danger">
                          (Required)
                        </span>
                      )}
                    </p>
                    <div className="mt-2 flex items-center gap-4 text-sm text-gray-600">
                      <span>Current: {skill.currentProficiency}%</span>
                      <span>→</span>
                      <span>Target: {skill.targetProficiency}%</span>
                    </div>
                  </div>
                  <span
                    className={cn(
                      'badge',
                      skill.priority === 'high'
                        ? 'badge-danger'
                        : skill.priority === 'medium'
                          ? 'badge-warning'
                          : 'badge-neutral'
                    )}
                  >
                    {skill.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="mt-8 flex gap-3">
          {missingSkills.length > 0 && (
            <button
              onClick={handleUnlockWithSkillGenie}
              className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 px-6 py-3 text-sm font-bold text-white shadow-md transition-all duration-200 hover:from-indigo-700 hover:via-purple-700 hover:to-pink-700 hover:shadow-lg"
            >
              <span className="text-base">🎯</span>
              Unlock with SkillGenie
            </button>
          )}
          {internship.applicationUrl && (
            <a
              href={internship.applicationUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-green-600 to-emerald-600 px-6 py-3 text-sm font-bold text-white shadow-md transition-all duration-200 hover:from-green-700 hover:to-emerald-700 hover:shadow-lg"
            >
              <ExternalLink className="h-4 w-4" />
              Apply Now
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
