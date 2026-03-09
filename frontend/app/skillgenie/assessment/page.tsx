'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { ArrowLeft, CheckCircle, Sparkles, Loader2, AlertCircle } from 'lucide-react';
import { api } from '@/lib/api';

export const dynamic = 'force-dynamic';

interface Question {
  id: number;
  question: string;
  options: string[];
  correct_answer: number;
  explanation?: string;
}

interface QuizResult {
  score: number;
  total_questions: number;
  percentage: number;
  passed: boolean;
  correct_answers: number[];
  explanations: string[];
  feedback: string;
}

export default function SkillAssessmentPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const skillsParam = searchParams.get('skills') || searchParams.get('skill') || 'HR Basics';
  const skillsArray = skillsParam.split(',').map(s => s.trim());
  const primarySkill = skillsArray[0];
  const skillsDisplay = skillsArray.length > 1 
    ? `${skillsArray.slice(0, 2).join(', ')}${skillsArray.length > 2 ? ` +${skillsArray.length - 2} more` : ''}`
    : primarySkill;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [evaluating, setEvaluating] = useState(false);

  // Generate questions on mount
  useEffect(() => {
    generateQuestions();
  }, []);

  const generateQuestions = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await api.post('/assessment/generate-questions', {
        skill: primarySkill,
        difficulty: 'intermediate',
        num_questions: 5
      });
      
      if (response.data.success) {
        setQuestions(response.data.data.questions);
      } else {
        throw new Error('Failed to generate questions');
      }
    } catch (err: any) {
      console.error('Error generating questions:', err);
      setError(err.response?.data?.detail || 'Failed to generate questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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
      // Submit quiz for evaluation
      evaluateQuiz(newAnswers);
    }
  };

  const evaluateQuiz = async (finalAnswers: number[]) => {
    try {
      setEvaluating(true);
      
      const response = await api.post('/assessment/evaluate-quiz', {
        skill: primarySkill,
        questions: questions,
        answers: finalAnswers
      });
      
      if (response.data.success) {
        setResult(response.data.data);
        setShowResult(true);
      } else {
        throw new Error('Failed to evaluate quiz');
      }
    } catch (err: any) {
      console.error('Error evaluating quiz:', err);
      setError(err.response?.data?.detail || 'Failed to evaluate quiz. Please try again.');
    } finally {
      setEvaluating(false);
    }
  };

  const handleFinish = () => {
    if (result && result.passed) {
      router.push(`/skillgenie/project?skills=${encodeURIComponent(skillsParam)}&level=main`);
    } else {
      router.push(`/skillgenie/project?skills=${encodeURIComponent(skillsParam)}&level=beginner`);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
          <p className="mt-4 text-gray-600">Generating questions with AI...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error && !questions.length) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-xl p-8 shadow-xl text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto" />
          <h2 className="mt-4 text-xl font-bold text-gray-900">Error</h2>
          <p className="mt-2 text-gray-600">{error}</p>
          <button
            onClick={generateQuestions}
            className="mt-6 btn-primary"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Evaluating state
  if (evaluating) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
          <p className="mt-4 text-gray-600">Evaluating your answers...</p>
        </div>
      </div>
    );
  }

  // Result screen
  if (showResult && result) {
    const passed = result.passed;

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
              <div className="text-6xl font-bold text-primary">{result.percentage}%</div>
              <div className="mt-2 text-gray-600">
                {result.score} out of {result.total_questions} correct
              </div>
            </div>

            <div className="mt-8 rounded-lg border border-gray-200 bg-gray-50 p-6 text-left">
              <h3 className="font-semibold text-gray-900 mb-2">
                {passed ? '🎉 Great job!' : '💪 Keep going!'}
              </h3>
              <p className="text-sm text-gray-700">
                {result.feedback}
              </p>
            </div>

            {/* Show explanations for incorrect answers */}
            {result.correct_answers.some((correct, idx) => correct !== answers[idx]) && (
              <div className="mt-6 rounded-lg border border-blue-200 bg-blue-50 p-6 text-left">
                <h3 className="font-semibold text-blue-900 mb-3">Review Your Answers</h3>
                <div className="space-y-3">
                  {result.correct_answers.map((correct, idx) => {
                    if (correct !== answers[idx]) {
                      return (
                        <div key={idx} className="text-sm">
                          <p className="font-medium text-gray-900">Question {idx + 1}</p>
                          <p className="text-gray-700 mt-1">{result.explanations[idx]}</p>
                        </div>
                      );
                    }
                    return null;
                  })}
                </div>
              </div>
            )}

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

  // Quiz screen
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
              AI Generated
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
