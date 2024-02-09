from typing import List

from fastapi import APIRouter, Depends, status
# from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from merchandising.models import Batch
from merchandising.schemas import BatchCreate, BatchRead


router_batches = APIRouter(
    tags=['batches'],
    prefix='/batches',
)


@router_batches.get('/', response_model=List[BatchRead])
def get_batches(db: Session = Depends(get_db)): 
    return db.query(Batch).all()


@router_batches.get('/{id}/', response_model=BatchRead)
def get_batch(id: int, db: Session = Depends(get_db)):
    return db.query(Batch).get(id)


@router_batches.post('/', status_code=status.HTTP_201_CREATED)
def create_batch(batches: List[BatchCreate], db: Session = Depends(get_db)):
    for batch in batches:
        batch = Batch(**batch.dict())
        db.add(batch)
    db.commit()
    return batches