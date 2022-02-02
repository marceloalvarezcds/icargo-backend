from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get(
    "/flete_anticipo/{flete_anticipo_id}/orden_carga/{orden_carga_id}",
    response_model=schemas.OrdenCargaAnticipoSaldo,
)
async def read_orden_carga_anticipo_saldo_by_flete_anticipo_id_and_orden_carga_id(
    flete_anticipo_id: int,
    orden_carga_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO)),  # noqa: B008
):
    return repositories.get_orden_carga_anticipo_saldo_by(
        db, flete_anticipo_id, orden_carga_id
    )
