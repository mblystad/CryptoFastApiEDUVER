from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess

from app.core.logging_config import logger
from app.api.v1 import crypto_metadata_endpoints
from app.db.session import SessionLocal
from app.models.metadata_models import CryptoMetadata

# --------------------------------------
# Instantiate FastAPI application
# --------------------------------------
app = FastAPI(
    title="Crypto Metadata API",
    description="An API and dashboard for managing cryptocurrency metadata",
    version="1.0.0"
)

# --------------------------------------
# API Router
# --------------------------------------
app.include_router(crypto_metadata_endpoints.router)

# --------------------------------------
# Static files and Templates (for frontend)
# --------------------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --------------------------------------
# Web UI route (dashboard)
# --------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    coins = db.query(CryptoMetadata).order_by(CryptoMetadata.market_cap_rank).all()
    return templates.TemplateResponse("index.html", {"request": request, "coins": coins})

# --------------------------------------
# Refresh data endpoint (calls fetch script)
# --------------------------------------
@app.post("/refresh")
def refresh():
    subprocess.run(["python", "app/scripts/fetch_and_post_metadata.py"])
    return {"status": "ok"}

# --------------------------------------
# Optional API Health check route
# --------------------------------------
@app.get("/api/health", tags=["Health"])
def health():
    logger.info("Health check passed.")
    return {"status": "ok", "message": "Welcome to the Crypto Metadata API"}
