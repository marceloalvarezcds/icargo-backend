from datetime import date
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import (
    Chofer,
    Ciudad,
    GestorCarga,
    Pais,
    TipoDocumento,
    TipoRegistro,
    User,
)
from app.repositories import (
    get_chofer_by,
    get_ciudad_by_nombre_and_localidad_id,
    get_localidad_by_nombre_and_pais_id,
    get_pais_by_nombre_corto,
    get_tipo_documento_by_descripcion,
    get_tipo_registro_by_descripcion,
    get_user_list_by_gestor_carga_id,
)

from .gestor_carga_chofer_seeds import gestor_carga_chofer_seeds


def chofer_seeds(
    db: Session,
    nombre: str,
    tipo_documento: Optional[TipoDocumento],
    pais_emisor_documento: Optional[Pais],
    numero_documento: str,
    ruc: str,
    digito_verificador: str,
    es_propietario: bool,
    ciudad_emisor_registro: Optional[Ciudad],
    tipo_registro: Optional[TipoRegistro],
    numero_registro: str,
    telefono: str,
    email: str,
    direccion: Optional[str],
    alias: str,
    gestor_cuenta: GestorCarga,
    oficial_cuenta: User,
    ciudad: Optional[Ciudad],
):
    if tipo_documento and pais_emisor_documento and numero_documento and ciudad:
        obj = get_chofer_by(
            db, tipo_documento.id, pais_emisor_documento.id, numero_documento
        )
        if not obj:
            chofer = Chofer(
                nombre=nombre,
                tipo_documento_id=tipo_documento.id,
                pais_emisor_documento_id=pais_emisor_documento.id,
                numero_documento=numero_documento,
                ruc=ruc,
                digito_verificador=digito_verificador,
                fecha_nacimiento=date(1981, 6, 1),
                gestor_cuenta_id=gestor_cuenta.id,
                oficial_cuenta_id=oficial_cuenta.id,
                es_propietario=es_propietario,
                foto_documento_frente=None,
                foto_documento_reverso=None,
                foto_perfil=None,
                # inicio registro
                ciudad_emisor_registro_id=ciudad_emisor_registro.id
                if ciudad_emisor_registro
                else None,
                tipo_registro_id=tipo_registro.id if tipo_registro else None,
                numero_registro=numero_registro,
                vencimiento_registro=date(2023, 6, 1),
                foto_registro_frente=None,
                foto_registro_reverso=None,
                # fin registro
                estado=EstadoEnum.PENDIENTE.value,
                telefono=telefono,
                email=email,
                direccion=direccion,
                ciudad_id=ciudad.id,
            )
            db.add(chofer)
            db.commit()
            gestor_carga_chofer_seeds(db, chofer, gestor_cuenta, alias)


