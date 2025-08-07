from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Position, Bucket
from app.api.schemas import PositionOut, BucketOut
from typing import List

router = APIRouter()


@router.get("/positions", response_model=List[PositionOut])
def get_all_positions(db: Session = Depends(get_db)):
    return db.query(Position).all()


@router.get("/buckets", response_model=List[BucketOut])
def get_all_buckets(db: Session = Depends(get_db)):
    return db.query(Bucket).all()
