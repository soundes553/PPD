from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Ajouter CORS
from app.routers.user_router import router as user_router
from app.routers.epds_router import router as epds_router
from app.routers import assessment_router
from app.routers.ml_router import router as ml_router
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Créer les tables dans la BD
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PPD Backend",
    description="API pour calcul PPD + gestion utilisateurs",
    version="1.0"
)

# ----------------------
# CORS : autoriser le front
# ----------------------
origins = [
    "*",  # remplacer par le port de ton front si différent
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Routers
# ----------------------
app.include_router(user_router)
app.include_router(epds_router)
app.include_router(assessment_router.router)
app.include_router(ml_router)

# Route racine pour tester le backend
@app.get("/")
def root():
    return {"message": "Backend PPD fonctionne !"}  