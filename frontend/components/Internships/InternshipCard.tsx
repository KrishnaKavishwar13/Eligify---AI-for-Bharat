'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  MapPin,
  Calendar,
  DollarSign,
  Briefcase,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { APP_ROUTES } from '@/lib/constants';
import type { InternshipMatch } from '@/types';
import InternshipDetailModal from './InternshipDetailModal';

interface InternshipCardProps {
  match: InternshipMatch;
  category: 'eligible' | 'almostEligible' | 'notEligible';
}

// Company type classification with professional metallic colors and highlight backgrounds
const getCompanyType = (company: string): { type: string; borderColor: string; accentColor: string; highlightBg: string } => {
  const companyLower = company.toLowerCase();
  
  // FAANG - Platinum with subtle slate highlight
  if (['google', 'amazon', 'microsoft', 'meta', 'apple', 'netflix'].some(c => companyLower.includes(c))) {
    return { 
      type: 'FAANG', 
      borderColor: 'border-slate-300',
      accentColor: 'bg-slate-600',
      highlightBg: 'from-slate-50/80 to-white'
    };
  }
  
  // Top MNCs - Steel Blue with blue highlight
  if (['nvidia', 'salesforce', 'adobe', 'oracle', 'ibm', 'intel', 'cisco'].some(c => companyLower.includes(c))) {
    return { 
      type: 'Top MNC', 
      borderColor: 'border-blue-300',
      accentColor: 'bg-blue-600',
      highlightBg: 'from-blue-50/80 to-white'
    };
  }
  
  // Indian Unicorns - Bronze with amber highlight
  if (['flipkart', 'swiggy', 'zomato', 'ola', 'paytm', 'phonepe', 'razorpay', 'myntra', 'dream11', 'unacademy'].some(c => companyLower.includes(c))) {
    return { 
      type: 'Unicorn', 
      borderColor: 'border-amber-300',
      accentColor: 'bg-amber-600',
      highlightBg: 'from-amber-50/80 to-white'
    };
  }
  
  // Startups - Emerald with green highlight
  if (['polygon', 'freshworks'].some(c => companyLower.includes(c))) {
    return { 
      type: 'Startup', 
      borderColor: 'border-emerald-300',
      accentColor: 'bg-emerald-600',
      highlightBg: 'from-emerald-50/80 to-white'
    };
  }
  
  // Enterprise - Gunmetal with indigo highlight
  if (['jio', 'bosch', 'accenture', 'tcs', 'infosys', 'wipro'].some(c => companyLower.includes(c))) {
    return { 
      type: 'Enterprise', 
      borderColor: 'border-indigo-300',
      accentColor: 'bg-indigo-600',
      highlightBg: 'from-indigo-50/80 to-white'
    };
  }
  
  // Default with gray highlight
  return { 
    type: 'Company', 
    borderColor: 'border-gray-300',
    accentColor: 'bg-gray-600',
    highlightBg: 'from-gray-50/80 to-white'
  };
};

