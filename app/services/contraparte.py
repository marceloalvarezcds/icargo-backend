from typing import List, Union, cast

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.enums import TipoContraparteEnum
from app.models import TipoContraparte
from app.schemas import Chofer, Contraparte, Propietario, Proveedor, Remitente


def get_tipo_contraparte_by_id(db: Session, id: int) -> TipoContraparte:
    obj = repositories.get_tipo_comprobante_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de contraparte no encontrado")
    return obj


def get_contraparte_list_by_tipo_contraparte_id(
    db: Session, tipo_contraparte_id: int
) -> List[Contraparte]:
    tipo_contraparte = get_tipo_contraparte_by_id(db, tipo_contraparte_id)
    if tipo_contraparte.descripcion == TipoContraparteEnum.OTRO.value:
        return repositories.get_contraparte_list_by_tipo_contraparte_id(
            db, tipo_contraparte.id
        )
    elif tipo_contraparte.descripcion == TipoContraparteEnum.PROPIETARIO.value:
        lista = repositories.get_propietario_list(db)
        return Contraparte.get_list_by_propietario(
            cast(List[Propietario], lista), tipo_contraparte
        )
    else:
        lista = []
        if tipo_contraparte.descripcion == TipoContraparteEnum.CHOFER.value:
            lista = repositories.get_chofer_list(db)
        elif tipo_contraparte.descripcion == TipoContraparteEnum.PROVEEDOR.value:
            lista = repositories.get_proveedor_list(db)
        elif tipo_contraparte.descripcion == TipoContraparteEnum.REMITENTE.value:
            lista = repositories.get_remitente_list(db)
        return Contraparte.get_list_by_model(
            cast(List[Union[Chofer, Proveedor, Remitente]], lista), tipo_contraparte
        )
