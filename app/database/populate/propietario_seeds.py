from datetime import date
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import (
    Chofer,
    Ciudad,
    Color,
    GestorCarga,
    MarcaCamion,
    Pais,
    Propietario,
    TipoCamion,
    TipoDocumento,
    TipoPersona,
    User,
)
from app.repositories import (
    get_cargo_by_descripcion,
    get_chofer_by,
    get_ciudad_by_nombre_and_localidad_id,
    get_color_by_descripcion,
    get_contacto_by_email,
    get_localidad_by_nombre_and_pais_id,
    get_marca_camion_by_descripcion,
    get_pais_by_nombre_corto,
    get_propietario_by,
    get_tipo_camion_by_descripcion,
    get_tipo_documento_by_descripcion,
    get_tipo_persona_by_descripcion,
    get_user_list_by_gestor_carga_id,
)

from .camion_seeds import camion_seeds
from .gestor_carga_propietario_seeds import gestor_carga_propietario_seeds
from .propietario_contacto_gestor_carga_seeds import (
    propietario_contacto_gestor_carga_seeds,
)


def get_chofer_by_tipo_documento_pais_ruc(
    db: Session,
    tipo_documento: Optional[TipoDocumento],
    pais_emisor_documento: Optional[Pais],
    numero_documento: str,
) -> Optional[Chofer]:
    if tipo_documento and pais_emisor_documento and numero_documento:
        return get_chofer_by(
            db, tipo_documento.id, pais_emisor_documento.id, numero_documento
        )
    return None


def propietario_seeds(
    db: Session,
    nombre: str,
    tipo_persona: Optional[TipoPersona],
    ruc: str,
    digito_verificador: str,
    pais_origen: Optional[Pais],
    es_chofer: bool,
    telefono: str,
    email: str,
    direccion: Optional[str],
    alias: str,
    cargo_descripcion: str,
    contacto_email: str,
    contacto_alias: str,
    gestor_cuenta: GestorCarga,
    oficial_cuenta: User,
    ciudad: Optional[Ciudad],
    chofer: Optional[Chofer] = None,
    # Datos Camion y Semi
    color: Optional[Color] = None,
    # datos camion
    marca_camion: Optional[MarcaCamion] = None,
    tipo_camion: Optional[TipoCamion] = None,
):
    if tipo_persona and pais_origen and ciudad:
        obj = get_propietario_by(db, tipo_persona.id, ruc)
        if not obj:
            propietario = Propietario(
                nombre=nombre,
                tipo_persona_id=tipo_persona.id,
                ruc=ruc,
                digito_verificador=digito_verificador,
                pais_origen_id=pais_origen.id,
                es_chofer=es_chofer,
                fecha_nacimiento=date(1981, 6, 1),
                gestor_cuenta_id=gestor_cuenta.id,
                oficial_cuenta_id=oficial_cuenta.id,
                foto_documento_frente=None,
                foto_documento_reverso=None,
                foto_perfil=None,
                estado=EstadoEnum.PENDIENTE.value,
                telefono=telefono,
                email=email,
                direccion=direccion,
                ciudad_id=ciudad.id,
                chofer_id=(chofer.id if chofer else None) if es_chofer else None,
            )
            db.add(propietario)
            db.commit()
            gestor_carga_propietario_seeds(db, propietario, gestor_cuenta, alias)
            cargo = get_cargo_by_descripcion(db, cargo_descripcion)
            contacto = get_contacto_by_email(db, contacto_email)
            propietario_contacto_gestor_carga_seeds(
                db, cargo, propietario, contacto, gestor_cuenta, contacto_alias
            )
            camion_seeds(
                db,
                placa=f"1{ruc}",
                propietario=propietario,
                chofer=chofer,
                numero_chasis=f"2{ruc}",
                ciudad_habilitacion_municipal=ciudad,
                numero_habilitacion_municipal=f"3{ruc}",
                numero_habilitacion_transporte=f"4{ruc}",
                titular_habilitacion_automotor=nombre,
                marca=marca_camion,
                tipo=tipo_camion,
                color=color,
            )


