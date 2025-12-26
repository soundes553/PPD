from sqlalchemy import Column, Integer, String
from app.core.database import Base

class EPDSRecommendation(Base):
    __tablename__ = "epds_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)      # minimal, mild, moderate
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    emergency_advice = Column(String, nullable=False)
