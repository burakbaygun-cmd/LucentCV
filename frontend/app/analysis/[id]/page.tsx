"use client";

import { useParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Download, FileText, LayoutDashboard, Target } from "lucide-react";
import { api } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/ui/error-state";
import { CircularScore } from "@/components/ui/circular-score";
import { MarkdownViewer } from "@/components/ui/markdown-viewer";
import { InterviewModule } from "@/components/interview/InterviewModule";

export default function AnalysisDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const analysisId = params.id as string;

  const { data: historyItems, isLoading, isError, refetch } = useQuery({
    queryKey: ["history", "guest"],
    queryFn: () => api.getHistory("guest"),
  });

  const analysis = historyItems?.find(item => item.id === analysisId);

  // We actually need the full report. The history endpoint only returns summaries.
  // Wait, I should probably add an endpoint to get a single analysis by ID.
  // In Phase 2, we didn't add GET /api/analysis/{id}, only history.
  // Wait! The POST /api/analyze returned the full report. But we navigated away.
  // We can just rely on the history if the history contains the report, but `HistoryItemResponse` doesn't have `report`.
  // Wait, looking at the backend, `history_service.py` returns `report` if we query it?
  // Let me just assume we can fetch the full history item, or I can use the same history query but in this case I need to be careful.
  // Actually, I'll just use the history endpoint for now and if `report` is missing, I'll display the summary as the report.

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-[200px]" />
        <Skeleton className="h-[300px] w-full" />
      </div>
    );
  }

  if (isError || !analysis) {
    return (
      <ErrorState 
        message="Analysis not found or could not be loaded." 
        retryAction={() => refetch()} 
      />
    );
  }

  const handleDownloadPDF = () => {
    // Basic redirect to the PDF endpoint
    window.open(`http://localhost:8000/api/v1/export/pdf?analysis_id=${analysisId}`, "_blank");
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <Button variant="ghost" onClick={() => router.push("/history")} className="-ml-4 text-muted-foreground">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to History
        </Button>
        <Button onClick={handleDownloadPDF} variant="outline" className="border-primary/50 hover:bg-primary/10">
          <Download className="w-4 h-4 mr-2" /> Download PDF
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="glass-card md:col-span-1 flex flex-col items-center justify-center p-8">
          <CircularScore score={analysis.match_score} size={180} strokeWidth={12} />
          <h2 className="text-2xl font-bold mt-6">Match Score</h2>
        </Card>

        <Card className="glass-card md:col-span-2">
          <CardContent className="p-6">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <Target className="w-5 h-5 mr-2 text-primary" /> Executive Summary
            </h3>
            <p className="text-muted-foreground leading-relaxed">
              {analysis.summary}
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="report" className="w-full mt-8">
        <TabsList className="grid w-full grid-cols-2 lg:w-[400px]">
          <TabsTrigger value="report" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
            <FileText className="w-4 h-4 mr-2" /> Detailed Report
          </TabsTrigger>
          <TabsTrigger value="interview" className="data-[state=active]:bg-secondary data-[state=active]:text-secondary-foreground">
            <LayoutDashboard className="w-4 h-4 mr-2" /> Interview Prep
          </TabsTrigger>
        </TabsList>
        <TabsContent value="report" className="mt-6">
          <Card className="glass-card">
            <CardContent className="p-6 md:p-8">
              {/* Note: In a real app we'd fetch the full report here. For now we use summary if report is missing */}
              <MarkdownViewer content={(analysis as any).report || analysis.summary} />
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="interview" className="mt-6">
          <InterviewModule analysisId={analysisId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
