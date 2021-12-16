from typing import Dict, List

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Flete, FleteAnticipo
from app.schemas import FleteAnticipoForm


def update_flete_anticipo_list(
    db: Session,
    dataList: List[FleteAnticipoForm],
    flete: Flete,
    modified_by: str,
):
    lista: List[FleteAnticipo] = flete.anticipos
    has_lista = len(lista) > 0
    if has_lista:
        found: Dict[int, bool] = {}
        created: Dict[str, bool] = {}
        for item in lista:
            item_id = item.id
            found[item_id] = found[item_id] if item_id in found else False
            for data in dataList:
                key = f"{data.tipo_id}_{flete.id}"
                if not data.id and key not in created:
                    created[key] = True
                    repositories.create_flete_anticipo(
                        db,
                        flete.id,
                        data,
                        modified_by,
                    )
                elif item_id == data.id and not found[item_id]:
                    obj = repositories.get_flete_anticipo_by_id(db, item_id)
                    if obj:
                        found[item_id] = True
                        repositories.edit_flete_anticipo(
                            obj,
                            db,
                            data,
                            modified_by,
                        )
            if not found[item_id]:
                repositories.delete_flete_anticipo(
                    db,
                    item_id,
                    modified_by,
                )
    else:
        for data in dataList:
            repositories.create_flete_anticipo(
                db,
                flete.id,
                data,
                modified_by,
            )
