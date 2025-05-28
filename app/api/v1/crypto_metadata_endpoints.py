from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.db.session import SessionLocal
from app.services.crypto_metadata_service import CryptoMetadataService
from app.models.metadata_models import CryptoMetadata
from pydantic import BaseModel, Field


# --------------------------
# DB Dependency
# --------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Pydantic Schemas
# --------------------------

class CryptoMetadataCreate(BaseModel):
    crypto_name: str
    crypto_symbol: str = Field(..., max_length=10)
    market_cap_rank: int | None = None
    circulating_supply: int | None = None
    max_supply: int | None = None
    listed_exchange: str
    notes: str | None = None

    # ✅ NEW FIELDS
    trend_info: str | None = None
    recent_headline: str | None = None


class CryptoMetadataOut(CryptoMetadataCreate):
    crypto_metadata_id: UUID

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }


# --------------------------
# FastAPI Router
# --------------------------
router = APIRouter(
    prefix="/api/v1/crypto-metadata",
    tags=["CryptoMetadata"]
)


# --------------------------
# CRUD Endpoints
# --------------------------

@router.post("/", response_model=CryptoMetadataOut, status_code=status.HTTP_201_CREATED)
def create_crypto_metadata(payload: CryptoMetadataCreate, db: Session = Depends(get_db)):
    return CryptoMetadataService.create_crypto_metadata(db, payload.dict())


@router.get("/", response_model=List[CryptoMetadataOut])
def list_crypto_metadata(db: Session = Depends(get_db)):
    return CryptoMetadataService.get_all_crypto_metadata(db)


@router.get("/{metadata_id}", response_model=CryptoMetadataOut)
def get_crypto_metadata(metadata_id: UUID, db: Session = Depends(get_db)):
    metadata = CryptoMetadataService.get_crypto_metadata_by_id(db, metadata_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return metadata


@router.put("/{metadata_id}", response_model=CryptoMetadataOut)
def update_crypto_metadata(metadata_id: UUID, payload: CryptoMetadataCreate, db: Session = Depends(get_db)):
    updated = CryptoMetadataService.update_crypto_metadata(db, metadata_id, payload.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return updated


@router.delete("/{metadata_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crypto_metadata(metadata_id: UUID, db: Session = Depends(get_db)):
    deleted = CryptoMetadataService.delete_crypto_metadata(db, metadata_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return None
