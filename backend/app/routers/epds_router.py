from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.epds import EPDSQuestion
from app.schemas.epds import QuestionResponse

router = APIRouter(prefix="/questions", tags=["EPDS"])

@router.get("/", response_model=list[QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    questions = db.query(EPDSQuestion).all()
    return questions

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(EPDSQuestion).filter(EPDSQuestion.question_id == question_id).first()
    return question
