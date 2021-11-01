from typing import Dict, List, Optional

from fastapi import HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import CentroOperativo, CentroOperativoContactoGestorCarga, Contacto
from app.schemas import ContactoForm


def get_contacto_by(
    db: Session, telefono: Optional[str], email: Optional[str]
) -> Optional[Contacto]:
    if telefono and email:
        return repositories.get_contacto_by_telefono_and_email(db, telefono, email)
    elif telefono:
        return repositories.get_contacto_by_telefono(db, telefono)
    elif email:
        return repositories.get_contacto_by_email(db, email)
    return None


def create_contacto(
    db: Session,
    data: ContactoForm,
    centro_operativo: CentroOperativo,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    contacto = get_contacto_by(db, data.telefono, data.email)
    if not contacto:
        contacto = repositories.create_contacto(db, data, modified_by)
    repositories.create_centro_operativo_contacto_gestor_carga(
        db,
        data.cargo,
        centro_operativo,
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
    centro_operativo: CentroOperativo,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    obj = get_contacto_by_id(db, id)
    cargo = data.cargo
    contacto = repositories.edit_contacto(obj, db, data, modified_by)
    centro_operativo_contacto_obj = (
        repositories.get_centro_operativo_contacto_gestor_carga_by(
            db, cargo.id, centro_operativo.id, contacto.id, gestor_carga_id
        )
    )
    if centro_operativo_contacto_obj:
        repositories.edit_centro_operativo_contacto_gestor_carga(
            centro_operativo_contacto_obj,
            db,
            cargo,
            centro_operativo,
            contacto,
            gestor_carga_id,
            (
                data.alias
                if data.alias
                else centro_operativo_contacto_obj.alias
                if centro_operativo_contacto_obj.alias
                else f"{contacto.nombre} {contacto.apellido}"
            ),
            modified_by,
        )
    else:
        create_contacto(db, data, centro_operativo, gestor_carga_id, modified_by)
    return contacto


def delete_contacto(
    db: Session,
    id: int,
    cargo_id: int,
    centro_operativo: CentroOperativo,
    gestor_carga_id: int,
    modified_by: str,
) -> Contacto:
    contacto = get_contacto_by_id(db, id)
    centro_operativo_contacto_obj = (
        repositories.get_centro_operativo_contacto_gestor_carga_by(
            db, cargo_id, centro_operativo.id, contacto.id, gestor_carga_id
        )
    )
    if centro_operativo_contacto_obj:
        repositories.delete_centro_operativo_contacto_gestor_carga(
            db,
            centro_operativo_contacto_obj.id,
            modified_by,
        )
    return contacto


def update_contacto_list(
    db: Session,
    contactoList: List[ContactoForm],
    centro_operativo: CentroOperativo,
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    if gestor_carga_id:
        contactos: List[CentroOperativoContactoGestorCarga] = centro_operativo.contactos
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
                            centro_operativo,
                            gestor_carga_id,
                            modified_by,
                        )
                    elif contacto_id == contactoForm.id and not found[contacto_id]:
                        found[contacto_id] = True
                        edit_contacto(
                            contacto_id,
                            db,
                            contactoForm,
                            centro_operativo,
                            gestor_carga_id,
                            modified_by,
                        )
                if not found[contacto_id]:
                    delete_contacto(
                        db,
                        contacto_id,
                        contacto.cargo_id,
                        centro_operativo,
                        gestor_carga_id,
                        modified_by,
                    )
        else:
            for contactoForm in contactoList:
                create_contacto(
                    db, contactoForm, centro_operativo, gestor_carga_id, modified_by
                )
