from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import TipoCuenta, TipoDocumentoRelacionado
from app.schemas import TipoCuentaForm
from app.services import seleccionable_service as service


def get_tipo_cuenta_list_by_tipo_documento_relacionado_otro(
    db: Session,
) -> List[TipoCuenta]:
    otro: Optional[TipoDocumentoRelacionado] = service.get_by_descripcion(
        TipoDocumentoRelacionado, db, "Otro"
    )
    if otro:
        return service.get_list_by_filter(
            TipoCuenta,
            db,
            tipo_documento_relacionado_id=otro.id,
        )
    return []


def get_tipo_cuenta_active_list_by_tipo_documento_relacionado_otro(
    db: Session,
) -> List[TipoCuenta]:
    otro: Optional[TipoDocumentoRelacionado] = service.get_by_descripcion(
        TipoDocumentoRelacionado, db, "Otro"
    )
    if otro:
        return service.get_list_by_filter(
            TipoCuenta,
            db,
            estado=EstadoEnum.ACTIVO.value,
            tipo_documento_relacionado_id=otro.id,
        )
    return []


def create_tipo_cuenta(
    db: Session, data: TipoCuentaForm, modified_by: str
) -> TipoCuenta:
    otro: Optional[TipoDocumentoRelacionado] = service.get_by_descripcion(
        TipoDocumentoRelacionado, db, "Otro"
    )
    data.tipo_documento_relacionado_id = otro.id if otro else None
    return service.create(TipoCuenta, db, data, modified_by, "El TipoCuenta")
