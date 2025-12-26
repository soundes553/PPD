from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EPDSAnswer(Base):
    __tablename__ = "epds_answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.assessment_id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    answer_value = Column(Integer, nullable=False)

    assessment = relationship("Assessment", back_populates="answers")
