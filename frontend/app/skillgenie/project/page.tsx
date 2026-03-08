'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import {
  ArrowLeft,
  CheckCircle,
  Circle,
  BookOpen,
  ExternalLink,
  Github,
  MessageSquare,
  Send,
  Sparkles,
  X,
  Minimize2,
  Maximize2,
} from 'lucide-react';

export default function ProjectWorkspacePage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  // Handle both 'skill' (singular) and 'skills' (plural) parameters
  const skillsParam = searchParams.get('skills') || searchParams.get('skill') || 'HR Basics';
  const skillsArray = skillsParam.split(',').map(s => s.trim());
  const primarySkill = skillsArray[0];
  const skillsDisplay = skillsArray.length > 1 
    ? `${skillsArray.slice(0, 2).join(', ')}${skillsArray.length > 2 ? ` +${skillsArray.length - 2} more` : ''}`
    : primarySkill;
  
  const level = searchParams.get('level') || 'main';

  const [completedMilestones, setCompletedMilestones] = useState<number[]>([]);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{ role: 'user' | 'agent'; content: string }>>([
    {
      role: 'agent',
      content: `Hi! I'm your SkillGenie AI assistant. I'm here to help you with your ${skillsDisplay} project. Feel free to ask me anything about the milestones, best practices, or if you need guidance!`,
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const project = {
    title:
      level === 'beginner'
        ? `Introduction to ${skillsDisplay} - Beginner Project`
        : `${skillsDisplay} Professional Project`,
    description:
      level === 'beginner'
        ? `Build foundational knowledge of ${skillsDisplay} through a guided project that covers the essential concepts and practices.`
        : `Apply your ${skillsDisplay} knowledge to solve a real-world problem. This project will demonstrate your competency to potential employers.`,
    milestones: [
      {
        id: 1,
        title: 'Project Setup',
        description: 'Set up your project repository and environment',
        tasks: [
          'Create GitHub repository',
          'Set up project structure',
          'Initialize documentation',
        ],
      },
      {
        id: 2,
        title: 'Core Implementation',
        description: 'Implement the main features',
        tasks: [
          'Build primary functionality',
          'Add required components',
          'Implement best practices',
        ],
      },
      {
        id: 3,
        title: 'Testing & Documentation',
        description: 'Test your work and document the process',
        tasks: [
          'Test all functionality',
          'Write comprehensive README',
          'Add code comments',
        ],
      },
      {
        id: 4,
        title: 'Final Review',
        description: 'Review and prepare for submission',
        tasks: [
          'Code review checklist',
          'Verify all requirements',
          'Prepare submission',
        ],
      },
    ],
    resources: [
      {
        title: `${primarySkill} Best Practices Guide`,
        type: 'Documentation',
        url: '#',
      },
      {
        title: `${primarySkill} Video Tutorial Series`,
        type: 'Video',
        url: '#',
      },
      {
        title: `${primarySkill} Case Studies`,
        type: 'Article',
        url: '#',
      },
      {
        title: `${primarySkill} Community Forum`,
        type: 'Community',
        url: '#',
      },
    ],
  };

  const toggleMilestone = (id: number) => {
    if (completedMilestones.includes(id)) {
      setCompletedMilestones(completedMilestones.filter((m) => m !== id));
    } else {
      setCompletedMilestones([...completedMilestones, id]);
    }
  };

  const progress = (completedMilestones.length / project.milestones.length) * 100;
  const allCompleted = completedMilestones.length === project.milestones.length;

  const handleSubmit = () => {
    router.push(`/skillgenie/submit?skills=${encodeURIComponent(skillsParam)}`);
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage = { role: 'user' as const, content: inputMessage };
    setChatMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        `Great question! For ${skillsDisplay}, I recommend focusing on practical implementation. Start by breaking down the milestone into smaller tasks.`,
        `Here's a tip: Make sure to document your code as you go. This will help with the final review milestone and make your project more professional.`,
        `For this ${skillsDisplay} project, consider looking at industry best practices. Check out the resources in the sidebar for detailed guides.`,
        `That's a common challenge! Try approaching it step by step. First, ensure your project setup is complete, then move to implementation.`,
        `Good thinking! For ${skillsDisplay}, it's important to test each feature thoroughly. This will help you catch issues early.`,
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      
      setChatMessages((prev) => [
        ...prev,
        { role: 'agent', content: randomResponse },
      ]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-white">
      {/* Top Bar */}
      <div className="border-b border-gray-200 bg-white/80 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-8 py-4">
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
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600">
                Progress: {Math.round(progress)}%
              </div>
              <div className="h-1 w-20 overflow-hidden rounded-full bg-gray-200">
                <div
                  className="h-full bg-gradient-to-r from-purple-600 to-sky-600 transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-8 py-8">
        <div className="grid gap-8 lg:grid-cols-3">
          {/* Left Column - Project Info & Milestones */}
          <div className="lg:col-span-2 space-y-6">
            {/* Project Description */}
            <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-primary">
                  <BookOpen className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h1 className="text-2xl font-bold text-gray-900">
                    {project.title}
                  </h1>
                  <p className="mt-2 text-gray-600">{project.description}</p>
                  {level === 'beginner' && (
                    <div className="mt-4 rounded-lg border border-yellow-200 bg-yellow-50 p-3 text-sm text-yellow-800">
                      💡 This is a beginner-friendly project designed to help you 
                      build foundational skills in {skillsDisplay}.
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Milestones */}
            <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="text-xl font-bold text-gray-900">
                Project Milestones
              </h2>
              <div className="mt-6 space-y-4">
                {project.milestones.map((milestone, index) => {
                  const isCompleted = completedMilestones.includes(milestone.id);
                  return (
                    <div
                      key={milestone.id}
                      className={`rounded-lg border-2 p-4 transition-all ${
                        isCompleted
                          ? 'border-success bg-green-50'
                          : 'border-gray-200 bg-white'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <button
                          onClick={() => toggleMilestone(milestone.id)}
                          className={`mt-1 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border-2 transition-all ${
                            isCompleted
                              ? 'border-success bg-success'
                              : 'border-gray-300 hover:border-primary'
                          }`}
                        >
                          {isCompleted && (
                            <CheckCircle className="h-4 w-4 text-white" />
                          )}
                        </button>
                        <div className="flex-1">
                          <h3
                            className={`font-semibold ${
                              isCompleted ? 'text-success' : 'text-gray-900'
                            }`}
                          >
                            {index + 1}. {milestone.title}
                          </h3>
                          <p className="mt-1 text-sm text-gray-600">
                            {milestone.description}
                          </p>
                          <ul className="mt-3 space-y-1">
                            {milestone.tasks.map((task, taskIndex) => (
                              <li
                                key={taskIndex}
                                className="flex items-center gap-2 text-sm text-gray-700"
                              >
                                <Circle className="h-1.5 w-1.5 fill-current text-gray-400" />
                                {task}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              disabled={!allCompleted}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-primary px-6 py-4 font-semibold text-white shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Github className="h-5 w-5" />
              {allCompleted ? 'Submit Project' : 'Complete All Milestones First'}
            </button>
          </div>

          {/* Right Column - Resources & Agent Chat */}
          <div className="space-y-6">
            {/* Agent Chat Card */}
            <div className="rounded-xl border border-purple-200 bg-gradient-to-br from-purple-50 to-blue-50 p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-purple-600 to-primary">
                    <Sparkles className="h-4 w-4 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">SkillGenie AI</h3>
                    <p className="text-xs text-gray-600">Your project assistant</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsChatOpen(!isChatOpen)}
                  className="rounded-lg bg-gradient-to-r from-purple-600 to-primary px-4 py-2 text-sm font-medium text-white shadow-md hover:shadow-lg transition-all"
                >
                  {isChatOpen ? 'Close Chat' : 'Open Chat'}
                </button>
              </div>
              
              {!isChatOpen && (
                <p className="mt-3 text-sm text-gray-700">
                  Need help with your project? Chat with our AI assistant for guidance, tips, and answers to your questions.
                </p>
              )}
            </div>

            {/* Chat Window */}
            {isChatOpen && (
              <div className={`rounded-xl border border-gray-200 bg-white shadow-xl transition-all ${isMinimized ? 'h-14' : 'h-[500px]'} flex flex-col`}>
                {/* Chat Header */}
                <div className="flex items-center justify-between border-b border-gray-200 bg-gradient-to-r from-purple-600 to-primary px-4 py-3 rounded-t-xl">
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-white" />
                    <div>
                      <h3 className="font-semibold text-white">SkillGenie AI</h3>
                      <p className="text-xs text-purple-100">Always here to help</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setIsMinimized(!isMinimized)}
                      className="rounded-lg p-1 text-white hover:bg-white/20 transition-colors"
                    >
                      {isMinimized ? <Maximize2 className="h-4 w-4" /> : <Minimize2 className="h-4 w-4" />}
                    </button>
                    <button
                      onClick={() => setIsChatOpen(false)}
                      className="rounded-lg p-1 text-white hover:bg-white/20 transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {!isMinimized && (
                  <>
                    {/* Chat Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                      {chatMessages.map((message, index) => (
                        <div
                          key={index}
                          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-[85%] rounded-lg px-4 py-2 ${
                              message.role === 'user'
                                ? 'bg-gradient-to-r from-purple-600 to-primary text-white'
                                : 'bg-gray-100 text-gray-900'
                            }`}
                          >
                            {message.role === 'agent' && (
                              <div className="mb-1 flex items-center gap-1 text-xs font-medium text-purple-600">
                                <Sparkles className="h-3 w-3" />
                                SkillGenie
                              </div>
                            )}
                            <p className="text-sm">{message.content}</p>
                          </div>
                        </div>
                      ))}
                      
                      {isTyping && (
                        <div className="flex justify-start">
                          <div className="max-w-[85%] rounded-lg bg-gray-100 px-4 py-2">
                            <div className="flex items-center gap-1 text-xs font-medium text-purple-600 mb-1">
                              <Sparkles className="h-3 w-3" />
                              SkillGenie
                            </div>
                            <div className="flex gap-1">
                              <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0ms' }}></div>
                              <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '150ms' }}></div>
                              <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '300ms' }}></div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Quick Actions */}
                    <div className="border-t border-gray-200 bg-gray-50 px-4 py-2">
                      <div className="flex flex-wrap gap-2">
                        <button
                          onClick={() => {
                            setInputMessage('How do I start this project?');
                            setTimeout(() => handleSendMessage(), 100);
                          }}
                          className="rounded-full border border-purple-200 bg-white px-3 py-1 text-xs text-purple-700 hover:bg-purple-50 transition-colors"
                        >
                          How to start?
                        </button>
                        <button
                          onClick={() => {
                            setInputMessage(`What are best practices for ${skillsDisplay}?`);
                            setTimeout(() => handleSendMessage(), 100);
                          }}
                          className="rounded-full border border-purple-200 bg-white px-3 py-1 text-xs text-purple-700 hover:bg-purple-50 transition-colors"
                        >
                          Best practices
                        </button>
                        <button
                          onClick={() => {
                            setInputMessage('I need help with testing');
                            setTimeout(() => handleSendMessage(), 100);
                          }}
                          className="rounded-full border border-purple-200 bg-white px-3 py-1 text-xs text-purple-700 hover:bg-purple-50 transition-colors"
                        >
                          Testing help
                        </button>
                      </div>
                    </div>

                    {/* Chat Input */}
                    <div className="border-t border-gray-200 p-4">
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={inputMessage}
                          onChange={(e) => setInputMessage(e.target.value)}
                          onKeyPress={handleKeyPress}
                          placeholder="Ask me anything..."
                          className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                        />
                        <button
                          onClick={handleSendMessage}
                          disabled={!inputMessage.trim()}
                          className="flex items-center justify-center rounded-lg bg-gradient-to-r from-purple-600 to-primary px-4 py-2 text-white shadow-md hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <Send className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            )}

            {/* Learning Resources */}
            <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-bold text-gray-900">
                Learning Resources
              </h2>
              <p className="mt-2 text-sm text-gray-600">
                Helpful materials to guide your project
              </p>
              <div className="mt-4 space-y-3">
                {project.resources.map((resource, index) => (
                  <a
                    key={index}
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-start gap-3 rounded-lg border border-gray-200 bg-gray-50 p-3 transition-colors hover:bg-gray-100"
                  >
                    <BookOpen className="mt-0.5 h-5 w-5 flex-shrink-0 text-primary" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">
                        {resource.title}
                      </p>
                      <p className="text-xs text-gray-500">{resource.type}</p>
                    </div>
                    <ExternalLink className="h-4 w-4 flex-shrink-0 text-gray-400" />
                  </a>
                ))}
              </div>
            </div>

            {/* Tips Card */}
            <div className="rounded-xl border border-blue-200 bg-blue-50 p-6">
              <h3 className="font-semibold text-blue-900">💡 Pro Tips</h3>
              <ul className="mt-3 space-y-2 text-sm text-blue-800">
                <li>• Commit your code regularly</li>
                <li>• Write clear documentation</li>
                <li>• Follow best practices</li>
                <li>• Test thoroughly before submitting</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
