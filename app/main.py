from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, bot
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Bauliver Backend - Autonomous Bot System",
    description="Backend API for Bauliver OS with autonomous bot capabilities for construction, solar, and permit automation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(bot.router, prefix="/bot", tags=["Autonomous Bot"])


@app.get("/")
def root():
    """
    Root endpoint - returns API information
    """
    return {
        "name": "Bauliver Backend API",
        "version": "1.0.0",
        "description": "Autonomous bot system for construction and solar automation",
        "features": [
            "Autonomous permit processing",
            "Project automation",
            "Workflow execution",
            "Real-world building demonstrations"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "auth": "/auth",
            "bot": "/bot"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "bauliver-backend",
        "autonomous_bot": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
