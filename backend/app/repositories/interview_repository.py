from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)

class InterviewRepository:
    def __init__(self):
        self.db = get_db()
        
    def create_interview(self, analysis_id: str, user_id: str, overall_score: int, feedback_summary: str):
        """Creates a new interview record."""
        try:
            payload = {
                "analysis_id": analysis_id,
                "user_id": user_id,
                "overall_score": overall_score,
                "feedback_summary": feedback_summary
            }
            response = self.db.table("interviews").insert(payload).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating interview: {str(e)}")
            raise e
            
    def save_questions(self, interview_id: str, questions: list):
        """Saves generated questions to the interview_questions table."""
        try:
            payloads = []
            for q in questions:
                payloads.append({
                    "interview_id": interview_id,
                    "question_text": q.get("question", ""),
                    "focus_area": q.get("focus_area", ""),
                    "question_type": q.get("question_type", ""),
                    "user_answer": q.get("user_answer", ""),
                    "score": q.get("score", 0),
                    "feedback": q.get("feedback", "")
                })
            if payloads:
                response = self.db.table("interview_questions").insert(payloads).execute()
                return response.data
            return []
        except Exception as e:
            logger.error(f"Error saving questions: {str(e)}")
            raise e
            
    def get_interview(self, interview_id: str):
        """Retrieves an interview and its questions."""
        try:
            # We can run two queries or rely on Supabase joins.
            interview_res = self.db.table("interviews").select("*").eq("id", interview_id).execute()
            if not interview_res.data:
                return None
            
            interview = interview_res.data[0]
            questions_res = self.db.table("interview_questions").select("*").eq("interview_id", interview_id).execute()
            interview["questions"] = questions_res.data
            return interview
        except Exception as e:
            logger.error(f"Error getting interview {interview_id}: {str(e)}")
            raise e
