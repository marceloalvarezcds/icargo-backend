from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore
from app.services import contribuyente as service
from app import schemas
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()

@api.get("/", response_model=List[schemas.Contribuyente])
async def read_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.FACTURA)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return service.get_list(db, current_user.gestor_carga_id)


#@api.get("/{id}", response_model=schemas.Contribuyente)
#async def read_by_id(
#    id: int,
#    db: Session = Depends(get_db_session),  # noqa: B008
#    _: bool = Depends(Permiso(a.VER, m.FACTURA)),  # noqa: B008
#):
#    return services.get_by_id(db, id)