def cargill_propietario_seeds(db: Session, gestor_cuenta: GestorCarga):
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

    fisica = get_tipo_persona_by_descripcion(db, "Física")
    juridica = get_tipo_persona_by_descripcion(db, "Jurídica")

    cedula = get_tipo_documento_by_descripcion(db, "Cédula")
    pasaporte = get_tipo_documento_by_descripcion(db, "Pasaporte")
    ruc = get_tipo_documento_by_descripcion(db, "RUC")
    carta = get_tipo_documento_by_descripcion(db, "Carta Argentina")

    doc1 = "3500500"
    doc2 = "p-500500"
    doc3 = "800500500"
    doc4 = "3600600"
    doc5 = "p-600600"

    chofer1 = get_chofer_by_tipo_documento_pais_ruc(db, cedula, paraguay, doc1)
    chofer2 = get_chofer_by_tipo_documento_pais_ruc(db, pasaporte, paraguay, doc2)
    chofer3 = get_chofer_by_tipo_documento_pais_ruc(db, ruc, paraguay, doc3)
    chofer4 = get_chofer_by_tipo_documento_pais_ruc(db, carta, paraguay, doc4)
    chofer5 = get_chofer_by_tipo_documento_pais_ruc(db, cedula, paraguay, doc5)

    azul = get_color_by_descripcion(db, "AZUL")
    blanco = get_color_by_descripcion(db, "BLANCO")
    gris = get_color_by_descripcion(db, "GRIS")
    negro = get_color_by_descripcion(db, "NEGRO")
    rojo = get_color_by_descripcion(db, "ROJO")

    lumavit = get_marca_camion_by_descripcion(db, "LUMAVIT")
    mercedes = get_marca_camion_by_descripcion(db, "MERCEDES BENZ")
    metalurgica = get_marca_camion_by_descripcion(db, "METALURGICA GUTIERREZ")
    phoenix = get_marca_camion_by_descripcion(db, "PHOENIX")
    scania = get_marca_camion_by_descripcion(db, "SCANIA")

    trucky = get_tipo_camion_by_descripcion(db, "Trucky")
    chasis = get_tipo_camion_by_descripcion(db, "Chasis & Acoplado")
    trucado = get_tipo_camion_by_descripcion(db, "1S.2D (trucado)")
    sencillo = get_tipo_camion_by_descripcion(db, "1S.1S (sencillo)")
    normal = get_tipo_camion_by_descripcion(db, "1S.1D (normal)")

    propietario_seeds(
        db,
        nombre="Propietario Chofer 1",
        tipo_persona=fisica,
        ruc=doc1,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=True,
        telefono="0982444444",
        email="contacto@cargill-cedrales.com",
        direccion="CEDRALES",
        alias="Cedrales",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=los_cedrales,
        chofer=chofer1,
        color=azul,
        marca_camion=lumavit,
        tipo_camion=trucky,
    )
    propietario_seeds(
        db,
        nombre="KM 28 - CARGILL SAECA",
        tipo_persona=juridica,
        ruc=doc2,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0982555555",
        email="contacto@km-28-cargill-saeca.com",
        direccion="MINGA GUAZU KM 28",
        alias="Cargill",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=minga_guazu,
        chofer=chofer2,
        color=blanco,
        marca_camion=mercedes,
        tipo_camion=chasis,
    )
    propietario_seeds(
        db,
        nombre="CARGILL_NUEVA TOLEDO",
        tipo_persona=juridica,
        ruc=doc3,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0982666666",
        email="contacto@cargill-nueva-toledo.com",
        direccion="Carlos A. López, Toledo",
        alias="Toledo",
        cargo_descripcion="Vendedor",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=caaguazu,
        chofer=chofer3,
        color=gris,
        marca_camion=metalurgica,
        tipo_camion=trucado,
    )
    propietario_seeds(
        db,
        nombre="CARGILL_VAQUERIA",
        tipo_persona=fisica,
        ruc=doc4,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0982777777",
        email="contacto@cargill-vaqueria.com",
        direccion="Unnamed Road, Vaquería",
        alias="Vaqueria",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=asuncion,
        chofer=chofer4,
        color=negro,
        marca_camion=phoenix,
        tipo_camion=sencillo,
    )
    propietario_seeds(
        db,
        nombre="CARGILL_PACURI",
        tipo_persona=juridica,
        ruc=doc5,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0982888888",
        email="contacto@cargill-pacuri.com",
        direccion="Departamento de Alto Paraná",
        alias="Pacuri",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=ciudad_del_este,
        chofer=chofer5,
        color=rojo,
        marca_camion=scania,
        tipo_camion=normal,
    )


