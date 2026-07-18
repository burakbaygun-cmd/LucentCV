"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { Sparkles, FileText, Briefcase } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/services/api";
import { useAuth } from "@/context/AuthContext";

export default function Dashboard() {
  const router = useRouter();
  const { user } = useAuth();
  const [cvText, setCvText] = useState("");
  const [jobText, setJobText] = useState("");

  const analyzeMutation = useMutation({
    mutationFn: () => api.analyze({ cv_text: cvText, job_text: jobText, user_id: user?.id || "guest" }),
    onSuccess: (data) => {
      toast.success("Analysis complete!");
      router.push(`/analysis/${data.analysis_id}`);
    },
    onError: (error) => {
      console.error(error);
      toast.error("Failed to analyze. Please try again.");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!cvText.trim() || !jobText.trim()) {
      toast.error("Please provide both CV and Job Description.");
      return;
    }
    analyzeMutation.mutate();
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Paste your CV and the Job Description below to get an instant AI match analysis.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CV Input */}
        <Card className="glass-card flex flex-col h-full border-primary/20 shadow-primary/5">
          <CardHeader>
            <CardTitle className="flex items-center text-xl">
              <FileText className="w-5 h-5 mr-2 text-primary" />
              Your CV
            </CardTitle>
            <CardDescription>Paste the plain text of your resume here.</CardDescription>
          </CardHeader>
          <CardContent className="flex-1">
            <Textarea
              placeholder="John Doe&#10;Software Engineer&#10;&#10;Experience...&#10;Skills..."
              className="min-h-[400px] h-full resize-none bg-background/50 border-white/10 focus-visible:ring-primary"
              value={cvText}
              onChange={(e) => setCvText(e.target.value)}
              disabled={analyzeMutation.isPending}
            />
          </CardContent>
        </Card>

        {/* Job Input */}
        <Card className="glass-card flex flex-col h-full border-secondary/20 shadow-secondary/5">
          <CardHeader>
            <CardTitle className="flex items-center text-xl">
              <Briefcase className="w-5 h-5 mr-2 text-secondary" />
              Job Description
            </CardTitle>
            <CardDescription>Paste the job posting requirements here.</CardDescription>
          </CardHeader>
          <CardContent className="flex-1">
            <Textarea
              placeholder="We are looking for a Senior Software Engineer...&#10;&#10;Requirements:&#10;- React&#10;- Python"
              className="min-h-[400px] h-full resize-none bg-background/50 border-white/10 focus-visible:ring-secondary"
              value={jobText}
              onChange={(e) => setJobText(e.target.value)}
              disabled={analyzeMutation.isPending}
            />
          </CardContent>
        </Card>

        <div className="lg:col-span-2 flex justify-end mt-4">
          <Button 
            type="submit" 
            size="lg" 
            className="w-full sm:w-auto px-8"
            disabled={analyzeMutation.isPending}
          >
            {analyzeMutation.isPending ? (
              <>
                <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin mr-2" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 mr-2" />
                Analyze Match
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}
