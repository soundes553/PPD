from pydantic import BaseModel
from typing import List

class AnswerItem(BaseModel):
    question_id: int
    answer_value: int

class AssessmentCreate(BaseModel):
    user_id: int
    answers: List[AnswerItem]

class AssessmentResponse(BaseModel):
    assessment_id: int
    total_epds_score: int
    depression_level: str
    recommendation_title: str
    recommendation_message: str
    emergency_advice: str
