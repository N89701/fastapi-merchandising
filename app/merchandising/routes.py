# from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from merchandising.models import Batch
from merchandising.schemas import BatchCreate


router_batches = APIRouter(
    tags=['batches'],
    prefix='/batches',
)

@router_batches.get('/', response_model=list[BatchCreate])
def get_notes(db: Session = Depends(get_db)):
    batches = db.query(Batch).all()
    return {'status': 'success', 'results': batches}