from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore
from sqlalchemy.sql import or_  # type: ignore

from app.models import Ciudad, Localidad, Pais


def get_ciudad_by_nombre_and_localidad_id(
    db: Session, nombre: str, localidad_id: int
) -> Optional[Ciudad]:
    return (
        db.query(Ciudad)
        .filter(and_(Ciudad.nombre == nombre, Ciudad.localidad_id == localidad_id))
        .first()
    )


def get_ciudad_list_by_localidad_id(db: Session, localidad_id: int) -> List[Ciudad]:
    return (
        db.query(Ciudad)
        .filter(Ciudad.localidad_id == localidad_id)
        .order_by(Ciudad.nombre)
        .all()
    )


def get_ciudad_list(
    db: Session, page: int = 1, pageSize: int = 10, queryFilter: str = ""
) -> List[Ciudad]:
    if page < 1:
        page = 1
    if pageSize < 1 or pageSize > 100:
        pageSize = 10
    query = db.query(Ciudad)
    if queryFilter is not None and queryFilter != "":
        if queryFilter.isnumeric():
            query = query.filter(Ciudad.id == int(queryFilter))
        else:
            queryFilter = "%" + queryFilter + "%"
            query = query.join(Ciudad.localidad, Localidad.pais)
            query = query.filter(
                or_(
                    Ciudad.nombre.ilike(queryFilter),
                    Localidad.nombre.ilike(queryFilter),
                    Pais.nombre.ilike(queryFilter),
                )
            )

    return (
        query.order_by(Ciudad.nombre)
        .limit(pageSize)
        .offset((page - 1) * pageSize)
        .all()
    )


def get_ciudad_count(db: Session, queryFilter: str = "") -> int:
    query = db.query(Ciudad)
    if queryFilter is not None and queryFilter != "":
        if queryFilter.isnumeric():
            query = query.filter(Ciudad.id == int(queryFilter))
        else:
            queryFilter = "%" + queryFilter + "%"
            query = query.join(Ciudad.localidad, Localidad.pais)
            query = query.filter(
                or_(
                    Ciudad.nombre.ilike(queryFilter),
                    Localidad.nombre.ilike(queryFilter),
                    Pais.nombre.ilike(queryFilter),
                )
            )

    return query.count()
