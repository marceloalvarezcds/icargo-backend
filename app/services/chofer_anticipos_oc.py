from sqlalchemy.orm import Session  # type: ignore

from app.repositories import (
    edit_orden_carga,
    get_orden_carga_with_anticipo_liberado_list_by_chofer_id,
)
from app.schemas import ChoferEditForm, OrdenCargaEditForm


def bloquear_anticipos_desde_el_chofer(
    db: Session,
    id: int,
    data: ChoferEditForm,
    gestor_carga_id: int,
    modified_by: str,
):
    if data.anticipos_bloqueados:
        oc_list = get_orden_carga_with_anticipo_liberado_list_by_chofer_id(db, id)
        for oc in oc_list:
            edit_orden_carga(
                oc,
                db,
                OrdenCargaEditForm(anticipos_liberados=False),
                gestor_carga_id,
                modified_by,
            )
