import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.webhooks.test import router as webhook_router
from src.utils.storage import init_db
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting SmarterOS Webhook Handler")
    init_db()
    yield
    logger.info("🛑 Shutting down")

app = FastAPI(
    title="SmarterOS Webhook Handler",
    description="Production-ready webhook handler with signature verification",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])

@app.get("/")
async def root():
    return {
        "service": "SmarterOS Webhook Handler",
        "version": "0.1.0",
        "status": "operational",
        "endpoints": {
            "webhooks": "/webhooks/test",
            "health": "/health",
            "docs": "/docs",
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "webhook-handler"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