def cargill_chofer_seeds(db: Session, gestor_cuenta: GestorCarga):
    oficial_cuenta = get_user_list_by_gestor_carga_id(db, gestor_cuenta.id)[0]

    paraguay = get_pais_by_nombre_corto(db, "PY")

    alto_parana = (
        get_localidad_by_nombre_and_pais_id(db, "Alto Parana", paraguay.id)
        if paraguay
        else None
    )
    central = (
        get_localidad_by_nombre_and_pais_id(db, "Central", paraguay.id)
        if paraguay
        else None
    )
    caaguazu_localidad = (
        get_localidad_by_nombre_and_pais_id(db, "Caaguazu", paraguay.id)
        if paraguay
        else None
    )
    los_cedrales = (
        get_ciudad_by_nombre_and_localidad_id(db, "Los Cedrales", alto_parana.id)
        if alto_parana
        else None
    )
    minga_guazu = (
        get_ciudad_by_nombre_and_localidad_id(db, "Minga Guazu", alto_parana.id)
        if alto_parana
        else None
    )
    caaguazu = (
        get_ciudad_by_nombre_and_localidad_id(db, "Caaguazu", caaguazu_localidad.id)
        if caaguazu_localidad
        else None
    )
    ciudad_del_este = (
        get_ciudad_by_nombre_and_localidad_id(db, "Ciudad del Este", alto_parana.id)
        if alto_parana
        else None
    )
    asuncion = (
        get_ciudad_by_nombre_and_localidad_id(db, "Asunción", central.id)
        if central
        else None
    )

    cedula = get_tipo_documento_by_descripcion(db, "Cédula")
    pasaporte = get_tipo_documento_by_descripcion(db, "Pasaporte")
    ruc = get_tipo_documento_by_descripcion(db, "RUC")
    carta = get_tipo_documento_by_descripcion(db, "Carta Argentina")

    profesional_a = get_tipo_registro_by_descripcion(db, "Profesional A")
    profesional_b = get_tipo_registro_by_descripcion(db, "Profesional A")

    chofer_seeds(
        db,
        nombre="Chofer Cargill 1",
        tipo_documento=cedula,
        pais_emisor_documento=paraguay,
        numero_documento="3500500",
        ruc="3500500",
        digito_verificador="1",
        es_propietario=True,
        ciudad_emisor_registro=los_cedrales,
        tipo_registro=profesional_a,
        numero_registro="3500500",
        telefono="0982444444",
        email="contacto@cargill-cedrales.com",
        direccion="CEDRALES",
        alias="Cedrales",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=los_cedrales,
    )
    chofer_seeds(
        db,
        nombre="Chofer Cargill 2",
        tipo_documento=pasaporte,
        pais_emisor_documento=paraguay,
        numero_documento="p-500500",
        ruc="p-500500",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=minga_guazu,
        tipo_registro=profesional_b,
        numero_registro="p-500500",
        telefono="0982555555",
        email="contacto@km-28-cargill-saeca.com",
        direccion="MINGA GUAZU KM 28",
        alias="Cargill",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=minga_guazu,
    )
    chofer_seeds(
        db,
        nombre="Chofer Cargill 3",
        tipo_documento=ruc,
        pais_emisor_documento=paraguay,
        numero_documento="800500500",
        ruc="800500500",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=caaguazu,
        tipo_registro=profesional_a,
        numero_registro="800500500",
        telefono="0982666666",
        email="contacto@cargill-nueva-toledo.com",
        direccion="Carlos A. López, Toledo",
        alias="Toledo",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=caaguazu,
    )
    chofer_seeds(
        db,
        nombre="Chofer Cargill 4",
        tipo_documento=carta,
        pais_emisor_documento=paraguay,
        numero_documento="3600600",
        ruc="3600600",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=asuncion,
        tipo_registro=profesional_b,
        numero_registro="3600600",
        telefono="0982777777",
        email="contacto@cargill-vaqueria.com",
        direccion="Unnamed Road, Vaquería",
        alias="Vaqueria",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=asuncion,
    )
    chofer_seeds(
        db,
        nombre="Chofer Cargill 5",
        tipo_documento=cedula,
        pais_emisor_documento=paraguay,
        numero_documento="p-600600",
        ruc="p-600600",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=ciudad_del_este,
        tipo_registro=profesional_a,
        numero_registro="p-600600",
        telefono="0982888888",
        email="contacto@cargill-pacuri.com",
        direccion="Departamento de Alto Paraná",
        alias="Pacuri",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=ciudad_del_este,
    )


