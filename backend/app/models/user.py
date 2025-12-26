from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    country = Column(String(100))
    delivery_type = Column(String(20))
    education_level = Column(String(100))
    income_level = Column(String(100))
    partner_support_level = Column(Integer)
    family_support_level = Column(Integer)
    total_support_score = Column(Integer)
    recent_birth = Column(Boolean)
