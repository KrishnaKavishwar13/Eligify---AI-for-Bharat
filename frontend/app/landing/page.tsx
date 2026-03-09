import GradientButton from '@/components/GradientButton';
import SectionHeader from '@/components/SectionHeader';
import Card from '@/components/Card';
import SkillBar from '@/components/SkillBar';
import Image from 'next/image';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50/30 via-white to-purple-50/20">
      
      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 text-center">
        <div className="max-w-5xl mx-auto">
          {/* Logo and Brand */}
          <div className="inline-flex items-center gap-2 mb-8">
            <Image 
              src="/final-logo-eligify.png" 
              alt="Eligify Logo" 
              width={80} 
              height={80}
              className="object-contain"
            />
            <span className="text-5xl font-bold bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 bg-clip-text text-transparent">
              Eligify
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Stop Applying Blindly.
            <br />
            <span className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 bg-clip-text text-transparent">
              Start Unlocking Strategically.
            </span>
          </h1>

          {/* Subtext */}
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto font-medium">
            AI-powered employability system that maps your skills to real internship eligibility and builds what you're missing.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <GradientButton href="/auth/signup">
              Get Started
            </GradientButton>
            <GradientButton href="#how-it-works" variant="secondary">
              See How It Works
            </GradientButton>
          </div>
        </div>
      </section>

      {/* The Problem Section */}
      <section className="container mx-auto px-6 py-20">
        <SectionHeader 
          title="The Problem Today"
          subtitle="Students are stuck in a cycle of unstructured learning and blind applications"
        />

        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {/* Problem Card 1 */}
          <Card>
            <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Scattered Learning</h3>
            <p className="text-gray-600">No clear path from tutorials to employability</p>
          </Card>

          {/* Problem Card 2 */}
          <Card>
            <div className="w-12 h-12 bg-gradient-to-br from-pink-400 to-orange-400 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Random Projects</h3>
            <p className="text-gray-600">Building things that don't match real job requirements</p>
          </Card>

          {/* Problem Card 3 */}
          <Card>
            <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-pink-400 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Blind Applications</h3>
            <p className="text-gray-600">Applying without knowing if you actually qualify</p>
          </Card>

          {/* Problem Card 4 */}
          <Card>
            <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-orange-400 rounded-xl flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Low Shortlisting</h3>
            <p className="text-gray-600">Hundreds of applications, zero callbacks</p>
          </Card>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="container mx-auto px-6 py-20">
        <SectionHeader 
          title="How It Works"
          subtitle="A closed-loop system that turns skill gaps into verified competencies"
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
          {/* Step 1 */}
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white font-bold text-xl shadow-lg">
              1
            </div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">STEP 1 — Analyze Profile</h3>
            <p className="text-gray-600">AI maps your existing skills</p>
          </div>

          {/* Step 2 */}
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-orange-400 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white font-bold text-xl shadow-lg">
              2
            </div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">STEP 2 — Identify Gaps</h3>
            <p className="text-gray-600">Precise gap analysis for each role</p>
          </div>

          {/* Step 3 */}
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-pink-400 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white font-bold text-xl shadow-lg">
              3
            </div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">STEP 3 — Build Projects</h3>
            <p className="text-gray-600">AI-guided structured skill-building projects</p>
          </div>

          {/* Step 4 */}
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-orange-400 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white font-bold text-xl shadow-lg">
              4
            </div>
            <h3 className="text-lg font-bold text-gray-800 mb-2">STEP 4 — Unlock Roles</h3>
            <p className="text-gray-600">Verified skills match to internships</p>
          </div>
        </div>
      </section>

      {/* Skill Graph Section */}
      <section className="container mx-auto px-6 py-20">
        <SectionHeader 
          title="Your Skill Graph"
          subtitle="A living map of your competencies, continuously updated as you learn and build"
        />

        <div className="max-w-3xl mx-auto">
          <Card hover={false} className="p-10">
            <SkillBar name="React" percentage={82} />
            <SkillBar name="TypeScript" percentage={70} />
            <SkillBar name="Python" percentage={78} />
            <SkillBar name="Node.js" percentage={55} />
            <SkillBar name="SQL" percentage={45} />
            <SkillBar name="System Design" percentage={35} />
          </Card>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <Card className="p-12 bg-gradient-to-br from-purple-50 to-orange-50">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Ready to Build Your
              <br />
              <span className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 bg-clip-text text-transparent">
                Strategic Career Path?
              </span>
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Join Eligify and transform scattered learning into verified competencies that unlock real opportunities.
            </p>
            <GradientButton href="/auth/signup">
              Start Your Journey
            </GradientButton>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-8 text-center text-gray-500 border-t border-gray-200">
        <p className="text-sm">© 2025 Eligify. Strategic Career Intelligence for the Modern Student.</p>
      </footer>
    </div>
  );
}
