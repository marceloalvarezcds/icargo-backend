from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import ComposicionJuridica, GestorCarga, PuntoVenta, TipoDocumento
from app.models.ciudad import Ciudad
from app.repositories import (
    get_cargo_by_descripcion,
    get_contacto_by_email,
    get_punto_venta_by,
)

from .gestor_carga_punto_venta_seeds import gestor_carga_punto_venta_seeds
from .punto_venta_contacto_gestor_carga_seeds import (
    punto_venta_contacto_gestor_carga_seeds,
)


def punto_venta_seeds(
    db: Session,
    nombre: str,
    proveedor_id: int,
    tipo_documento: Optional[TipoDocumento],
    numero_documento: str,
    digito_verificador: Optional[str],
    composicion_juridica: Optional[ComposicionJuridica],
    telefono: str,
    email: str,
    pagina_web: str,
    direccion: Optional[str],
    latitud: float,
    longitud: float,
    alias: str,
    cargo_descripcion: str,
    contacto_email: str,
    contacto_alias: str,
    gestor_carga: GestorCarga,
    ciudad: Optional[Ciudad],
):
    ciudad_id = ciudad.id if ciudad else None
    if tipo_documento and composicion_juridica and ciudad_id:
        obj = get_punto_venta_by(db, tipo_documento.id, numero_documento)
        if not obj:
            punto_venta = PuntoVenta(
                nombre=nombre,
                nombre_corto=None,
                proveedor_id=proveedor_id,
                tipo_documento_id=tipo_documento.id,
                numero_documento=numero_documento,
                digito_verificador=digito_verificador,
                composicion_juridica_id=composicion_juridica.id,
                logo=None,
                estado=EstadoEnum.ACTIVO.value,
                telefono=telefono,
                email=email,
                pagina_web=pagina_web,
                info_complementaria=None,
                direccion=direccion,
                latitud=latitud,
                longitud=longitud,
                ciudad_id=ciudad_id,
            )
            db.add(punto_venta)
            db.commit()
            gestor_carga_punto_venta_seeds(db, punto_venta, gestor_carga, alias)
            cargo = get_cargo_by_descripcion(db, cargo_descripcion)
            contacto = get_contacto_by_email(db, contacto_email)
            punto_venta_contacto_gestor_carga_seeds(
                db, cargo, punto_venta, contacto, gestor_carga, contacto_alias
            )
