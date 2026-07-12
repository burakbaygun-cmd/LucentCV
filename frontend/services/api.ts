import axios from "axios";
import {
  AnalyzeRequest,
  AnalyzeResponse,
  GenerateQuestionsResponse,
  EvaluateInterviewRequest,
  EvaluateInterviewResponse,
  HistoryItemResponse,
} from "../types/api";

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const api = {
  analyze: async (data: AnalyzeRequest): Promise<AnalyzeResponse> => {
    const response = await apiClient.post<AnalyzeResponse>("/analyze", data);
    return response.data;
  },

  generateQuestions: async (analysisId: string): Promise<GenerateQuestionsResponse> => {
    const response = await apiClient.post<GenerateQuestionsResponse>("/interview/questions", {
      analysis_id: analysisId,
    });
    return response.data;
  },

  evaluateInterview: async (data: EvaluateInterviewRequest): Promise<EvaluateInterviewResponse> => {
    const response = await apiClient.post<EvaluateInterviewResponse>("/interview/evaluate", data);
    return response.data;
  },

  getHistory: async (userId: string = "guest"): Promise<HistoryItemResponse[]> => {
    const response = await apiClient.get<HistoryItemResponse[]>("/history", {
      params: { user_id: userId },
    });
    return response.data;
  },

  deleteHistory: async (id: string): Promise<{ status: string; deleted_id: string }> => {
    const response = await apiClient.delete(`/history/${id}`);
    return response.data;
  },
};
