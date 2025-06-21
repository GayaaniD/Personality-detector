import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import router as personality_router
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personality Prediction API",
    description="Predicts personality type from behavioral data",
    version="1.0.0",
    swagger_ui_parameters={"displayRequestDuration": True},
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Health check and root
@app.get("/")
async def root():
    return {"message": "Personality API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routes
app.include_router(personality_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
