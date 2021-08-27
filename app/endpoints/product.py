from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import product as schemas
from app.services import product as services
from . import api, get_db


@api.get("/products/full", response_model=List[schemas.ProductFull], tags=["product"])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = services.get_products(db, skip=skip, limit=limit)
    return products


@api.get("/products/", response_model=List[schemas.Product], tags=["product"])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = services.get_products(db, skip=skip, limit=limit)
    return products


@api.get("/products/{product_id}", response_model=schemas.Product, tags=["product"])
def get_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = services.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@api.post("/products/", response_model=schemas.Product, tags=["product"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return services.create_product(db=db, product=product)


@api.put("/products/details", response_model=schemas.ProductFull, tags=["product"])
def update_details_of_product(detail: schemas.ProductDetail, db: Session = Depends(get_db)):
    return services.add_details(db=db, detail=detail)


@api.delete("/products/{product_id}", status_code=status.HTTP_200_OK, tags=["product"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return services.inactivated_product(product_id, db)
