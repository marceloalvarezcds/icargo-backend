from typing import Any, Optional

from fastapi import HTTPException


def get_gestor_carga_by_params(param: Any, gestor_carga_id: Optional[int]) -> int:
    gestor_id = gestor_carga_id if gestor_carga_id else param.gestor_carga_id
    if not gestor_id:
        raise HTTPException(status_code=409, detail="Debe elegir un Gestor de carga")
    return gestor_id
