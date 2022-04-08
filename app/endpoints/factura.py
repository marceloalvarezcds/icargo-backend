from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/liquidacion/{liquidacion_id}", response_model=List[schemas.Factura])
async def read_factura_list_liquidacion_id(
    liquidacion_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.FACTURA)),  # noqa: B008
):
    return repositories.get_factura_list_by_liquidacion_id(db, liquidacion_id)


@api.get("/{id}", response_model=schemas.Factura)
async def read_factura_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.FACTURA)),  # noqa: B008
):
    return services.get_factura_by_id(db, id)


@api.post("/", response_model=schemas.Factura)
async def add_new_factura(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.FacturaForm] = Form(...),  # type: ignore  # noqa: B008
    foto_file: UploadFile = File(...),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.FACTURA)),  # noqa: B008
):
    return await services.create_factura(
        db, data, foto_file, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Factura)
async def edit_factura(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.FacturaForm] = Form(...),  # type: ignore  # noqa: B008
    foto_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.FACTURA)),  # noqa: B008
):
    return await services.edit_factura(
        id, db, data, foto_file, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Factura)
async def delete_factura(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.FACTURA)),  # noqa: B008
):
    return services.delete_factura(db, id, current_user.username)
