from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, projects, recordings, bookings, files, requests

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blink Customers Platform",
    description="Portal do Cliente para Consultoria e Projetos",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(recordings.router)
app.include_router(bookings.router)
app.include_router(files.router)
app.include_router(requests.router)


@app.get("/")
def root():
    return {
        "message": "Blink Customers Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
