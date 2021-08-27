import logging as log
from typing import List

from fastapi import HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Product, ProductDetail
from app.schemas import product as SchemaProduct


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.active == 't').offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: SchemaProduct.ProductCreate):
    """
    Create a new product if name isn't already taken.

    :param db: SQLAlchemy database session.
    :type db: Session
    :param product: New product record to create.
    :type product: ProductCreate

    :return: Optional[ProductCreate]
    """
    try:
        existing_product = db.query(Product).filter(Product.name == product.name).first()
        if existing_product is None:
            db_product = Product(name=product.name, price=product.price, brand=product.brand, status=product.status)
            db.add(db_product)  # Add the product
            db.commit()  # Commit the change
            db.refresh(db_product)
            print(f"Created product: {product}")
            return db_product
        else:
            print(f"Product already exists in database: {existing_product}")
            raise HTTPException(status_code=400, detail="Product already exists in database")
    except IntegrityError as e:
        log.error(e)
        raise e
    except SQLAlchemyError as e:
        print(f"Unexpected error when creating product: {e}")
        raise HTTPException(status_code=500, detail="Unexpected Error")


def create_product_with_details(db: Session, product: SchemaProduct.ProductCreate):
    db_product = Product(name=product.name, price=product.price, brand=product.brand, status=product.status)
    new_product = create_product(db, db_product)
    product_details = product.details

    for detail in product_details:
        db_detail = ProductDetail(description=detail['description'], product_id=new_product.id)
        _create_details(db, db_detail)

    return get_product_by_id(db, new_product.id)


def add_details(db: Session, detail: ProductDetail):
    try:
        product_db = db.query(Product).filter(Product.id == detail.product_id).first()
        if product_db is None:
            print(f"Product not  exists in database: {product_db}")
            raise HTTPException(status_code=400, detail="Product not exists in database")
        else:
            for det in detail.details:
                db_detail = ProductDetail(description=det['description'], product_id=detail.product_id)
                product_db.details.append(db_detail)

            db.add(product_db)
            db.commit()
            db.refresh(product_db)
            print(f"Added details to product: {product_db}")
            return product_db

    except IntegrityError as e:
        print(f"Unexpected error when creating detail: {e}")
        raise HTTPException(status_code=500, detail="Unexpected Error")
    except SQLAlchemyError as e:
        print(f"Unexpected error when creating detail: {e}")
        raise HTTPException(status_code=500, detail="Unexpected Error")


# def add_details_to_product(db: Session, detail: ProductDetail):
#     try:
#         product_db = db.query(Product).filter(Product.id == detail.product_id).first()
#         if product_db is None:
#             print(f"Product not  exists in database: {product_db}")
#             raise HTTPException(status_code=400, detail="Product not exists in database")
#         else:
#             product_details = detail.details
#
#             for det in product_details:
#                 db_detail = ProductDetail(description=det['description'], product_id=detail.product_id)
#                 _create_details(db, db_detail)
#
#             db.refresh(product_db)
#             print(f"Added details to product: {product_db}")
#             return product_db
#
#     except IntegrityError as e:
#         print(f"Unexpected error when creating detail: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected Error")
#     except SQLAlchemyError as e:
#         print(f"Unexpected error when creating detail: {e}")
#         raise HTTPException(status_code=500, detail="Unexpected Error")


def _create_details(db: Session, detail: ProductDetail) -> ProductDetail:
    """
    Create a detail.

    :param db: SQLAlchemy database session.
    :type db: Session
    :param detail: Detail to be created.
    :type detail: ProductDetail

    :return: Post
    """
    try:
        existing_detail = db.query(ProductDetail).filter(
            ProductDetail.description == detail.description and ProductDetail.product_id.id == detail.product_id.id).first()
        if existing_detail is None:
            db.add(detail)  # Add the detail
            db.commit()  # Commit the change
            print(f"Created detail {detail} belonging to the product ")
            return db.query(ProductDetail).filter(ProductDetail.description == detail.description).first()
        else:
            print(f"Detail already exists for this product in database: {detail}")
            raise HTTPException(status_code=400, detail="Detail already exists for this product in database:")
    except IntegrityError as e:
        print(f"Unexpected error when creating detail: {e}")
        raise HTTPException(status_code=500, detail="Unexpected Error")
    except SQLAlchemyError as e:
        print(f"Unexpected error when creating detail: {e}")
        raise HTTPException(status_code=500, detail="Unexpected Error")


def inactivated_product(product_id: int, db: Session):
    db_product = get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        prodcut = db.query(Product).filter(Product.id == product_id).one()
        prodcut.active = False
        db.commit()  # Commit the change
        raise HTTPException(status_code=200, detail="Product delete successfully")
