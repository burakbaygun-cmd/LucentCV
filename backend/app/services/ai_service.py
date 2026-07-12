from typing import Dict, Any
from app.agents import (
    cv_agent,
    job_agent,
    matcher_agent,
    interview_generator,
    interview_evaluator,
    summary_agent,
    report_agent
)
from app.agents.base import get_client
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.interview_repository import InterviewRepository
from app.core.logging import logger

class AIService:
    def __init__(self):
        self.client = get_client()
        self.analysis_repo = AnalysisRepository()
        self.interview_repo = InterviewRepository()

    def run_full_analysis(self, cv_text: str, job_text: str, user_id: str = "default-user-id") -> Dict[str, Any]:
        """
        Orchestrates the entire CV/Job analysis pipeline using 4 specialized agents,
        and saves the result to Supabase.
        """
        logger.info(f"Starting full analysis for user {user_id}")
        
        cv_result = cv_agent.run(self.client, cv_text)
        logger.info("CV analysis completed")
        
        job_result = job_agent.run(self.client, job_text)
        logger.info("Job analysis completed")
        
        match_result = matcher_agent.run(self.client, cv_result, job_result)
        logger.info("Match analysis completed")
        
        summary_result = summary_agent.run(self.client, cv_result, job_result, match_result)
        logger.info("Summary generated")
        
        full_data = {
            "cv_analysis": cv_result,
            "job_analysis": job_result,
            "match_result": match_result,
            "summary": summary_result.get("summary", ""),
            "match_score": match_result.get("match_score", 0)
        }
        
        report_result = report_agent.run(self.client, full_data)
        logger.info("Markdown report generated")
        full_data["report"] = report_result.get("markdown_report", "")

        # Save to database
        db_payload = {
            "cv_text": cv_text,
            "job_text": job_text,
            "match_score": match_result.get("match_score", 0),
            "strengths": match_result.get("matching_skills", []),
            "missing_skills": match_result.get("missing_skills", []),
            "recommendations": match_result.get("recommendations", []),
            "summary": full_data["summary"],
            "report": full_data["report"]
        }
        saved_record = self.analysis_repo.create_analysis(user_id, db_payload)
        logger.info(f"Analysis saved to db with id: {saved_record.get('id') if saved_record else 'unknown'}")
        
        full_data["analysis_id"] = saved_record.get("id") if saved_record else None
        return full_data
        
    def generate_interview_questions(self, analysis_id: str) -> Dict[str, Any]:
        """
        Fetches an analysis from DB and generates tailored interview questions.
        """
        logger.info(f"Generating interview questions for analysis {analysis_id}")
        
        # 1. Fetch analysis details
        analysis = self.analysis_repo.get_analysis(analysis_id)
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")
            
        cv_analysis = {
            "strengths": analysis.get("strengths", []),
            "missing_skills": analysis.get("missing_skills", [])
        }
        
        # 2. Call generator agent
        result = interview_generator.run(
            self.client, 
            cv_analysis=cv_analysis, 
            job_analysis={"job_text": analysis.get("job_text", "")}, 
            match_result={"match_score": analysis.get("match_score", 0)}
        )
        
        logger.info("Interview questions generated")
        return result
        
    def evaluate_interview(self, analysis_id: str, user_id: str, questions: list, answers: dict) -> Dict[str, Any]:
        """
        Evaluates the user's interview answers, generates feedback, 
        and saves everything to the database.
        """
        logger.info(f"Evaluating interview for analysis {analysis_id}")
        
        eval_result = interview_evaluator.run(self.client, questions, answers)
        
        overall_score = eval_result.get("overall_score", 0)
        strengths_str = ", ".join(eval_result.get("strengths", []))
        areas_str = ", ".join(eval_result.get("areas_to_improve", []))
        feedback_summary = f"Strengths: {strengths_str}\nAreas to Improve: {areas_str}"
        
        # Save interview record
        interview_record = self.interview_repo.create_interview(
            analysis_id=analysis_id,
            user_id=user_id,
            overall_score=overall_score,
            feedback_summary=feedback_summary
        )
        
        if interview_record:
            interview_id = interview_record.get("id")
            
            # Combine questions and answers and feedback to save
            q_feedbacks = {str(item.get("question_id")): item for item in eval_result.get("per_question_feedback", [])}
            
            questions_to_save = []
            for q in questions:
                qid = str(q.get("id"))
                feedback_info = q_feedbacks.get(qid, {})
                questions_to_save.append({
                    "question": q.get("question", ""),
                    "focus_area": q.get("focus_area", ""),
                    "question_type": q.get("question_type", ""),
                    "user_answer": answers.get(qid, ""),
                    "score": feedback_info.get("score", 0),
                    "feedback": feedback_info.get("feedback", "")
                })
                
            self.interview_repo.save_questions(interview_id, questions_to_save)
            logger.info(f"Interview {interview_id} and questions saved.")
            
        return eval_result
