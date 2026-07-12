export interface AnalyzeRequest {
  cv_text: string;
  job_text: string;
  user_id?: string;
}

export interface AnalyzeResponse {
  analysis_id: string;
  match_score: number;
  summary: string;
  report: string;
}

export interface QuestionItem {
  id: number;
  question: string;
  focus_area: string;
  question_type: string;
}

export interface GenerateQuestionsResponse {
  questions: QuestionItem[];
}

export interface EvaluateInterviewRequest {
  analysis_id: string;
  user_id?: string;
  questions: QuestionItem[];
  answers: Record<string, string>;
}

export interface PerQuestionFeedback {
  question_id: number;
  score: number;
  feedback: string;
}

export interface EvaluateInterviewResponse {
  overall_score: number;
  per_question_feedback: PerQuestionFeedback[];
  strengths: string[];
  areas_to_improve: string[];
}

export interface HistoryItemResponse {
  id: string;
  match_score: number;
  summary: string;
  created_at: string;
}
