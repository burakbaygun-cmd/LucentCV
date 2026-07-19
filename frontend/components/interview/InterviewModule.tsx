"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Send, Target, Zap, AlertCircle } from "lucide-react";
import { api } from "@/services/api";
import { QuestionItem } from "@/types/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CircularScore } from "@/components/ui/circular-score";
import { toast } from "sonner";
import { Skeleton } from "@/components/ui/skeleton";

interface InterviewModuleProps {
  analysisId: string;
}

export function InterviewModule({ analysisId }: InterviewModuleProps) {
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [evaluation, setEvaluation] = useState<any>(null);

  const generateMutation = useMutation({
    mutationFn: () => api.generateQuestions(analysisId),
    onSuccess: (data) => {
      setQuestions(data.questions);
    },
    onError: () => {
      toast.error("Failed to generate questions");
    },
  });

  const evaluateMutation = useMutation({
    mutationFn: () => api.evaluateInterview({
      analysis_id: analysisId,
      user_id: "guest",
      questions,
      answers,
    }),
    onSuccess: (data) => {
      setEvaluation(data);
      toast.success("Interview evaluated!");
    },
    onError: () => {
      toast.error("Failed to evaluate interview");
    },
  });

  if (generateMutation.isPending) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-12 w-full" />
        <Skeleton className="h-[200px] w-full" />
        <Skeleton className="h-[200px] w-full" />
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center border border-dashed rounded-xl bg-muted/20">
        <Target className="w-12 h-12 text-muted-foreground mb-4" />
        <h3 className="text-xl font-semibold mb-2">Practice for the Interview</h3>
        <p className="text-muted-foreground mb-6 max-w-md">
          Generate personalized interview questions based on your CV and the job description to practice your answers.
        </p>
        <Button size="lg" onClick={() => generateMutation.mutate()}>
          Generate Questions
        </Button>
      </div>
    );
  }

  if (evaluation) {
    return (
      <div className="space-y-8 animate-in fade-in duration-700">
        <div className="flex flex-col items-center justify-center bg-card rounded-xl p-8 border shadow-xl">
          <CircularScore score={evaluation.overall_score} size={150} strokeWidth={12} />
          <h2 className="text-2xl font-bold mt-4">Interview Performance</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="border-success/20 bg-success/5">
            <CardHeader>
              <CardTitle className="text-success flex items-center">
                <Zap className="w-5 h-5 mr-2" /> Strengths
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5 space-y-2 text-sm">
                {evaluation.strengths.map((s: string, i: number) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="border-destructive/20 bg-destructive/5">
            <CardHeader>
              <CardTitle className="text-destructive flex items-center">
                <AlertCircle className="w-5 h-5 mr-2" /> Areas to Improve
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5 space-y-2 text-sm">
                {evaluation.areas_to_improve.map((a: string, i: number) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>

        <h3 className="text-xl font-bold pt-4">Question Breakdown</h3>
        <div className="space-y-6">
          {evaluation.per_question_feedback.map((fb: any, index: number) => {
            const q = questions.find((q) => q.id === fb.question_id);
            return (
              <Card key={fb.question_id} className="glass-card">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <Badge variant="outline" className="mb-2">Question {index + 1}</Badge>
                    <Badge variant={fb.score >= 70 ? "default" : "destructive"}>
                      Score: {fb.score}/100
                    </Badge>
                  </div>
                  <CardTitle className="text-lg">{q?.question}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4 text-sm">
                  <div className="p-4 rounded-lg bg-muted/50 border">
                    <span className="font-semibold block mb-1">Your Answer:</span>
                    {answers[fb.question_id.toString()] || "No answer provided"}
                  </div>
                  <div className="p-4 rounded-lg bg-primary/10 border border-primary/20 text-foreground">
                    <span className="font-semibold block mb-1 text-primary">Feedback:</span>
                    {fb.feedback}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-bold">Answer these {questions.length} questions</h3>
      </div>
      
      <div className="space-y-6">
        {questions.map((q, index) => (
          <Card key={q.id} className="glass-card">
            <CardHeader>
              <div className="flex justify-between">
                <Badge variant="secondary" className="mb-2">Question {index + 1}</Badge>
                {['guclu_nokta', 'gucli_nokta'].includes(q.question_type) ? (
                  <Badge variant="default" className="bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20 border-emerald-500/20">Güçlü Nokta</Badge>
                ) : q.question_type === 'eksik_beceri' ? (
                  <Badge variant="destructive" className="bg-destructive/10 text-destructive hover:bg-destructive/20 border-destructive/20">Eksik Beceri</Badge>
                ) : (
                  <Badge variant="outline" className="capitalize">{q.question_type?.replace('_', ' ')}</Badge>
                )}
              </div>
              <CardTitle className="text-lg leading-relaxed">{q.question}</CardTitle>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Type your answer here..."
                className="min-h-[150px] bg-background/50 focus-visible:ring-primary"
                value={answers[q.id.toString()] || ""}
                onChange={(e) => setAnswers({ ...answers, [q.id.toString()]: e.target.value })}
                disabled={evaluateMutation.isPending}
              />
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="flex justify-end pt-4">
        <Button 
          size="lg" 
          onClick={() => evaluateMutation.mutate()}
          disabled={evaluateMutation.isPending || Object.keys(answers).length === 0}
        >
          {evaluateMutation.isPending ? (
            "Evaluating..."
          ) : (
            <>
              Submit Answers <Send className="ml-2 w-4 h-4" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
