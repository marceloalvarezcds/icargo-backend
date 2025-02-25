
from typing import List, Optional
from fastapi import HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.models import TextoLegal
from app.schemas import TextoLegalBaseModel, AuthUser, TextoLegalModel
from app.services import generic_service as service
from app.logger import logger


def get_texto_legal_list_by_gestor(db: Session, gestor_carga_id: Optional[int]) -> List[TextoLegal]:
    if gestor_carga_id:
        lista = service.get_list_all_or_by_gestor_carga_id(TextoLegal, db, gestor_carga_id)
        return lista

    return service.get_list(TextoLegal, db)


def get_texto_legal_list(db: Session) -> List[TextoLegal]:
    return service.get_list(TextoLegal, db)


def get_texto_legal_by_id(db: Session, id: int) -> TextoLegal:
    obj = service.get_by_id(TextoLegal, db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Banco no encontrado")
    return obj


def crear_texto_legal(
    db: Session, data: TextoLegalBaseModel, usr: AuthUser
) -> TextoLegal:

    titulo = data.titulo
    data.gestor_carga_id = usr.gestor_carga_id

    return service.create(
        TextoLegal,
        db,
        data,
        usr.username,
        f"Texto legal con titulo {data.titulo} ya existe",
        titulo=titulo,
    )


def edit_texto_legal(
    id: int, db: Session, data: TextoLegalBaseModel, usr: AuthUser
) -> TextoLegal:


    titulo = data.titulo
    data.gestor_carga_id = usr.gestor_carga_id

    return service.edit(
        TextoLegal,
        db,
        id,
        data,
        usr.username,
        f"Texto legal con titulo {data.titulo} ya existe",
        titulo=titulo,
    )