def multiple_propietario_seeds(db: Session, gestor_cuenta: GestorCarga):
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

    fisica = get_tipo_persona_by_descripcion(db, "Física")
    juridica = get_tipo_persona_by_descripcion(db, "Jurídica")

    cedula = get_tipo_documento_by_descripcion(db, "Cédula")
    pasaporte = get_tipo_documento_by_descripcion(db, "Pasaporte")
    ruc = get_tipo_documento_by_descripcion(db, "RUC")
    carta = get_tipo_documento_by_descripcion(db, "Carta Argentina")

    doc1 = "3100100"
    doc2 = "p-100100"
    doc3 = "800100100"
    doc4 = "3200200"
    doc5 = "p-200200"
    doc6 = "800200200"
    doc7 = "3300300"
    doc8 = "p-300300"
    doc9 = "800300300"
    doc10 = "3400400"
    doc11 = "p-400400"
    doc12 = "800400400"

    chofer1 = get_chofer_by_tipo_documento_pais_ruc(db, cedula, paraguay, doc1)
    chofer2 = get_chofer_by_tipo_documento_pais_ruc(db, pasaporte, paraguay, doc2)
    chofer3 = get_chofer_by_tipo_documento_pais_ruc(db, ruc, paraguay, doc3)
    chofer4 = get_chofer_by_tipo_documento_pais_ruc(db, carta, paraguay, doc4)
    chofer5 = get_chofer_by_tipo_documento_pais_ruc(db, cedula, paraguay, doc5)
    chofer6 = get_chofer_by_tipo_documento_pais_ruc(db, pasaporte, paraguay, doc6)
    chofer7 = get_chofer_by_tipo_documento_pais_ruc(db, ruc, paraguay, doc7)
    chofer8 = get_chofer_by_tipo_documento_pais_ruc(db, carta, paraguay, doc8)
    chofer9 = get_chofer_by_tipo_documento_pais_ruc(db, cedula, paraguay, doc9)
    chofer10 = get_chofer_by_tipo_documento_pais_ruc(db, pasaporte, paraguay, doc10)
    chofer11 = get_chofer_by_tipo_documento_pais_ruc(db, ruc, argentina, doc11)
    chofer12 = get_chofer_by_tipo_documento_pais_ruc(db, carta, brasil, doc12)

    azul = get_color_by_descripcion(db, "AZUL")
    blanco = get_color_by_descripcion(db, "BLANCO")
    gris = get_color_by_descripcion(db, "GRIS")
    negro = get_color_by_descripcion(db, "NEGRO")
    rojo = get_color_by_descripcion(db, "ROJO")
    verde = get_color_by_descripcion(db, "VERDE")

    lumavit = get_marca_camion_by_descripcion(db, "LUMAVIT")
    mercedes = get_marca_camion_by_descripcion(db, "MERCEDES BENZ")
    metalurgica = get_marca_camion_by_descripcion(db, "METALURGICA GUTIERREZ")
    phoenix = get_marca_camion_by_descripcion(db, "PHOENIX")
    scania = get_marca_camion_by_descripcion(db, "SCANIA")
    tecno = get_marca_camion_by_descripcion(db, "TECNO EQUIPO")
    volvo = get_marca_camion_by_descripcion(db, "VOLVO")

    trucky = get_tipo_camion_by_descripcion(db, "Trucky")
    chasis = get_tipo_camion_by_descripcion(db, "Chasis & Acoplado")
    trucado = get_tipo_camion_by_descripcion(db, "1S.2D (trucado)")
    sencillo = get_tipo_camion_by_descripcion(db, "1S.1S (sencillo)")
    normal = get_tipo_camion_by_descripcion(db, "1S.1D (normal)")

    propietario_seeds(
        db,
        nombre="Propietario Transred 1",
        tipo_persona=fisica,
        ruc=doc1,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=True,
        telefono="0981111111",
        email="contacto@adm-santa-rita.com",
        direccion="SANTA RITA",
        alias="Santa Rita",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=santa_rita,
        chofer=chofer1,
        color=azul,
        marca_camion=lumavit,
        tipo_camion=trucky,
    )
    propietario_seeds(
        db,
        nombre="GICAL KM12",
        tipo_persona=juridica,
        ruc=doc2,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981222222",
        email="contacto@gical-km12.com",
        direccion="GICAL KM 12",
        alias="KM12",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=hernandarias,
        chofer=chofer2,
        color=blanco,
        marca_camion=mercedes,
        tipo_camion=chasis,
    )
    propietario_seeds(
        db,
        nombre="LA PAZ",
        tipo_persona=juridica,
        ruc=doc3,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981333333",
        email="contacto@la-paz.com",
        direccion=None,
        alias="La Paz",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=la_paz,
        chofer=chofer3,
        color=gris,
        marca_camion=metalurgica,
        tipo_camion=trucado,
    )
    propietario_seeds(
        db,
        nombre="PUERTO TROCIUCK",
        tipo_persona=fisica,
        ruc=doc4,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981444444",
        email="contacto@puerto-trociuck.com",
        direccion=None,
        alias="Trociuck",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=encarnacion,
        chofer=chofer4,
        color=negro,
        marca_camion=phoenix,
        tipo_camion=sencillo,
    )
    propietario_seeds(
        db,
        nombre="PUERTO SAN ANTONIO",
        tipo_persona=juridica,
        ruc=doc5,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981555555",
        email="contacto@puerto-san-antonio.com",
        direccion="Av. San Antonio",
        alias="San Antonio",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=san_antonio,
        chofer=chofer5,
        color=rojo,
        marca_camion=scania,
        tipo_camion=normal,
    )
    propietario_seeds(
        db,
        nombre="AGROFERTIL SANTA FE",
        tipo_persona=juridica,
        ruc=doc6,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981666666",
        email="contacto@agrofertil-santa-fe.com",
        direccion="Ciudad de Santa Fe - Alto Paraná",
        alias="Santa Fe",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=hernandarias,
        chofer=chofer6,
        color=verde,
        marca_camion=tecno,
        tipo_camion=trucky,
    )
    propietario_seeds(
        db,
        nombre="ITAKYRY",
        tipo_persona=fisica,
        ruc=doc7,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981777777",
        email="contacto@itakyry.com",
        direccion="ITAKYRY",
        alias="Itakyry",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=itakyry,
        chofer=chofer7,
        color=azul,
        marca_camion=volvo,
        tipo_camion=chasis,
    )
    propietario_seeds(
        db,
        nombre="ESTANCIA YBY PORA",
        tipo_persona=juridica,
        ruc=doc8,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981888888",
        email="contacto@estancia-yby-pora.com",
        direccion=None,
        alias="Yby Pora",
        cargo_descripcion="Vendedor",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=san_isidro,
        chofer=chofer8,
        color=blanco,
        marca_camion=lumavit,
        tipo_camion=trucado,
    )
    propietario_seeds(
        db,
        nombre="LOS CEDRALES",
        tipo_persona=juridica,
        ruc=doc9,
        digito_verificador="1",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0981999999",
        email="contacto@los-cedrales.com",
        direccion="LOS CEDRALES",
        alias="Los Cedrales",
        cargo_descripcion="Vendedor",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=salto_del_guaira,
        chofer=chofer9,
        color=gris,
        marca_camion=mercedes,
        tipo_camion=sencillo,
    )
    propietario_seeds(
        db,
        nombre="PUERTO CAIASA",
        tipo_persona=fisica,
        ruc=doc10,
        digito_verificador="2",
        pais_origen=paraguay,
        es_chofer=False,
        telefono="0982111111",
        email="contacto@puerto-caiasa.com",
        direccion="km 7 Ruta Villeta-Alberdi (Paraguay)",
        alias="Caiasa",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=villeta,
        chofer=chofer10,
        color=negro,
        marca_camion=metalurgica,
        tipo_camion=normal,
    )
    propietario_seeds(
        db,
        nombre="PUERTO UNION",
        tipo_persona=juridica,
        ruc=doc11,
        digito_verificador="2",
        pais_origen=argentina,
        es_chofer=False,
        telefono="0982222222",
        email="contacto@puerto-union.com",
        direccion="Puerto Union, gral.",
        alias="Union",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=ambato,
        chofer=chofer11,
        color=rojo,
        marca_camion=phoenix,
        tipo_camion=trucky,
    )
    propietario_seeds(
        db,
        nombre="LDC_POZUELO",
        tipo_persona=juridica,
        ruc=doc12,
        digito_verificador="3",
        pais_origen=brasil,
        es_chofer=False,
        telefono="0982333333",
        email="contacto@ldc-pozuelo.com",
        direccion="Califórnia, Brazil",
        alias="Pozuelo",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_cuenta=gestor_cuenta,
        oficial_cuenta=oficial_cuenta,
        ciudad=california,
        chofer=chofer12,
        color=verde,
        marca_camion=scania,
        tipo_camion=chasis,
    )
