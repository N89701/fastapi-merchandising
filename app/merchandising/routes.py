from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
# from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from merchandising.models import Batch
from merchandising.schemas import BatchCreate, BatchRead, BatchUpdate


router_batches = APIRouter(
    tags=['batches'],
    prefix='/batches',
)


@router_batches.get('/', response_model=List[BatchRead])
def get_batches(db: Session = Depends(get_db)): 
    return db.query(Batch).all()


@router_batches.get('/{id}/', response_model=BatchRead)
def get_batch(id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).get(id)
    if batch is None:
        raise HTTPException(status_code=404, detail="This batch doesn't exists")
    return batch


@router_batches.post('/', status_code=status.HTTP_201_CREATED)
def create_batch(batches: List[BatchCreate], db: Session = Depends(get_db)):
    for batch in batches:
        batch = Batch(**batch.dict())
        db.add(batch)
    db.commit()
    return batches


@router_batches.patch('/{id}/', status_code=status.HTTP_200_OK)
def update_batch(id: int, request: BatchUpdate, db: Session = Depends(get_db)):
    batch = db.query(Batch).get(id)
    if batch is None:
        raise HTTPException(status_code=400, detail="This batch doesn't exists")
    update_date = request.dict(exclude_unset=True)
    for field, value in update_date.items():
        setattr(batch, field, value)
    db.commit()
    db.refresh(batch)
    return batch
