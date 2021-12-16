from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import FleteDestinatarioEnum
from app.models import (
    CentroOperativo,
    CentroOperativoContactoGestorCarga,
    Flete,
    Remitente,
    RemitenteContactoGestorCarga,
    User,
)
from app.repositories import get as get_user_by_id
from app.repositories import (
    get_centro_operativo_contacto_gestor_carga_by_id,
    get_flete_by_id,
    get_remitente_contacto_gestor_carga_by_id,
    get_user_list_by_gestor_carga_id,
    update_flete_destinatarios,
)
from app.schemas import FleteDestinatario


def get_destinatario_list_by_flete_id(
    db: Session, flete_id: int, gestor_cuenta_id: Optional[int]
) -> List[FleteDestinatario]:
    lista: List[FleteDestinatario] = []
    if gestor_cuenta_id:
        users = get_user_list_by_gestor_carga_id(db, gestor_cuenta_id)
        for item in users:
            lista.append(
                FleteDestinatario(
                    id=item.id,
                    tipo_destinatario=FleteDestinatarioEnum.USUARIO,
                    email=item.email,
                    nombre=f"{item.first_name} {item.last_name}",
                )
            )
    flete = get_flete_by_id(db, flete_id)
    if flete:
        remitente: Remitente = flete.remitente
        remitente_contactos: List[RemitenteContactoGestorCarga] = remitente.contactos
        origen: CentroOperativo = flete.origen
        origen_contactos: List[CentroOperativoContactoGestorCarga] = origen.contactos
        destino: CentroOperativo = flete.destino
        destino_contactos: List[CentroOperativoContactoGestorCarga] = destino.contactos
        for item in remitente_contactos:
            if gestor_cuenta_id and item.gestor_carga_id == gestor_cuenta_id:
                lista.append(
                    FleteDestinatario(
                        id=item.id,
                        tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                        email=item.contacto_email,
                        nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
                    )
                )
        for item in origen_contactos:
            if gestor_cuenta_id and item.gestor_carga_id == gestor_cuenta_id:
                lista.append(
                    FleteDestinatario(
                        id=item.id,
                        tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                        email=item.contacto_email,
                        nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
                    )
                )
        for item in destino_contactos:
            if gestor_cuenta_id and item.gestor_carga_id == gestor_cuenta_id:
                lista.append(
                    FleteDestinatario(
                        id=item.id,
                        tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                        email=item.contacto_email,
                        nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
                    )
                )
    return lista


def get_destinatario_selected_list_by_flete(flete: Flete) -> List[FleteDestinatario]:
    lista: List[FleteDestinatario] = []
    cList: List[
        CentroOperativoContactoGestorCarga
    ] = flete.emision_orden_centro_operativo_destinatarios
    rList: List[
        RemitenteContactoGestorCarga
    ] = flete.emision_orden_remitente_destinatarios
    uList: List[User] = flete.emision_orden_user_destinatarios
    for item in cList:
        lista.append(
            FleteDestinatario(
                id=item.id,
                tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                email=item.contacto_email,
                nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
            )
        )
    for item in rList:
        lista.append(
            FleteDestinatario(
                id=item.id,
                tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                email=item.contacto_email,
                nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
            )
        )
    for item in uList:
        lista.append(
            FleteDestinatario(
                id=item.id,
                tipo_destinatario=FleteDestinatarioEnum.USUARIO,
                email=item.email,
                nombre=f"{item.first_name} {item.last_name}",
            )
        )
    return lista


def update_flete_destinatario_list(
    db: Session,
    dataList: List[FleteDestinatario],
    flete: Flete,
    modified_by: str,
):
    for data in dataList:
        if data.tipo_destinatario == FleteDestinatarioEnum.CENTRO_OPERATIVO.value:
            obj = get_centro_operativo_contacto_gestor_carga_by_id(db, data.id)
            if obj:
                flete.emision_orden_centro_operativo_destinatarios.append(obj)
        elif data.tipo_destinatario == FleteDestinatarioEnum.REMITENTE.value:
            obj = get_remitente_contacto_gestor_carga_by_id(db, data.id)
            if obj:
                flete.emision_orden_remitente_destinatarios.append(obj)
        elif data.tipo_destinatario == FleteDestinatarioEnum.USUARIO.value:
            obj = get_user_by_id(db, data.id)
            if obj:
                flete.emision_orden_user_destinatarios.append(obj)
    update_flete_destinatarios(
        flete,
        db,
        modified_by,
    )
