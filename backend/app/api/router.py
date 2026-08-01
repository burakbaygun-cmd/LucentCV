from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from typing import List

from app.schemas.analysis import (
    AnalyzeRequest, 
    AnalyzeResponse,
    GenerateQuestionsRequest,
    GenerateQuestionsResponse,
    EvaluateInterviewRequest,
    EvaluateInterviewResponse,
    HistoryItemResponse,
    DeleteHistoryResponse,
    ExportRequest,
    ExportMarkdownResponse
)
from app.services.ai_service import AIService
from app.services.export_service import ExportService
from app.repositories.analysis_repository import AnalysisRepository
from app.core.logging import logger

api_router = APIRouter()

# Dependency injection for services
def get_ai_service():
    return AIService()
    
def get_export_service():
    return ExportService()
    
def get_analysis_repo():
    return AnalysisRepository()

@api_router.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
def analyze_resume(request: AnalyzeRequest, ai_service: AIService = Depends(get_ai_service)):
    try:
        result = ai_service.run_full_analysis(
            cv_text=request.cv_text, 
            job_text=request.job_text,
            user_id=request.user_id
        )
        return AnalyzeResponse(**result)
    except Exception as e:
        logger.error(f"Failed to analyze resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/interview/questions", response_model=GenerateQuestionsResponse, tags=["Interview"])
def generate_questions(request: GenerateQuestionsRequest, ai_service: AIService = Depends(get_ai_service)):
    try:
        result = ai_service.generate_interview_questions(analysis_id=request.analysis_id)
        return GenerateQuestionsResponse(**result)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/interview/evaluate", response_model=EvaluateInterviewResponse, tags=["Interview"])
def evaluate_interview(request: EvaluateInterviewRequest, ai_service: AIService = Depends(get_ai_service)):
    try:
        result = ai_service.evaluate_interview(
            analysis_id=request.analysis_id,
            user_id=request.user_id,
            questions=request.questions,
            answers=request.answers
        )
        return EvaluateInterviewResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analysis/{id}", response_model=AnalyzeResponse, tags=["Analysis"])
def get_analysis_by_id(id: str, repo: AnalysisRepository = Depends(get_analysis_repo)):
    try:
        record = repo.get_analysis(id)
        if not record:
            raise HTTPException(status_code=404, detail=f"Analysis {id} not found")
        return AnalyzeResponse(
            analysis_id=record["id"],
            match_score=record.get("match_score", 0),
            summary=record.get("summary", ""),
            report=record.get("report", ""),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/history", response_model=List[HistoryItemResponse], tags=["History"])
def get_history(user_id: str = "default-user-id", repo: AnalysisRepository = Depends(get_analysis_repo)):
    try:
        records = repo.get_user_history(user_id)
        return [HistoryItemResponse(**r) for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/history/{id}", response_model=DeleteHistoryResponse, tags=["History"])
def delete_history(id: str, repo: AnalysisRepository = Depends(get_analysis_repo)):
    try:
        repo.delete_analysis(id)
        return DeleteHistoryResponse(status="success", deleted_id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/export/markdown", response_model=ExportMarkdownResponse, tags=["Export"])
def export_markdown(request: ExportRequest, export_service: ExportService = Depends(get_export_service)):
    try:
        markdown_text = export_service.generate_markdown(request.analysis_id)
        return ExportMarkdownResponse(markdown=markdown_text)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.api_route("/export/pdf", methods=["GET", "POST"], tags=["Export"])
def export_pdf(
    request: ExportRequest = None,
    analysis_id: str = None,
    export_service: ExportService = Depends(get_export_service)
):
    try:
        target_id = (request.analysis_id if request and hasattr(request, 'analysis_id') else None) or analysis_id
        if not target_id:
            raise HTTPException(status_code=400, detail="analysis_id query parameter or body is required")
        pdf_bytes = export_service.generate_pdf(target_id)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename=report_{target_id}.pdf"
        })
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Failed to export PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
