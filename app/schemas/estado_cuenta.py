from decimal import Decimal
from typing import Dict, List
from urllib.parse import urlencode

from pydantic import BaseModel
from sqlalchemy.engine.row import Row  # type: ignore


class EstadoCuenta(BaseModel):
    contraparte: str
    contraparte_numero_documento: str
    tipo_contraparte_id: int
    tipo_contraparte_descripcion: str
    pendiente: Decimal
    en_proceso: Decimal
    confirmado: Decimal
    finalizado: Decimal
    q: str

    @classmethod
    def from_dict(cls, dic: Dict) -> "EstadoCuenta":
        return EstadoCuenta(**dic)

    @classmethod
    def from_orm_row(cls, row: Row) -> "EstadoCuenta":
        dic = row._asdict()
        qdic = {
            "contraparte": dic["contraparte"],
            "contraparte_numero_documento": dic["contraparte_numero_documento"],
            "tipo_contraparte_id": dic["tipo_contraparte_id"],
        }
        dic["q"] = urlencode(qdic)
        return cls.from_dict(dic)

    @classmethod
    def result_of_query_to_list(cls, results: List[Row]) -> List["EstadoCuenta"]:
        list_to_return = []
        for row in results:
            list_to_return.append(cls.from_orm_row(row))
        return list_to_return
