from datetime import date, datetime
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Batch, Product
from app.schemas import (
    Aggregation, BatchCreate, BatchRead, BatchUpdate, ProductCreate,
    ProductRead
)


router_batches = APIRouter(
    tags=['batches'],
    prefix='/batches',
)


@router_batches.get('/', response_model=List[BatchRead])
def get_batches(
    db: Session = Depends(get_db),
    status: bool = None,
    line: str = None,
    shift: str = None,
    assignment: str = Query(None, min_length=1, max_length=255),
    date: Optional[Union[date, str]] = Query(None),
    number: int = Query(None, gt=0),
    limit: int = Query(10, gt=0, le=1000),
    offset: int = Query(0, ge=0)
    ): 
    query = db.query(Batch)
    if status is not None:
        query = query.filter(Batch.status == status)
    if line is not None:
        query = query.filter(Batch.line == line)
    if shift is not None:
        query = query.filter(Batch.shift == shift)
    if assignment:
        query = query.filter(Batch.assignment.ilike(f"%{assignment}%"))
    if date:
        query = query.filter(Batch.date == date)
    if number:
        query = query.filter(Batch.number == number)
    query = query.offset(offset).limit(limit)
    return query.all()


@router_batches.get('/{id}/', response_model=BatchRead)
def get_batch(id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).get(id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch doesn't exists")
    return batch


@router_batches.post('/', status_code=status.HTTP_201_CREATED)
def create_batch(batches: List[BatchCreate], db: Session = Depends(get_db)):
    for batch in batches:
        date = batch.date
        number = batch.number
        existing_batches = db.query(Batch).filter(
            Batch.date == date,
            Batch.number == number
        ).all()
        for existing_batch in existing_batches:
            db.delete(existing_batch)
        new_batch = Batch(**batch.dict())
        db.add(new_batch)
    db.commit()
    return batches


@router_batches.patch(
    '/{id}/',
    status_code=status.HTTP_200_OK,
    response_model=BatchRead
)
def update_batch(id: int, request: BatchUpdate, db: Session = Depends(get_db)):
    batch = db.query(Batch).get(id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch doesn't exists")
    update_data = request.dict(exclude_unset=True)
    if 'status' in update_data and update_data['status'] != batch.status:
        if update_data['status']:
            batch.closed_at = datetime.now()
        else:
            batch.closed_at = None
    for field, value in update_data.items():
        setattr(batch, field, value)
    db.commit()
    db.refresh(batch)
    return batch


router_products = APIRouter(
    tags=['products'],
    prefix='/products',
)


@router_products.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=List[ProductRead]
)
def create_product(
    products: List[ProductCreate],
    db: Session = Depends(get_db)
):
    added_products = []
    try:
        for product in products:
            batch = db.query(Batch).filter(
                Batch.date == product.date,
                Batch.number == product.batch_number
            ).first()
            if batch:
                new_product = Product(
                    **product.dict(exclude={'batch'}),
                    batch_id=batch.id
                )
                added_products.append(new_product)
                db.add(new_product)
        db.commit()
        return added_products
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="The request body is incorrect. Please check the product code"
        )


@router_products.patch("/", status_code=200, response_model=ProductRead)
def aggregate_product(aggregation: Aggregation, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.code == aggregation.code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if product.is_aggregated:
        aggregated_at = product.aggregated_at.strftime("%Y-%m-%d %H:%M:%S")
        raise HTTPException(
            status_code=400,
            detail=f"Unique code already used at {aggregated_at}"
        )
    if product.batch_id != aggregation.id:
        raise HTTPException(
            status_code=400,
            detail="Unique code is attached to another batch"
        )
    product.is_aggregated = True
    product.aggregated_at = datetime.now()
    db.commit()
    return product
