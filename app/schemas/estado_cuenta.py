from typing import Dict, List, Optional
from urllib.parse import urlencode

from pydantic import BaseModel
from sqlalchemy.engine.row import Row  # type: ignore

from .rounded_decimal_model import RoundedDecimal

class EstadoCuentaForm(BaseModel):
    contraparte_id: int
    contraparte: str
    contraparte_numero_documento: str
    punto_venta_id: Optional[int]
    contraparte_pdv: Optional[str]
    contraparte_numero_documento_pdv: Optional[str]
    tipo_contraparte_id: int
    tipo_contraparte_descripcion: str
    moneda_id: int


class EstadoCuenta(BaseModel):
    contraparte_id: Optional[int]
    contraparte: str
    contraparte_numero_documento: str
    punto_venta_id: Optional[int]
    contraparte_pdv: Optional[str]
    contraparte_numero_documento_pdv: Optional[str]
    tipo_contraparte_id: int
    tipo_contraparte_descripcion: str
    pendiente: RoundedDecimal
    en_proceso: Optional[RoundedDecimal]
    confirmado: RoundedDecimal
    saldo_pendiente: Optional[RoundedDecimal]
    finalizado: RoundedDecimal
    cantidad_pendiente: int
    cantidad_en_proceso: Optional[int]
    cantidad_confirmado: int
    cantidad_finalizado: int
    q: str

    @classmethod
    def from_dict(cls, dic: Dict) -> "EstadoCuenta":
        return EstadoCuenta(**dic)

    @classmethod
    def from_orm_row(cls, row: Row) -> "EstadoCuenta":
        dic = row._asdict()
        qdic = {
            "contraparte_id": dic["contraparte_id"],
            "contraparte": dic["contraparte"],
            "contraparte_numero_documento": dic["contraparte_numero_documento"],
            "tipo_contraparte_id": dic["tipo_contraparte_id"],

            "punto_venta_id": dic["punto_venta_id"],
            "contraparte_pdv": dic["contraparte_pdv"],
            "contraparte_numero_documento_pdv": dic["contraparte_numero_documento_pdv"],
        }
        dic["q"] = urlencode(qdic)
        return cls.from_dict(dic)

    @classmethod
    def result_of_query_to_list(cls, results: List[Row]) -> List["EstadoCuenta"]:
        list_to_return = []
        for row in results:
            list_to_return.append(cls.from_orm_row(row))
        return list_to_return


class ContraparteEstadoCuenta(BaseModel):
    confirmado: RoundedDecimal
    finalizado: RoundedDecimal

    @classmethod
    def from_dict(cls, dic: Dict) -> "ContraparteEstadoCuenta":
        return ContraparteEstadoCuenta(**dic)

    @classmethod
    def from_orm_row(cls, row: Row) -> "ContraparteEstadoCuenta":
        dic = row._asdict()
        return cls.from_dict(dic)
