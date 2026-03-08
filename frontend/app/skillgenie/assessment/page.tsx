'use client';

import { useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { ArrowLeft, CheckCircle, Sparkles } from 'lucide-react';

export const dynamic = 'force-dynamic';

interface Question {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
}

export default function SkillAssessmentPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  // Handle both 'skill' (singular) and 'skills' (plural) parameters
  const skillsParam = searchParams.get('skills') || searchParams.get('skill') || 'HR Basics';
  const skillsArray = skillsParam.split(',').map(s => s.trim());
  const primarySkill = skillsArray[0];
  const skillsDisplay = skillsArray.length > 1 
    ? `${skillsArray.slice(0, 2).join(', ')}${skillsArray.length > 2 ? ` +${skillsArray.length - 2} more` : ''}`
    : primarySkill;

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);

  // Generate questions based on the skills
  const questions: Question[] = [
    {
      id: 1,
      question: `What is a fundamental concept you should understand about ${primarySkill}?`,
      options: [
        'Basic syntax and structure',
        'Advanced optimization techniques',
        'Enterprise architecture patterns',
        'Legacy system maintenance',
      ],
      correctAnswer: 0,
    },
    {
      id: 2,
      question: `Which of the following is a common use case for ${primarySkill}?`,
      options: [
        'Building scalable applications',
        'Managing hardware resources',
        'Designing physical products',
        'Conducting market research',
      ],
      correctAnswer: 0,
    },
    {
      id: 3,
      question: `What is an important best practice when working with ${primarySkill}?`,
      options: [
        'Ignoring documentation',
        'Writing clean, maintainable code',
        'Avoiding testing',
        'Using deprecated features',
      ],
      correctAnswer: 1,
    },
    {
      id: 4,
      question: `How would you approach learning ${primarySkill} effectively?`,
      options: [
        'Only reading theory',
        'Memorizing syntax without practice',
        'Building hands-on projects',
        'Avoiding community resources',
      ],
      correctAnswer: 2,
    },
    {
      id: 5,
      question: `What makes ${primarySkill} valuable in the job market?`,
      options: [
        'It\'s rarely used',
        'It solves real-world problems',
        'It\'s only for beginners',
        'It has no practical applications',
      ],
      correctAnswer: 1,
    },
  ];

  const handleAnswerSelect = (answerIndex: number) => {
    setSelectedAnswer(answerIndex);
  };

  const handleNext = () => {
    if (selectedAnswer === null) return;

    const newAnswers = [...answers, selectedAnswer];
    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
    } else {
      // Calculate score
      const correctCount = newAnswers.reduce((count, answer, index) => {
        return answer === questions[index].correctAnswer ? count + 1 : count;
      }, 0);
      const finalScore = (correctCount / questions.length) * 100;
      setScore(finalScore);
      setShowResult(true);
    }
  };

  const handleFinish = () => {
    if (score >= 60) {
      // Passed - go to main project
      router.push(`/skillgenie/project?skills=${encodeURIComponent(skillsParam)}&level=main`);
    } else {
      // Failed - go to beginner project
      router.push(`/skillgenie/project?skills=${encodeURIComponent(skillsParam)}&level=beginner`);
    }
  };

  if (showResult) {
    const passed = score >= 60;

    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white">
        <div className="mx-auto max-w-3xl px-8 py-12">
          <div className="rounded-2xl border border-gray-200 bg-white p-12 text-center shadow-xl">
            <div
              className={`mx-auto flex h-24 w-24 items-center justify-center rounded-full ${
                passed ? 'bg-green-100' : 'bg-yellow-100'
              }`}
            >
              {passed ? (
                <CheckCircle className="h-12 w-12 text-success" />
              ) : (
                <Sparkles className="h-12 w-12 text-warning" />
              )}
            </div>

            <h1 className="mt-6 text-3xl font-bold text-gray-900">
              {passed ? 'Assessment Passed!' : 'Keep Learning!'}
            </h1>

            <div className="mt-6">
              <div className="text-6xl font-bold text-primary">{score}%</div>
              <div className="mt-2 text-gray-600">Your Score</div>
            </div>

            <div className="mt-8 rounded-lg border border-gray-200 bg-gray-50 p-6">
              {passed ? (
                <>
                  <h3 className="font-semibold text-gray-900">
                    Great job! You're ready for the main project.
                  </h3>
                  <p className="mt-2 text-sm text-gray-600">
                    You've demonstrated a solid understanding of {skillsDisplay}. 
                    Let's move on to building a real-world project.
                  </p>
                </>
              ) : (
                <>
                  <h3 className="font-semibold text-gray-900">
                    Start with a foundational project
                  </h3>
                  <p className="mt-2 text-sm text-gray-600">
                    No worries! We'll start with a beginner-friendly project 
                    to help you build the basics of {skillsDisplay}.
                  </p>
                </>
              )}
            </div>

            <button
              onClick={handleFinish}
              className="mt-8 inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-primary px-8 py-4 text-base font-semibold text-white shadow-lg hover:shadow-xl transition-all"
            >
              Continue to Project
            </button>
          </div>
        </div>
      </div>
    );
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white">
      {/* Top Bar */}
      <div className="border-b border-gray-200 bg-white/80 backdrop-blur-sm">
        <div className="mx-auto max-w-5xl px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => router.back()}
                className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </button>
              <div className="h-4 w-px bg-gray-300"></div>
              <div className="text-sm font-medium text-gray-900">
                Skills: <span className="text-sky-600">{skillsDisplay}</span>
              </div>
            </div>
            <div className="text-sm font-medium text-gray-600">
              Question {currentQuestion + 1} of {questions.length}
            </div>
          </div>
          {/* Progress Bar */}
          <div className="mt-4 h-1 w-full overflow-hidden rounded-full bg-gray-200">
            <div
              className="h-full bg-gradient-to-r from-purple-600 to-sky-600 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="mx-auto max-w-3xl px-8 py-12">
        <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl">
          {/* Question */}
          <div className="mb-8">
            <div className="inline-flex items-center gap-2 rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-700">
              <Sparkles className="h-4 w-4" />
              {skillsDisplay}
            </div>
            <h2 className="mt-4 text-2xl font-bold text-gray-900">
              {questions[currentQuestion].question}
            </h2>
          </div>

          {/* Options */}
          <div className="space-y-3">
            {questions[currentQuestion].options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                className={`w-full rounded-lg border-2 p-4 text-left transition-all ${
                  selectedAnswer === index
                    ? 'border-primary bg-blue-50'
                    : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border-2 ${
                      selectedAnswer === index
                        ? 'border-primary bg-primary'
                        : 'border-gray-300'
                    }`}
                  >
                    {selectedAnswer === index && (
                      <div className="h-2 w-2 rounded-full bg-white" />
                    )}
                  </div>
                  <span className="font-medium text-gray-900">{option}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Next Button */}
          <button
            onClick={handleNext}
            disabled={selectedAnswer === null}
            className="mt-8 w-full rounded-lg bg-gradient-to-r from-purple-600 to-primary px-6 py-4 font-semibold text-white shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {currentQuestion < questions.length - 1 ? 'Next Question' : 'Finish Assessment'}
          </button>
        </div>
      </div>
    </div>
  );
}
