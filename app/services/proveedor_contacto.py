from typing import Dict, List, Optional

from fastapi import HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Contacto, Proveedor, ProveedorContactoGestorCarga
from app.schemas import ContactoForm

from .contacto import get_contacto_by


def create_contacto(
    db: Session,
    data: ContactoForm,
    proveedor: Proveedor,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    contacto = get_contacto_by(db, data.telefono, data.email)
    if not contacto:
        contacto = repositories.create_contacto(db, data, modified_by)
    repositories.create_proveedor_contacto_gestor_carga(
        db,
        data.cargo,
        proveedor,
        contacto,
        gestor_carga_id,
        data.alias,
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
    proveedor: Proveedor,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    obj = get_contacto_by_id(db, id)
    cargo = data.cargo
    contacto = repositories.edit_contacto(obj, db, data, modified_by)
    proveedor_contacto_obj = repositories.get_proveedor_contacto_gestor_carga_by(
        db, proveedor.id, contacto.id, gestor_carga_id
    )
    if proveedor_contacto_obj:
        repositories.edit_proveedor_contacto_gestor_carga(
            proveedor_contacto_obj,
            db,
            cargo,
            proveedor,
            contacto,
            gestor_carga_id,
            data.alias,
            modified_by,
        )
    else:
        create_contacto(db, data, proveedor, gestor_carga_id, modified_by)
    return contacto


def delete_contacto(
    db: Session,
    id: int,
    cargo_id: int,
    proveedor: Proveedor,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    contacto = get_contacto_by_id(db, id)
    proveedor_contacto_obj = (
        repositories.get_proveedor_contacto_gestor_carga_by_cargo_id(
            db, cargo_id, proveedor.id, contacto.id, gestor_carga_id
        )
    )
    if proveedor_contacto_obj:
        repositories.delete_proveedor_contacto_gestor_carga(
            db,
            proveedor_contacto_obj.id,
            modified_by,
        )
    return contacto


def update_proveedor_contacto_list(
    db: Session,
    contactoList: List[ContactoForm],
    proveedor: Proveedor,
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    if gestor_carga_id:
        contactos: List[ProveedorContactoGestorCarga] = proveedor.contactos
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
                            proveedor,
                            gestor_carga_id,
                            modified_by,
                        )
                    elif contacto_id == contactoForm.id and not found[contacto_id]:
                        found[contacto_id] = True
                        edit_contacto(
                            contacto_id,
                            db,
                            contactoForm,
                            proveedor,
                            gestor_carga_id,
                            modified_by,
                        )
                if not found[contacto_id]:
                    delete_contacto(
                        db,
                        contacto_id,
                        contacto.cargo_id,
                        proveedor,
                        gestor_carga_id,
                        modified_by,
                    )
        else:
            for contactoForm in contactoList:
                create_contacto(
                    db, contactoForm, proveedor, gestor_carga_id, modified_by
                )
