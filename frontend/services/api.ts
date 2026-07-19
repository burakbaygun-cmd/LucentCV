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

  /**
   * Requests a PDF report from the backend and triggers a browser file download.
   *
   * Uses responseType "blob" so axios receives binary data instead of trying
   * to parse the PDF bytes as JSON. A temporary object URL is created for the
   * download anchor and immediately revoked afterward to prevent memory leaks.
   */
  exportPdf: async (analysisId: string): Promise<void> => {
    // POST with JSON body — backend expects { analysis_id } in the request body.
    const response = await apiClient.post(
      "/export/pdf",
      { analysis_id: analysisId },
      { responseType: "blob" }
    );

    // Wrap the raw binary response in a Blob with the correct MIME type.
    const blob = new Blob([response.data], { type: "application/pdf" });

    // Create a short-lived object URL to feed the anchor's href.
    const objectUrl = URL.createObjectURL(blob);

    // Programmatically click a hidden anchor to trigger the browser download dialog.
    const anchor = document.createElement("a");
    anchor.href = objectUrl;
    anchor.download = `lucent-cv-report-${analysisId}.pdf`;
    anchor.click();

    // Release the object URL immediately — the download is already queued by the browser.
    URL.revokeObjectURL(objectUrl);
  },
};
