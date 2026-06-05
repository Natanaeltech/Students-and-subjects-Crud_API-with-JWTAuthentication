from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from src.routes import subjects
from src.Models.base import Base
from src.routes import auth, subjects, etudiants

app = FastAPI(title="Etudiants and subject CRUD API with JWT", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(etudiants.router)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)