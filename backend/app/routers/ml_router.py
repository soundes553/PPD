from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.ml.result import predict_ppd_risk
from app.core.security import encrypt_prediction, decrypt_prediction
from app.core.database import SessionLocal
from app.models.assessment import Assessment

router = APIRouter(prefix="/ml", tags=["ML Risk Prediction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/predict")
def predict_risk(data: dict, db: Session = Depends(get_db)):
    """
    Input JSON example :
    {
        "user_id": 1,
        "age": 28,
        "partner_support": 7,
        "sleep_quality": 3,
        "epds_10": 0,
        "total_epds_score": 12,
        "depression_level": "Moderate"
    }
    """
    # Get prediction
    result = predict_ppd_risk(data)
    
    # Encrypt the prediction result
    encrypted_result = encrypt_prediction(result)
    
    # Store in database with encrypted prediction
    new_assessment = Assessment(
        user_id=data.get("user_id"),
        total_epds_score=data.get("total_epds_score"),
        depression_level=data.get("depression_level"),
        encrypted_prediction=encrypted_result
    )
    
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)
    
    # Return the original (unencrypted) result to the user
    return {
        "assessment_id": new_assessment.assessment_id,
        "prediction": result
    }


@router.get("/assessment/{assessment_id}")
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve and decrypt a stored assessment
    """
    assessment = db.query(Assessment).filter(
        Assessment.assessment_id == assessment_id
    ).first()
    
    if not assessment:
        return {"error": "Assessment not found"}
    
    # Decrypt the prediction
    decrypted_prediction = decrypt_prediction(assessment.encrypted_prediction)
    
    return {
        "assessment_id": assessment.assessment_id,
        "user_id": assessment.user_id,
        "total_epds_score": assessment.total_epds_score,
        "depression_level": assessment.depression_level,
        "prediction": decrypted_prediction
    }