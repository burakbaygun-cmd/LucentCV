"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { Sparkles, FileText, Briefcase, Upload, Loader2, X, FileCheck2 } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/services/api";
import { useAuth } from "@/context/AuthContext";

const ACCEPTED_FILE_TYPES = ".pdf,.docx,.txt";
const ACCEPTED_EXTENSIONS = [".pdf", ".docx", ".txt"];

export default function Dashboard() {
  const router = useRouter();
  const { user } = useAuth();
  const [cvText, setCvText] = useState("");
  const [jobText, setJobText] = useState("");
  const [isUploadingCv, setIsUploadingCv] = useState(false);

  // When a CV file is uploaded, we keep the extracted text in `cvText` (used
  // for the actual analysis) but DON'T render it in the textarea — instead
  // we show a compact "file attached" indicator. `cvFileName` being non-null
  // is what switches the CV card into "attached file" mode.
  const [cvFileName, setCvFileName] = useState<string | null>(null);
  const [cvCharCount, setCvCharCount] = useState<number>(0);

  const cvFileInputRef = useRef<HTMLInputElement>(null);

  const handleCvFileSelected = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    // Reset the input value so selecting the same file again still fires onChange.
    e.target.value = "";
    if (!file) return;

    const extension = "." + file.name.split(".").pop()?.toLowerCase();
    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      toast.error("Please upload a .pdf, .docx, or .txt file.");
      return;
    }

    setIsUploadingCv(true);
    try {
      const result = await api.parseFile(file);
      setCvText(result.text);
      setCvFileName(result.filename);
      setCvCharCount(result.char_count);
      toast.success(`Extracted text from ${result.filename}`);
    } catch (error: unknown) {
      console.error(error);
      const message =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        "Could not extract text from the file. Please try pasting it manually.";
      toast.error(message);
    } finally {
      setIsUploadingCv(false);
    }
  };

  const handleRemoveCvFile = () => {
    setCvFileName(null);
    setCvCharCount(0);
    setCvText("");
  };

  const analyzeMutation = useMutation({
    mutationFn: () => api.analyze({ cv_text: cvText, job_text: jobText, user_id: user?.id || "guest" }),
    onSuccess: (data) => {
      toast.success("Analysis complete!");
      router.push(`/analysis/${data.analysis_id}`);
    },
    onError: (error: unknown) => {
      console.error(error);
      const message =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        "Failed to analyze. Please try again.";
      toast.error(message);
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
            <div className="flex items-start justify-between gap-2">
              <div>
                <CardTitle className="flex items-center text-xl">
                  <FileText className="w-5 h-5 mr-2 text-primary" />
                  Your CV
                </CardTitle>
                <CardDescription>Paste the plain text of your resume, or upload a file.</CardDescription>
              </div>
              <input
                ref={cvFileInputRef}
                type="file"
                accept={ACCEPTED_FILE_TYPES}
                className="hidden"
                onChange={handleCvFileSelected}
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => cvFileInputRef.current?.click()}
                disabled={isUploadingCv || analyzeMutation.isPending}
              >
                {isUploadingCv ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-1.5 animate-spin" />
                    Reading...
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4 mr-1.5" />
                    Upload PDF/DOCX
                  </>
                )}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex-1">
            {cvFileName ? (
              <div className="min-h-[400px] h-full rounded-lg border border-white/10 bg-background/50 flex flex-col items-center justify-center gap-3 p-6 text-center">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <FileCheck2 className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <p className="font-medium break-all">{cvFileName}</p>
                  <p className="text-sm text-muted-foreground mt-1">
                    {cvCharCount.toLocaleString()} characters extracted
                  </p>
                </div>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={handleRemoveCvFile}
                  disabled={analyzeMutation.isPending}
                >
                  <X className="w-4 h-4 mr-1.5" />
                  Remove file
                </Button>
              </div>
            ) : (
              <Textarea
                placeholder="John Doe&#10;Software Engineer&#10;&#10;Experience...&#10;Skills..."
                className="min-h-[400px] h-full resize-none bg-background/50 border-white/10 focus-visible:ring-primary"
                value={cvText}
                onChange={(e) => setCvText(e.target.value)}
                disabled={analyzeMutation.isPending || isUploadingCv}
              />
            )}
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
