from typing import Dict, List

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Flete, FleteComplemento
from app.schemas import FleteComplementoForm


def update_flete_complemento_list(
    db: Session,
    dataList: List[FleteComplementoForm],
    flete: Flete,
    modified_by: str,
):
    lista: List[FleteComplemento] = flete.complementos
    has_lista = len(lista) > 0
    if has_lista:
        found: Dict[int, bool] = {}
        created: Dict[str, bool] = {}
        for item in lista:
            item_id = item.id
            found[item_id] = found[item_id] if item_id in found else False
            for data in dataList:
                key = f"{data.concepto_id}_{data.propietario_moneda_id}_{data.propietario_monto}_{data.remitente_moneda_id}_{data.remitente_monto}_{flete.id}"  # noqa: B950
                if not data.id and key not in created:
                    created[key] = True
                    repositories.create_flete_complemento(
                        db,
                        flete.id,
                        data,
                        modified_by,
                    )
                elif item_id == data.id and not found[item_id]:
                    obj = repositories.get_flete_complemento_by_id(db, item_id)
                    if obj:
                        found[item_id] = True
                        repositories.edit_flete_complemento(
                            obj,
                            db,
                            data,
                            modified_by,
                        )
            if not found[item_id]:
                repositories.delete_flete_complemento(
                    db,
                    item_id,
                    modified_by,
                )
    else:
        for data in dataList:
            repositories.create_flete_complemento(
                db,
                flete.id,
                data,
                modified_by,
            )
