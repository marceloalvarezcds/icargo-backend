from typing import List, Union

from pydantic import BaseModel

from .chofer import Chofer
from .propietario import Propietario
from .proveedor import Proveedor
from .remitente import Remitente
from .tipo_contraparte import TipoContraparte


class PartialIdentityModel(BaseModel):
    id: int
    nombre: str
    numero_documento: str

    @classmethod
    def to_partial(
        cls, item: Union[Chofer, Proveedor, Remitente]
    ) -> "PartialIdentityModel":
        return PartialIdentityModel(
            id=item.id,
            nombre=item.nombre,
            numero_documento=item.numero_documento,
        )


class Contraparte(BaseModel):
    id: int
    contraparte: str
    contraparte_numero_documento: str
    info: str
    tipo_contraparte_id: int
    tipo_contraparte_descripcion: str

    @classmethod
    def get_by_model(
        cls, item: PartialIdentityModel, tipo: TipoContraparte
    ) -> "Contraparte":
        return Contraparte(
            id=item.id,
            contraparte=item.nombre,
            contraparte_numero_documento=item.numero_documento,
            info=f"{item.nombre} - {item.numero_documento}",
            tipo_contraparte_id=tipo.id,
            tipo_contraparte_descripcion=tipo.descripcion,
        )

    @classmethod
    def get_list_by_model(
        cls, list: List[Union[Chofer, Proveedor, Remitente]], tipo: TipoContraparte
    ) -> List["Contraparte"]:
        return [
            cls.get_by_model(PartialIdentityModel.to_partial(it), tipo) for it in list
        ]

    @classmethod
    def get_by_propietario(
        cls, item: Propietario, tipo: TipoContraparte
    ) -> "Contraparte":
        return Contraparte(
            id=item.id,
            contraparte=item.nombre,
            contraparte_numero_documento=item.ruc,
            info=f"{item.nombre} - {item.ruc}",
            tipo_contraparte_id=tipo.id,
            tipo_contraparte_descripcion=tipo.descripcion,
        )

    @classmethod
    def get_list_by_propietario(
        cls, list: List[Propietario], tipo: TipoContraparte
    ) -> List["Contraparte"]:
        return [cls.get_by_propietario(it, tipo) for it in list]
