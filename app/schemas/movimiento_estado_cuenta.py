from app.schemas.date_model import Date
from typing import Dict, List, Optional
from urllib.parse import urlencode

from pydantic import BaseModel
from sqlalchemy.engine.row import Row  # type: ignore

from .rounded_decimal_model import RoundedDecimal

class MovimientoEstadoCuentaForm(BaseModel):
    contraparte_id: int
    contraparte: str
    contraparte_numero_documento: str
    punto_venta_id: Optional[int]
    contraparte_pdv: Optional[str]
    contraparte_numero_documento_pdv: Optional[str]
    tipo_contraparte_id: int
    tipo_contraparte_descripcion: str
    moneda_id: int


class MovimientoEstadoCuenta(BaseModel):
    movimiento_id: Optional[int]
    liquidacion_id: Optional[int]
    fecha: Optional[Date]
    tipo_cuenta_descripcion: str
    tipo_movimiento_concepto: str
    nro_documento_relacionado: int
    detalle: str
    info: Optional[str]
    estado: str
    pendiente: RoundedDecimal
    en_proceso: RoundedDecimal
    confirmado: RoundedDecimal
    finalizado: RoundedDecimal 
    saldo: Optional[RoundedDecimal]
    # q: str

    @classmethod
    def from_dict(cls, dic: Dict) -> "MovimientoEstadoCuenta":
        return MovimientoEstadoCuenta(**dic)

    @classmethod
    def from_orm_row(cls, row: Row) -> "MovimientoEstadoCuenta":
        dic = row._asdict()
        # qdic = {
        #     "contraparte_id": dic["contraparte_id"],
        #     "contraparte": dic["contraparte"],
        #     "contraparte_numero_documento": dic["contraparte_numero_documento"],
        #     "tipo_contraparte_id": dic["tipo_contraparte_id"],

        #     "punto_venta_id": dic["punto_venta_id"],
        #     "contraparte_pdv": dic["contraparte_pdv"],
        #     "contraparte_numero_documento_pdv": dic["contraparte_numero_documento_pdv"],
        # }
        #dic["q"] = urlencode(qdic)
        return cls.from_dict(dic)

    @classmethod
    def result_of_query_to_list(cls, results: List[Row]) -> List["MovimientoEstadoCuenta"]:
        list_to_return = []
        for row in results:
            list_to_return.append(cls.from_orm_row(row))
        return list_to_return

