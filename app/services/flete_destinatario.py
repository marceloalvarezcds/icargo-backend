from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import FleteDestinatarioCentroOperativoEnum, FleteDestinatarioEnum
from app.models import (
    CentroOperativoContactoGestorCarga,
    Flete,
    FleteCentroOperativoContacto,
    FleteRemitenteContacto,
    FleteUserContacto,
    RemitenteContactoGestorCarga,
    User,
)
from app.repositories import (
    get_centro_operativo_by_id,
    get_centro_operativo_contacto_gestor_carga_by_id,
    get_remitente_by_id,
    get_remitente_contacto_gestor_carga_by_id,
    update_flete_destinatarios,
)
from app.schemas import FleteDestinatario

from .user import get_user_active_list_by_gestor_carga_id, get_user_by_id


def get_destinatario_list_by(
    db: Session,
    remitente_id: int,
    origen_id: int,
    destino_id: int,
    gestor_carga_id: Optional[int],
) -> List[FleteDestinatario]:
    lista: List[FleteDestinatario] = []
    if gestor_carga_id:
        users = get_user_active_list_by_gestor_carga_id(db, gestor_carga_id)
        for item in users:
            lista.append(
                FleteDestinatario(
                    id=item.id,
                    tipo_destinatario=FleteDestinatarioEnum.USUARIO,
                    email=item.email,
                    nombre=f"{item.first_name} {item.last_name}",
                )
            )
    remitente = get_remitente_by_id(db, remitente_id)
    origen = get_centro_operativo_by_id(db, origen_id)
    destino = get_centro_operativo_by_id(db, destino_id)
    if remitente and origen and destino:
        remitente_contactos: List[RemitenteContactoGestorCarga] = remitente.contactos
        origen_contactos: List[CentroOperativoContactoGestorCarga] = origen.contactos
        destino_contactos: List[CentroOperativoContactoGestorCarga] = destino.contactos
        for item in remitente_contactos:
            if gestor_carga_id and item.gestor_carga_id == gestor_carga_id:
                lista.append(
                    FleteDestinatario(
                        id=item.id,
                        tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                        email=item.contacto_email,
                        nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
                    )
                )
        for item in origen_contactos:
            if gestor_carga_id and item.gestor_carga_id == gestor_carga_id:
                lista.append(
                    FleteDestinatario(
                        id=item.id,
                        tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                        tipo_centro_operativo=FleteDestinatarioCentroOperativoEnum.ORIGEN,
                        email=item.contacto_email,
                        nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
                    )
                )
        for item in destino_contactos:
            if gestor_carga_id and item.gestor_carga_id == gestor_carga_id:
                lista.append(
                    FleteDestinatario(
                        id=item.id,
                        tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                        tipo_centro_operativo=FleteDestinatarioCentroOperativoEnum.DESTINO,
                        email=item.contacto_email,
                        nombre=f"{item.contacto_nombre} {item.contacto_apellido}",
                    )
                )
    return lista


def get_destinatario_selected_list_by_flete(flete: Flete) -> List[FleteDestinatario]:
    lista: List[FleteDestinatario] = []
    cList: List[
        FleteCentroOperativoContacto
    ] = flete.emision_orden_centro_operativo_destinatarios
    rList: List[FleteRemitenteContacto] = flete.emision_orden_remitente_destinatarios
    uList: List[FleteUserContacto] = flete.emision_orden_user_destinatarios
    for item in cList:
        co: CentroOperativoContactoGestorCarga = item.centro_operativo_contacto
        lista.append(
            FleteDestinatario(
                id=co.id,
                tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                email=co.contacto_email,
                nombre=f"{co.contacto_nombre} {co.contacto_apellido}",
            )
        )
    for item in rList:
        re: RemitenteContactoGestorCarga = item.remitente_contacto
        lista.append(
            FleteDestinatario(
                id=re.id,
                tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                email=re.contacto_email,
                nombre=f"{re.contacto_nombre} {re.contacto_apellido}",
            )
        )
    for item in uList:
        user: User = item.user_contacto
        lista.append(
            FleteDestinatario(
                id=user.id,
                tipo_destinatario=FleteDestinatarioEnum.USUARIO,
                email=user.email,
                nombre=f"{user.first_name} {user.last_name}",
            )
        )
    return lista


def update_flete_destinatario_list(
    db: Session,
    dataList: Optional[List[FleteDestinatario]],
    flete: Flete,
    modified_by: str,
):
    flete_id = flete.id
    flete.emision_orden_centro_operativo_destinatarios = []
    flete.emision_orden_remitente_destinatarios = []
    flete.emision_orden_user_destinatarios = []
    if dataList:
        for data in dataList:
            if data.tipo_destinatario == FleteDestinatarioEnum.CENTRO_OPERATIVO.value:
                obj = get_centro_operativo_contacto_gestor_carga_by_id(db, data.id)
                if obj:
                    item = FleteCentroOperativoContacto(
                        flete_id=flete_id, centro_operativo_contacto_id=obj.id
                    )
                    flete.emision_orden_centro_operativo_destinatarios.append(item)
            elif data.tipo_destinatario == FleteDestinatarioEnum.REMITENTE.value:
                obj = get_remitente_contacto_gestor_carga_by_id(db, data.id)
                if obj:
                    item = FleteRemitenteContacto(
                        flete_id=flete_id, remitente_contacto_id=obj.id
                    )
                    flete.emision_orden_remitente_destinatarios.append(item)
            elif data.tipo_destinatario == FleteDestinatarioEnum.USUARIO.value:
                obj = get_user_by_id(db, data.id)
                if obj:
                    item = FleteUserContacto(flete_id=flete_id, user_contacto_id=obj.id)
                    flete.emision_orden_user_destinatarios.append(item)
    update_flete_destinatarios(
        flete,
        db,
        modified_by,
    )
