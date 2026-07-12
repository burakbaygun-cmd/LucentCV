from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)

class AnalysisRepository:
    def __init__(self):
        self.db = get_db()
        
    def create_analysis(self, user_id: str, data: dict):
        """Creates a new analysis record in Supabase."""
        try:
            # We first ensure a profile exists (for MVP testing purposes if auth is skipped)
            # In production, profiles are created via Supabase Auth triggers.
            try:
                self.db.table("profiles").insert({"id": user_id, "full_name": "Test User"}).execute()
            except Exception:
                pass # Profile likely already exists
                
            payload = {
                "user_id": user_id,
                "cv_text": data.get("cv_text", ""),
                "job_text": data.get("job_text", ""),
                "match_score": data.get("match_score", 0),
                "strengths": data.get("strengths", []),
                "missing_skills": data.get("missing_skills", []),
                "recommendations": data.get("recommendations", []),
                "summary": data.get("summary", ""),
                "report": data.get("report", "")
            }
            response = self.db.table("analyses").insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating analysis: {str(e)}")
            raise e
        
    def get_analysis(self, analysis_id: str):
        """Retrieves an analysis by ID."""
        try:
            response = self.db.table("analyses").select("*").eq("id", analysis_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting analysis {analysis_id}: {str(e)}")
            raise e
        
    def get_user_history(self, user_id: str):
        """Retrieves all analyses for a user."""
        try:
            response = self.db.table("analyses").select("id, match_score, summary, created_at").eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting history for user {user_id}: {str(e)}")
            raise e

    def delete_analysis(self, analysis_id: str):
        """Deletes an analysis record."""
        try:
            response = self.db.table("analyses").delete().eq("id", analysis_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
            raise e
