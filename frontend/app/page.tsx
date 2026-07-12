import Link from "next/link";
import { ArrowRight, Sparkles, Target, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-12rem)] space-y-20 py-10">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-3xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-1000">
        <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80 mx-auto mb-4">
          <Sparkles className="w-4 h-4 mr-1" />
          LucentCV 2.0 is now live
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary pb-2">
          Elevate your career with AI-powered CV Analysis
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground leading-relaxed">
          Match your resume against job descriptions, generate personalized interview questions, and receive actionable feedback in seconds.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link href="/dashboard">
            <Button size="lg" className="w-full sm:w-auto font-semibold shadow-xl shadow-primary/25 group">
              Start Analysis
              <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
          <Link href="/history">
            <Button size="lg" variant="outline" className="w-full sm:w-auto">
              View History
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
        <div className="glass-card p-6 rounded-2xl space-y-4 hover:scale-[1.02] transition-transform">
          <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center text-primary">
            <Target className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold">Smart Matching</h3>
          <p className="text-muted-foreground text-sm">
            Advanced algorithms compare your CV against job requirements to give you a precise match score and actionable insights.
          </p>
        </div>
        
        <div className="glass-card p-6 rounded-2xl space-y-4 hover:scale-[1.02] transition-transform">
          <div className="w-12 h-12 bg-secondary/20 rounded-lg flex items-center justify-center text-secondary">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold">Actionable Feedback</h3>
          <p className="text-muted-foreground text-sm">
            Get instant feedback on what you're missing, strengths to highlight, and how to improve your chances of getting hired.
          </p>
        </div>

        <div className="glass-card p-6 rounded-2xl space-y-4 hover:scale-[1.02] transition-transform">
          <div className="w-12 h-12 bg-success/20 rounded-lg flex items-center justify-center text-success">
            <Sparkles className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold">Interview Prep</h3>
          <p className="text-muted-foreground text-sm">
            Generate custom behavioral and technical interview questions based on your CV and the specific role you want.
          </p>
        </div>
      </section>
    </div>
  );
}
