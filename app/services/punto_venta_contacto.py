from typing import Dict, List, Optional

from fastapi import HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Contacto, PuntoVenta, PuntoVentaContactoGestorCarga
from app.schemas import ContactoForm

from .contacto import get_contacto_by


def create_contacto(
    db: Session,
    data: ContactoForm,
    punto_venta: PuntoVenta,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    contacto = get_contacto_by(db, data.telefono, data.email)
    if not contacto:
        contacto = repositories.create_contacto(db, data, modified_by)
    repositories.create_punto_venta_contacto_gestor_carga(
        db,
        data.cargo,
        punto_venta,
        contacto,
        gestor_carga_id,
        data.alias if data.alias else f"{contacto.nombre} {contacto.apellido}",
        modified_by,
    )
    return contacto


def get_contacto_by_id(db: Session, id: int) -> Contacto:
    obj = repositories.get_contacto_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return obj


def edit_contacto(
    id: int,
    db: Session,
    data: ContactoForm,
    punto_venta: PuntoVenta,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    obj = get_contacto_by_id(db, id)
    cargo = data.cargo
    contacto = repositories.edit_contacto(obj, db, data, modified_by)
    punto_venta_contacto_obj = repositories.get_punto_venta_contacto_gestor_carga_by(
        db, cargo.id, punto_venta.id, contacto.id, gestor_carga_id
    )
    if punto_venta_contacto_obj:
        repositories.edit_punto_venta_contacto_gestor_carga(
            punto_venta_contacto_obj,
            db,
            cargo,
            punto_venta,
            contacto,
            gestor_carga_id,
            (
                data.alias
                if data.alias
                else punto_venta_contacto_obj.alias
                if punto_venta_contacto_obj.alias
                else f"{contacto.nombre} {contacto.apellido}"
            ),
            modified_by,
        )
    else:
        create_contacto(db, data, punto_venta, gestor_carga_id, modified_by)
    return contacto


def delete_contacto(
    db: Session,
    id: int,
    cargo_id: int,
    punto_venta: PuntoVenta,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    contacto = get_contacto_by_id(db, id)
    punto_venta_contacto_obj = repositories.get_punto_venta_contacto_gestor_carga_by(
        db, cargo_id, punto_venta.id, contacto.id, gestor_carga_id
    )
    if punto_venta_contacto_obj:
        repositories.delete_punto_venta_contacto_gestor_carga(
            db,
            punto_venta_contacto_obj.id,
            modified_by,
        )
    return contacto


def update_punto_venta_contacto_list(
    db: Session,
    contactoList: List[ContactoForm],
    punto_venta: PuntoVenta,
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    if gestor_carga_id:
        contactos: List[PuntoVentaContactoGestorCarga] = punto_venta.contactos
        has_contactos = len(contactos) > 0
        if has_contactos:
            found: Dict[int, bool] = {}
            created: Dict[str, bool] = {}
            for contacto in contactos:
                contacto_id = contacto.contacto_id
                found[contacto_id] = (
                    found[contacto_id] if contacto_id in found else False
                )
                for contactoForm in contactoList:
                    if not contactoForm.id and contactoForm.telefono not in created:
                        created[contactoForm.telefono] = True
                        create_contacto(
                            db,
                            contactoForm,
                            punto_venta,
                            gestor_carga_id,
                            modified_by,
                        )
                    elif contacto_id == contactoForm.id and not found[contacto_id]:
                        found[contacto_id] = True
                        edit_contacto(
                            contacto_id,
                            db,
                            contactoForm,
                            punto_venta,
                            gestor_carga_id,
                            modified_by,
                        )
                if not found[contacto_id]:
                    delete_contacto(
                        db,
                        contacto_id,
                        contacto.cargo_id,
                        punto_venta,
                        gestor_carga_id,
                        modified_by,
                    )
        else:
            for contactoForm in contactoList:
                create_contacto(
                    db, contactoForm, punto_venta, gestor_carga_id, modified_by
                )
