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

class AIController:
    def __init__(self):
        self.client = get_client()

    def run_full_analysis(self, cv_text: str, job_text: str) -> dict:
        """Runs the 4 agents sequentially to produce the full CV-Job match result + summary."""
        cv_result = cv_agent.run(self.client, cv_text)
        job_result = job_agent.run(self.client, job_text)
        match_result = matcher_agent.run(self.client, cv_result, job_result)
        summary_result = summary_agent.run(self.client, cv_result, job_result, match_result)
        
        full_data = {
            "cv_analysis": cv_result,
            "job_analysis": job_result,
            "match_result": match_result,
            "summary": summary_result
        }
        
        # Optionally generate a report immediately (or we can defer to an endpoint)
        report_result = report_agent.run(self.client, full_data)
        full_data["report"] = report_result.get("markdown_report", "")

        return full_data
        
    def generate_interview_questions(self, cv_analysis: dict, job_analysis: dict, match_result: dict) -> dict:
        """Generates tailored interview questions based on prior analysis."""
        return interview_generator.run(self.client, cv_analysis, job_analysis, match_result)
        
    def evaluate_interview(self, questions: list, answers: dict) -> dict:
        """Evaluates interview answers and generates feedback."""
        return interview_evaluator.run(self.client, questions, answers)
