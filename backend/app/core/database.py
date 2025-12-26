from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------
# 1. CONFIGURATION DE LA CONNEXION A POSTGRESQL
# --------------------------------------------------

DATABASE_URL = "postgresql://postgres:douaa.16@localhost:5432/postpartum_bdd"

# create_engine → crée la connexion
engine = create_engine(DATABASE_URL, echo=True)

# sessionmaker → pour créer des sessions (interaction DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base → classe mère des modèles SQLAlchemy
Base = declarative_base()

# --------------------------------------------------
# 2. FONCTION POUR OBTENIR UNE SESSION
# --------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
