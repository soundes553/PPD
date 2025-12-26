from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EPDSQuestion(Base):
    __tablename__ = "epds_questions"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)

    options = relationship("EPDSOption", back_populates="question")


class EPDSOption(Base):
    __tablename__ = "epds_options"

    option_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("epds_questions.question_id"))
    option_text = Column(String, nullable=False)
    answer_value = Column(Integer)
    option_order = Column(Integer)

    question = relationship("EPDSQuestion", back_populates="options")
