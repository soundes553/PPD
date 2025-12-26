from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.assessment import AssessmentCreate, AssessmentResponse
from app.models.assessment import Assessment
from app.models.epds_answer import EPDSAnswer
from app.models.epds_recommendation import EPDSRecommendation

router = APIRouter(prefix="/assessments", tags=["Assessments"])


# -----------------------------
# 1. DB SESSION
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# 2. SCORE → LEVEL
# -----------------------------
def calculate_level(score: int) -> str:
    if score <= 9:
        return "minimal"
    elif score <= 12:
        return "mild"
    else:
        return "higher_risk"


# -----------------------------
# 3. CREATE ASSESSMENT
# -----------------------------
@router.post("/", response_model=AssessmentResponse)
def create_assessment(data: AssessmentCreate, db: Session = Depends(get_db)):

    # --- Calculate EPDS Score ---
    total_score = sum([a.answer_value for a in data.answers])
    level = calculate_level(total_score)

    # --- Insert assessment record ---
    new_assessment = Assessment(
        user_id=data.user_id,
        total_epds_score=total_score,
        depression_level=level,
    )
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    # --- Insert each EPDS answer ---
    for ans in data.answers:
        answer = EPDSAnswer(
            assessment_id=new_assessment.assessment_id,
            question_id=ans.question_id,
            answer_value=ans.answer_value
        )
        db.add(answer)

    db.commit()

    # -----------------------------
    # 4. SELECT RECOMMENDATION BASED ON LEVEL
    # -----------------------------
    reco = db.query(EPDSRecommendation).filter(
        EPDSRecommendation.level == level
    ).first()

    return AssessmentResponse(
        assessment_id=new_assessment.assessment_id,
        total_epds_score=total_score,
        depression_level=level,
        recommendation_title=reco.title if reco else None,
        recommendation_message=reco.message if reco else None,
        emergency_advice=reco.emergency_advice if reco else None,
    )
