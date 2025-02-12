from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import TipoCuenta, TipoDocumentoRelacionado
from app.schemas import TipoCuentaForm
from app.services import generic_service as service
from app.services import seleccionable_service


def get_tipo_cuenta_list(
    db: Session,
) -> List[TipoCuenta]:
    return service.get_list(
        TipoCuenta,
        db
    )


def get_tipo_cuenta_list_by_tipo_documento_relacionado_otro(
    db: Session,
) -> List[TipoCuenta]:
    otro: Optional[TipoDocumentoRelacionado] = seleccionable_service.get_by_descripcion(
        TipoDocumentoRelacionado, db, "Otro"
    )
    if otro:
        return service.get_list_by_filter(
            TipoCuenta,
            db,
            tipo_documento_relacionado_id=otro.id,
        )
    return []


def get_tipo_cuenta_active_list(
    db: Session,
) -> List[TipoCuenta]:

    return service.get_list_by_filter(
        TipoCuenta,
        db,
        estado=EstadoEnum.ACTIVO.value,
    )


def get_tipo_cuenta_active_list_by_tipo_documento_relacionado_otro(
    db: Session,
) -> List[TipoCuenta]:
    otro: Optional[TipoDocumentoRelacionado] = seleccionable_service.get_by_descripcion(
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


def _check_codigo(codigo: str):
    if len(codigo) > 3:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="El código debe poseer hasta 3 caracteres",
        )


def create_tipo_cuenta(
    db: Session, data: TipoCuentaForm, modified_by: str
) -> TipoCuenta:
    otro: Optional[TipoDocumentoRelacionado] = seleccionable_service.get_by_descripcion(
        TipoDocumentoRelacionado, db, "Otro"
    )
    data.tipo_documento_relacionado_id = otro.id if otro else None
    codigo = data.codigo
    _check_codigo(codigo)
    return service.create(
        TipoCuenta,
        db,
        data,
        modified_by,
        f"La Cuenta con código {codigo} ya existe",
        codigo=codigo,
    )


def edit_tipo_cuenta(
    id: int, db: Session, data: TipoCuentaForm, modified_by: str
) -> TipoCuenta:
    codigo = data.codigo
    _check_codigo(codigo)
    return service.edit(
        TipoCuenta,
        db,
        id,
        data,
        modified_by,
        f"La Cuenta con código {codigo} ya existe",
        codigo=codigo,
    )
