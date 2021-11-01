from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import get_db_session, reusable_oauth2

api = APIRouter()


@api.get("/{telefono}/{email}", response_model=schemas.Contacto)
async def read_ciudad_list(
    telefono: str,
    email: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return services.get_contacto_by(db, telefono, email)