def multiple_chofer_seeds(db: Session, gestor_cuenta: GestorCarga):
    oficial_cuenta = get_user_list_by_gestor_carga_id(db, gestor_cuenta.id)[0]

    paraguay = get_pais_by_nombre_corto(db, "PY")
    argentina = get_pais_by_nombre_corto(db, "AR")
    brasil = get_pais_by_nombre_corto(db, "BR")

    alto_parana = (
        get_localidad_by_nombre_and_pais_id(db, "Alto Parana", paraguay.id)
        if paraguay
        else None
    )
    itapua = (
        get_localidad_by_nombre_and_pais_id(db, "Itapua", paraguay.id)
        if paraguay
        else None
    )
    central = (
        get_localidad_by_nombre_and_pais_id(db, "Central", paraguay.id)
        if paraguay
        else None
    )
    canindeyu = (
        get_localidad_by_nombre_and_pais_id(db, "Canindeyu", paraguay.id)
        if paraguay
        else None
    )
    catamarca = (
        get_localidad_by_nombre_and_pais_id(db, "Catamarca", argentina.id)
        if argentina
        else None
    )
    parana = (
        get_localidad_by_nombre_and_pais_id(db, "Paraná", brasil.id) if brasil else None
    )
    santa_rita = (
        get_ciudad_by_nombre_and_localidad_id(db, "Santa Rita", alto_parana.id)
        if alto_parana
        else None
    )
    hernandarias = (
        get_ciudad_by_nombre_and_localidad_id(db, "Hernandarias", alto_parana.id)
        if alto_parana
        else None
    )
    la_paz = (
        get_ciudad_by_nombre_and_localidad_id(db, "La Paz", itapua.id)
        if itapua
        else None
    )
    encarnacion = (
        get_ciudad_by_nombre_and_localidad_id(db, "Encarnacion", itapua.id)
        if itapua
        else None
    )
    san_antonio = (
        get_ciudad_by_nombre_and_localidad_id(db, "San Antonio", central.id)
        if central
        else None
    )
    itakyry = (
        get_ciudad_by_nombre_and_localidad_id(db, "Itakyry", alto_parana.id)
        if alto_parana
        else None
    )
    san_isidro = (
        get_ciudad_by_nombre_and_localidad_id(
            db, "Villa San Isidro Curuguaty", canindeyu.id
        )
        if canindeyu
        else None
    )
    villeta = (
        get_ciudad_by_nombre_and_localidad_id(db, "Villeta", central.id)
        if central
        else None
    )
    salto_del_guaira = (
        get_ciudad_by_nombre_and_localidad_id(db, "Salto del Guaira", canindeyu.id)
        if canindeyu
        else None
    )
    ambato = (
        get_ciudad_by_nombre_and_localidad_id(db, "Ambato", catamarca.id)
        if catamarca
        else None
    )
    california = (
        get_ciudad_by_nombre_and_localidad_id(db, "Califórnia", parana.id)
        if parana
        else None
    )

    cedula = get_tipo_documento_by_descripcion(db, "Cédula")
    pasaporte = get_tipo_documento_by_descripcion(db, "Pasaporte")
    ruc = get_tipo_documento_by_descripcion(db, "RUC")
    carta = get_tipo_documento_by_descripcion(db, "Carta Argentina")

    profesional_a = get_tipo_registro_by_descripcion(db, "Profesional A")
    profesional_b = get_tipo_registro_by_descripcion(db, "Profesional A")

    chofer_seeds(
        db,
        nombre="Chofer Transred 1",
        tipo_documento=cedula,
        pais_emisor_documento=paraguay,
        numero_documento="3100100",
        ruc="3100100",
        digito_verificador="1",
        es_propietario=True,
        ciudad_emisor_registro=encarnacion,
        tipo_registro=profesional_a,
        numero_registro="3100100",
        telefono="0981111111",
        email="contacto@adm-santa-rita.com",
        direccion="SANTA RITA",
        alias="Santa Rita",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=santa_rita,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 2",
        tipo_documento=pasaporte,
        pais_emisor_documento=paraguay,
        numero_documento="p-100100",
        ruc="p-100100",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=hernandarias,
        tipo_registro=profesional_b,
        numero_registro="p-100100",
        telefono="0981222222",
        email="contacto@gical-km12.com",
        direccion="GICAL KM 12",
        alias="KM12",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=hernandarias,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 3",
        tipo_documento=ruc,
        pais_emisor_documento=paraguay,
        numero_documento="800100100",
        ruc="800100100",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=la_paz,
        tipo_registro=profesional_a,
        numero_registro="800100100",
        telefono="0981333333",
        email="contacto@la-paz.com",
        direccion=None,
        alias="La Paz",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=la_paz,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 4",
        tipo_documento=carta,
        pais_emisor_documento=paraguay,
        numero_documento="3200200",
        ruc="3200200",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=encarnacion,
        tipo_registro=profesional_b,
        numero_registro="3200200",
        telefono="0981444444",
        email="contacto@puerto-trociuck.com",
        direccion=None,
        alias="Trociuck",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=encarnacion,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 5",
        tipo_documento=cedula,
        pais_emisor_documento=paraguay,
        numero_documento="p-200200",
        ruc="p-200200",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=san_antonio,
        tipo_registro=profesional_a,
        numero_registro="p-200200",
        telefono="0981555555",
        email="contacto@puerto-san-antonio.com",
        direccion="Av. San Antonio",
        alias="San Antonio",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=san_antonio,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 6",
        tipo_documento=pasaporte,
        pais_emisor_documento=paraguay,
        numero_documento="800200200",
        ruc="800200200",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=hernandarias,
        tipo_registro=profesional_b,
        numero_registro="800200200",
        telefono="0981666666",
        email="contacto@agrofertil-santa-fe.com",
        direccion="Ciudad de Santa Fe - Alto Paraná",
        alias="Santa Fe",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=hernandarias,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 7",
        tipo_documento=ruc,
        pais_emisor_documento=paraguay,
        numero_documento="3300300",
        ruc="3300300",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=encarnacion,
        tipo_registro=profesional_a,
        numero_registro="3300300",
        telefono="0981777777",
        email="contacto@itakyry.com",
        direccion="ITAKYRY",
        alias="Itakyry",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=itakyry,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 8",
        tipo_documento=carta,
        pais_emisor_documento=paraguay,
        numero_documento="p-300300",
        ruc="p-300300",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=san_isidro,
        tipo_registro=profesional_b,
        numero_registro="p-300300",
        telefono="0981888888",
        email="contacto@estancia-yby-pora.com",
        direccion=None,
        alias="Yby Pora",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=san_isidro,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 9",
        tipo_documento=cedula,
        pais_emisor_documento=paraguay,
        numero_documento="800300300",
        ruc="800300300",
        digito_verificador="1",
        es_propietario=False,
        ciudad_emisor_registro=salto_del_guaira,
        tipo_registro=profesional_a,
        numero_registro="800300300",
        telefono="0981999999",
        email="contacto@los-cedrales.com",
        direccion="LOS CEDRALES",
        alias="Los Cedrales",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=salto_del_guaira,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 10",
        tipo_documento=pasaporte,
        pais_emisor_documento=paraguay,
        numero_documento="3400400",
        ruc="3400400",
        digito_verificador="2",
        es_propietario=False,
        ciudad_emisor_registro=villeta,
        tipo_registro=profesional_b,
        numero_registro="3400400",
        telefono="0982111111",
        email="contacto@puerto-caiasa.com",
        direccion="km 7 Ruta Villeta-Alberdi (Paraguay)",
        alias="Caiasa",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=villeta,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 11",
        tipo_documento=ruc,
        pais_emisor_documento=argentina,
        numero_documento="p-400400",
        ruc="p-400400",
        digito_verificador="2",
        es_propietario=False,
        ciudad_emisor_registro=ambato,
        tipo_registro=profesional_a,
        numero_registro="p-400400",
        telefono="0982222222",
        email="contacto@puerto-union.com",
        direccion="Puerto Union, gral.",
        alias="Union",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=ambato,
    )
    chofer_seeds(
        db,
        nombre="Chofer Transred 12",
        tipo_documento=carta,
        pais_emisor_documento=brasil,
        numero_documento="800400400",
        ruc="800400400",
        digito_verificador="3",
        es_propietario=False,
        ciudad_emisor_registro=california,
        tipo_registro=profesional_b,
        numero_registro="800400400",
        telefono="0982333333",
        email="contacto@ldc-pozuelo.com",
        direccion="Califórnia, Brazil",
        alias="Pozuelo",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=california,
    )