export default function InternshipCard({
  match,
  category,
}: InternshipCardProps) {
  const router = useRouter();
  const [showModal, setShowModal] = useState(false);
  const { internship, matchScore, missingSkills = [], matchedSkills = [] } = match;
  const companyInfo = getCompanyType(internship.company);

  const handleUnlockWithSkillGenie = (e: React.MouseEvent) => {
    e.stopPropagation();
    // Navigate to SkillGenie assessment with missing skills
    const skillsParam = missingSkills.join(',');
    router.push(`${APP_ROUTES.SKILLGENIE_ASSESSMENT}?skills=${encodeURIComponent(skillsParam)}`);
  };

  return (
    <>
      <div
        className="group relative cursor-pointer transition-all duration-200 hover:-translate-y-1"
        onClick={() => setShowModal(true)}
      >
        {/* Professional Card Container with highlight color */}
        <div className={cn(
          "relative w-full overflow-hidden rounded-lg bg-gradient-to-br border-2 shadow-sm transition-all duration-200 group-hover:shadow-md",
          companyInfo.borderColor,
          companyInfo.highlightBg
        )}>
          {/* Subtle Top Accent Bar */}
          <div className={cn("h-1 w-full", companyInfo.accentColor)} />

          {/* Content */}
          <div className="relative flex flex-col p-5">
            {/* Header - Company Type & Match Score */}
            <div className="flex items-start justify-between mb-3">
              <div className={cn(
                'px-2.5 py-1 rounded text-xs font-semibold text-white',
                companyInfo.accentColor
              )}>
                {companyInfo.type}
              </div>
              
              {/* Match Score Badge */}
              <div className={cn(
                "px-3 py-1 rounded font-bold text-sm text-white",
                matchScore >= 90 ? 'bg-green-600' : matchScore >= 70 ? 'bg-amber-600' : 'bg-red-600'
              )}>
                {matchScore}% Match
              </div>
            </div>

            {/* Company Logo Placeholder */}
            <div className="flex items-center justify-center mb-3">
              <div className="h-12 w-12 rounded-lg bg-gray-100 border border-gray-200 flex items-center justify-center">
                <Briefcase className="h-6 w-6 text-gray-400" />
              </div>
            </div>

            {/* Title & Company */}
            <div className="mb-3">
              <h3 className="text-base font-bold text-gray-900 leading-tight line-clamp-2 mb-1.5">
                {internship.title}
              </h3>
              <p className="text-sm font-semibold text-gray-600">
                {internship.company}
              </p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-2 mb-3">
              <div className="rounded border border-gray-200 bg-gray-50 p-2">
                <div className="flex items-center gap-1.5 mb-0.5">
                  <DollarSign className="h-3.5 w-3.5 text-gray-500" />
                  <span className="text-xs text-gray-500">Stipend</span>
                </div>
                <div className="text-sm font-bold text-gray-900">
                  ₹{((internship.stipend?.amount || 0) / 1000).toFixed(0)}K/mo
                </div>
              </div>
              
              <div className="rounded border border-gray-200 bg-gray-50 p-2">
                <div className="flex items-center gap-1.5 mb-0.5">
                  <Calendar className="h-3.5 w-3.5 text-gray-500" />
                  <span className="text-xs text-gray-500">Duration</span>
                </div>
                <div className="text-sm font-bold text-gray-900">
                  {internship.duration}
                </div>
              </div>
            </div>

            {/* Location & Type */}
            <div className="flex items-center gap-3 mb-3 text-xs text-gray-600">
              <div className="flex items-center gap-1">
                <MapPin className="h-3.5 w-3.5" />
                <span>{internship.location.split(',')[0]}</span>
              </div>
              <span>•</span>
              <span className="capitalize">{internship.type}</span>
            </div>

            {/* Skills Match Progress */}
            <div className="mb-3">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-semibold text-gray-700">Skills Match</span>
                <span className="text-xs font-bold text-gray-900">
                  {matchedSkills.length}/{internship.requiredSkills.length}
                </span>
              </div>
              <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gray-700 rounded-full transition-all duration-500"
                  style={{ width: `${(matchedSkills.length / internship.requiredSkills.length) * 100}%` }}
                />
              </div>
            </div>

            {/* Action Buttons */}
            {missingSkills.length > 0 ? (
              <div className="space-y-2">
                <button
                  onClick={handleUnlockWithSkillGenie}
                  className="w-full rounded-lg py-3 text-sm font-bold transition-all duration-200 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white hover:from-indigo-700 hover:via-purple-700 hover:to-pink-700 shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                >
                  <span className="text-base">🎯</span>
                  <span>Unlock with SkillGenie</span>
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowModal(true);
                  }}
                  className="w-full rounded-lg py-2.5 text-sm font-semibold transition-all duration-200 bg-white text-gray-700 border-2 border-gray-300 hover:border-gray-400 hover:bg-gray-50"
                >
                  View Details
                </button>
              </div>
            ) : (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setShowModal(true);
                }}
                className="w-full rounded-lg py-3 text-sm font-bold transition-all duration-200 bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:from-green-700 hover:to-emerald-700 shadow-md hover:shadow-lg"
              >
                ✓ Apply Now
              </button>
            )}
          </div>
        </div>
      </div>

      {showModal && (
        <InternshipDetailModal
          match={match}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}
