from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from common.config import settings
from common.dependencies import verify_api_key
from agents.planning.router import router as planning_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models, establish connections
    logger.info("Starting up Hybrid Toolbox Agents API")
    yield
    # Shutdown: Clean up resources
    logger.info("Shutting down Hybrid Toolbox Agents API")

app = FastAPI(
    title="Hybrid Toolbox Agents API",
    description="Multi-agent system for hybrid training plan generation",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# API version prefix
api_v1 = FastAPI(
    title="Hybrid Toolbox Agents API v1",
    dependencies=[Depends(verify_api_key)]
)

# Register the planning agent router with simplified MVP endpoints
api_v1.include_router(planning_router, prefix="/planning", tags=["Planning Agent"])

# Mount the v1 API under /v1 prefix
app.mount("/v1", api_v1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
