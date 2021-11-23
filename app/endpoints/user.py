from typing import Any, List

from fastapi import APIRouter, Depends, Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/gestor_carga_id", response_model=List[schemas.User])
async def read_user_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.USER)),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_user_list_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )


@api.get("/me", response_model=schemas.UserAccount)
def my_account(
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.USER)),  # noqa: B008
) -> Any:
    """
    Retrieve current user.
    """
    return current_user


@api.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.USER)),  # noqa: B008
    user_in: schemas.UserCreate,
    request: Request,
) -> Any:
    """
    Create new user.
    """
    return services.create_user(
        db, modified_by=current_user.username, user_in=user_in, request=request
    )
