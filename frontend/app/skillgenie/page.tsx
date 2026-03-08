'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { ArrowLeft, Sparkles, CheckCircle, Circle, Play } from 'lucide-react';
import { APP_ROUTES } from '@/lib/constants';

export const dynamic = 'force-dynamic';

export default function SkillGenieDashboard() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [selectedSkill, setSelectedSkill] = useState('');

  useEffect(() => {
    const skillParam = searchParams.get('skill');
    if (skillParam) {
      setSelectedSkill(skillParam);
    }
  }, [searchParams]);

  const learningSteps = [
    {
      number: 1,
      title: 'Assessment',
      description: 'Test knowledge',
      status: 'current',
    },
    {
      number: 2,
      title: 'Project',
      description: 'Build & learn',
      status: 'upcoming',
    },
    {
      number: 3,
      title: 'Verification',
      description: 'Get verified',
      status: 'upcoming',
    },
  ];

  const handleStartAssessment = () => {
    router.push(`/skillgenie/assessment?skill=${encodeURIComponent(selectedSkill)}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white">
      {/* Top Bar */}
      <div className="border-b border-gray-200 bg-white/80 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.push(APP_ROUTES.DASHBOARD)}
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Eligify
            </button>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-purple-600 to-sky-600">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div>
                <div className="text-sm font-semibold text-gray-900">SkillGenie</div>
                <div className="text-xs text-gray-500">AI Learning Assistant</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-5xl px-8 py-12">
        {/* Header */}
        <div className="text-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-purple-100 px-4 py-2 text-sm font-medium text-purple-700">
            <Sparkles className="h-4 w-4" />
            Learning Journey
          </div>
          <h1 className="mt-6 text-4xl font-bold text-gray-900">
            Unlock Skill: <span className="bg-gradient-to-r from-sky-600 to-blue-600 bg-clip-text text-transparent">{selectedSkill || 'Select a Skill'}</span>
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Complete these 3 steps to master {selectedSkill} and unlock new opportunities
          </p>
        </div>

        {/* Compact Progress Tracker */}
        <div className="mt-12">
          <div className="relative">
            {/* Progress Line */}
            <div className="absolute left-0 right-0 top-8 h-0.5 bg-gray-200">
              <div className="h-full w-0 bg-gradient-to-r from-purple-600 to-sky-600 transition-all duration-500"></div>
            </div>

            {/* Steps */}
            <div className="relative grid grid-cols-3 gap-8">
              {learningSteps.map((step) => (
                <div key={step.number} className="text-center">
                  {/* Step Circle - Compact */}
                  <div className="relative mx-auto flex h-16 w-16 items-center justify-center">
                    <div
                      className={`flex h-full w-full items-center justify-center rounded-full border-3 transition-all ${
                        step.status === 'current'
                          ? 'border-sky-600 bg-sky-600 shadow-lg shadow-sky-200'
                          : step.status === 'completed'
                            ? 'border-success bg-success'
                            : 'border-gray-300 bg-white'
                      }`}
                    >
                      {step.status === 'completed' ? (
                        <CheckCircle className="h-8 w-8 text-white" />
                      ) : step.status === 'current' ? (
                        <span className="text-2xl font-bold text-white">
                          {step.number}
                        </span>
                      ) : (
                        <Circle className="h-8 w-8 text-gray-400" />
                      )}
                    </div>
                  </div>

                  {/* Step Info - Compact */}
                  <div className="mt-3">
                    <h3
                      className={`text-base font-semibold ${
                        step.status === 'current'
                          ? 'text-sky-600'
                          : step.status === 'completed'
                            ? 'text-success'
                            : 'text-gray-400'
                      }`}
                    >
                      {step.title}
                    </h3>
                    <p className="mt-0.5 text-xs text-gray-600">
                      {step.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Current Step Card */}
        <div className="mt-16 rounded-2xl border border-gray-200 bg-white p-8 shadow-xl">
          <div className="flex items-start gap-6">
            <div className="flex h-16 w-16 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-purple-600 to-sky-600">
              <span className="text-2xl font-bold text-white">1</span>
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900">
                Skill Assessment
              </h2>
              <p className="mt-2 text-gray-600">
                Let's evaluate your current understanding of {selectedSkill}. 
                This quick assessment will help us personalize your learning path.
              </p>

              <div className="mt-6 grid gap-4 sm:grid-cols-3">
                <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
                  <div className="text-2xl font-bold text-sky-600">5</div>
                  <div className="mt-1 text-sm text-gray-600">Questions</div>
                </div>
                <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
                  <div className="text-2xl font-bold text-sky-600">10</div>
                  <div className="mt-1 text-sm text-gray-600">Minutes</div>
                </div>
                <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
                  <div className="text-2xl font-bold text-sky-600">60%</div>
                  <div className="mt-1 text-sm text-gray-600">Pass Score</div>
                </div>
              </div>

              <button
                onClick={handleStartAssessment}
                disabled={!selectedSkill}
                className="mt-8 inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-sky-600 px-8 py-4 text-base font-semibold text-white shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Play className="h-5 w-5" />
                Start Assessment
              </button>
            </div>
          </div>
        </div>

        {/* Info Cards */}
        <div className="mt-8 grid gap-6 sm:grid-cols-2">
          <div className="rounded-xl border border-blue-200 bg-blue-50 p-6">
            <h3 className="font-semibold text-blue-900">💡 What to Expect</h3>
            <ul className="mt-3 space-y-2 text-sm text-blue-800">
              <li>• Multiple choice questions</li>
              <li>• Real-world scenario problems</li>
              <li>• Instant feedback on answers</li>
            </ul>
          </div>
          <div className="rounded-xl border border-purple-200 bg-purple-50 p-6">
            <h3 className="font-semibold text-purple-900">🎯 After Assessment</h3>
            <ul className="mt-3 space-y-2 text-sm text-purple-800">
              <li>• Pass: Move to main project</li>
              <li>• Need practice: Get beginner project</li>
              <li>• Personalized learning path</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
