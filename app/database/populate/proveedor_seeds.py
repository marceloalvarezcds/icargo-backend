from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import ComposicionJuridica, GestorCarga, Proveedor, TipoDocumento
from app.models.ciudad import Ciudad
from app.repositories import (
    get_cargo_by_descripcion,
    get_ciudad_by_nombre_and_localidad_id,
    get_composicion_juridica_by_nombre,
    get_contacto_by_email,
    get_localidad_by_nombre_and_pais_id,
    get_pais_by_nombre_corto,
    get_proveedor_by,
    get_tipo_documento_by_descripcion,
)

from .gestor_carga_proveedor_seeds import gestor_carga_proveedor_seeds
from .proveedor_contacto_gestor_carga_seeds import proveedor_contacto_gestor_carga_seeds
from .punto_venta_seeds import punto_venta_seeds


def proveedor_seeds(
    db: Session,
    nombre: str,
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
        obj = get_proveedor_by(db, tipo_documento.id, numero_documento)
        if not obj:
            proveedor = Proveedor(
                nombre=nombre,
                nombre_corto=None,
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
            db.add(proveedor)
            db.commit()
            gestor_carga_proveedor_seeds(db, proveedor, gestor_carga, alias)
            cargo = get_cargo_by_descripcion(db, cargo_descripcion)
            contacto = get_contacto_by_email(db, contacto_email)
            proveedor_contacto_gestor_carga_seeds(
                db, cargo, proveedor, contacto, gestor_carga, contacto_alias
            )
            punto_venta_seeds(
                db,
                nombre=nombre,
                proveedor_id=proveedor.id,
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                digito_verificador=digito_verificador,
                composicion_juridica=composicion_juridica,
                telefono=telefono,
                email=email,
                pagina_web=pagina_web,
                direccion=direccion,
                latitud=latitud,
                longitud=longitud,
                alias=alias,
                cargo_descripcion=cargo_descripcion,
                contacto_email=contacto_email,
                contacto_alias=contacto_alias,
                gestor_carga=gestor_carga,
                ciudad=ciudad,
            )


def cargill_proveedor_seeds(db: Session, gestor_carga: GestorCarga):
    sociedad_anonima = get_composicion_juridica_by_nombre(db, "Sociedad Anónima")
    sociedad_cooperativa = get_composicion_juridica_by_nombre(
        db, "Sociedad Cooperativa"
    )
    sociedad_responsabilidad_limitada = get_composicion_juridica_by_nombre(
        db, "Sociedad de Responsabilidad Limitada"
    )
    uni_personal = get_composicion_juridica_by_nombre(db, "Uni-personal")

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

    proveedor_seeds(
        db,
        nombre="CARGILL CEDRALES",
        tipo_documento=cedula,
        numero_documento="3500500",
        digito_verificador=None,
        composicion_juridica=sociedad_anonima,
        telefono="0982444444",
        email="contacto@cargill-cedrales.com",
        pagina_web="cargill-cedrales.com",
        direccion="CEDRALES",
        latitud=-25.658948139894708,
        longitud=-54.717514329980474,
        alias="Cedrales",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_carga=gestor_carga,
        ciudad=los_cedrales,
    )
    proveedor_seeds(
        db,
        nombre="KM 28 - CARGILL SAECA",
        tipo_documento=pasaporte,
        numero_documento="p-500500",
        digito_verificador=None,
        composicion_juridica=sociedad_cooperativa,
        telefono="0982555555",
        email="contacto@km-28-cargill-saeca.com",
        pagina_web="km-28-cargill-saeca.com",
        direccion="MINGA GUAZU KM 28",
        latitud=-25.4838585,
        longitud=-54.885111300000005,
        alias="Cargill",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=minga_guazu,
    )
    proveedor_seeds(
        db,
        nombre="CARGILL_NUEVA TOLEDO",
        tipo_documento=ruc,
        numero_documento="800500500",
        digito_verificador="1",
        composicion_juridica=sociedad_responsabilidad_limitada,
        telefono="0982666666",
        email="contacto@cargill-nueva-toledo.com",
        pagina_web="cargill-nueva-toledo.com",
        direccion="Carlos A. López, Toledo",
        latitud=-24.972151,
        longitud=-55.618852100000026,
        alias="Toledo",
        cargo_descripcion="Vendedor",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=caaguazu,
    )
    proveedor_seeds(
        db,
        nombre="CARGILL_VAQUERIA",
        tipo_documento=cedula,
        numero_documento="3600600",
        digito_verificador=None,
        composicion_juridica=uni_personal,
        telefono="0982777777",
        email="contacto@cargill-vaqueria.com",
        pagina_web="cargill-vaqueria.com",
        direccion="Unnamed Road, Vaquería",
        latitud=-24.9959388,
        longitud=-55.821775,
        alias="Vaqueria",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_carga=gestor_carga,
        ciudad=asuncion,
    )
    proveedor_seeds(
        db,
        nombre="CARGILL_PACURI",
        tipo_documento=pasaporte,
        numero_documento="p-600600",
        digito_verificador=None,
        composicion_juridica=sociedad_anonima,
        telefono="0982888888",
        email="contacto@cargill-pacuri.com",
        pagina_web="cargill-pacuri.com",
        direccion="Departamento de Alto Paraná",
        latitud=-25.48814618098412,
        longitud=-54.89485988242188,
        alias="Pacuri",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_carga=gestor_carga,
        ciudad=ciudad_del_este,
    )


def multiple_proveedor_seeds(db: Session, gestor_carga: GestorCarga):
    sociedad_anonima = get_composicion_juridica_by_nombre(db, "Sociedad Anónima")
    sociedad_cooperativa = get_composicion_juridica_by_nombre(
        db, "Sociedad Cooperativa"
    )
    sociedad_responsabilidad_limitada = get_composicion_juridica_by_nombre(
        db, "Sociedad de Responsabilidad Limitada"
    )
    uni_personal = get_composicion_juridica_by_nombre(db, "Uni-personal")

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

    proveedor_seeds(
        db,
        nombre="ADM SANTA RITA",
        tipo_documento=cedula,
        numero_documento="3100100",
        digito_verificador=None,
        composicion_juridica=sociedad_anonima,
        telefono="0981111111",
        email="contacto@adm-santa-rita.com",
        pagina_web="adm-santa-rita.com",
        direccion="SANTA RITA",
        latitud=-25.7917136,
        longitud=-55.08793379999997,
        alias="Santa Rita",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_carga=gestor_carga,
        ciudad=santa_rita,
    )
    proveedor_seeds(
        db,
        nombre="GICAL KM12",
        tipo_documento=pasaporte,
        numero_documento="p-100100",
        digito_verificador=None,
        composicion_juridica=sociedad_cooperativa,
        telefono="0981222222",
        email="contacto@gical-km12.com",
        pagina_web="gical-km12.com",
        direccion="GICAL KM 12",
        latitud=-25.4921592,
        longitud=-54.72833349999996,
        alias="KM12",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_carga=gestor_carga,
        ciudad=hernandarias,
    )
    proveedor_seeds(
        db,
        nombre="LA PAZ",
        tipo_documento=ruc,
        numero_documento="800100100",
        digito_verificador="1",
        composicion_juridica=sociedad_responsabilidad_limitada,
        telefono="0981333333",
        email="contacto@la-paz.com",
        pagina_web="la-paz.com",
        direccion=None,
        latitud=-26.991085,
        longitud=-55.89410369999996,
        alias="La Paz",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_carga=gestor_carga,
        ciudad=la_paz,
    )
    proveedor_seeds(
        db,
        nombre="PUERTO TROCIUCK",
        tipo_documento=cedula,
        numero_documento="3200200",
        digito_verificador=None,
        composicion_juridica=uni_personal,
        telefono="0981444444",
        email="contacto@puerto-trociuck.com",
        pagina_web="puerto-trociuck.com",
        direccion=None,
        latitud=-27.2996615,
        longitud=-56.02708849999999,
        alias="Trociuck",
        cargo_descripcion="Gerente",
        contacto_email="maria@cardozo.com",
        contacto_alias="Maria",
        gestor_carga=gestor_carga,
        ciudad=encarnacion,
    )
    proveedor_seeds(
        db,
        nombre="PUERTO SAN ANTONIO",
        tipo_documento=pasaporte,
        numero_documento="p-200200",
        digito_verificador=None,
        composicion_juridica=sociedad_anonima,
        telefono="0981555555",
        email="contacto@puerto-san-antonio.com",
        pagina_web="puerto-san-antonio.com",
        direccion="Av. San Antonio",
        latitud=-25.428378380516225,
        longitud=-57.55939476199342,
        alias="San Antonio",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=san_antonio,
    )
    proveedor_seeds(
        db,
        nombre="AGROFERTIL SANTA FE",
        tipo_documento=ruc,
        numero_documento="800200200",
        digito_verificador="1",
        composicion_juridica=sociedad_cooperativa,
        telefono="0981666666",
        email="contacto@agrofertil-santa-fe.com",
        pagina_web="agrofertil-santa-fe.com",
        direccion="Ciudad de Santa Fe - Alto Paraná",
        latitud=-25.2215574,
        longitud=-54.70587929999999,
        alias="Santa Fe",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=hernandarias,
    )
    proveedor_seeds(
        db,
        nombre="ITAKYRY",
        tipo_documento=cedula,
        numero_documento="3300300",
        digito_verificador=None,
        composicion_juridica=sociedad_responsabilidad_limitada,
        telefono="0981777777",
        email="contacto@itakyry.com",
        pagina_web="itakyry.com",
        direccion="ITAKYRY",
        latitud=-24.9852879,
        longitud=-55.15138009999998,
        alias="Itakyry",
        cargo_descripcion="Gerente",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=itakyry,
    )
    proveedor_seeds(
        db,
        nombre="ESTANCIA YBY PORA",
        tipo_documento=pasaporte,
        numero_documento="p-300300",
        digito_verificador=None,
        composicion_juridica=uni_personal,
        telefono="0981888888",
        email="contacto@estancia-yby-pora.com",
        pagina_web="estancia-yby-pora.com",
        direccion=None,
        latitud=-24.4724333,
        longitud=-55.69672809999997,
        alias="Yby Pora",
        cargo_descripcion="Vendedor",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=san_isidro,
    )
    proveedor_seeds(
        db,
        nombre="LOS CEDRALES",
        tipo_documento=ruc,
        numero_documento="800300300",
        digito_verificador="1",
        composicion_juridica=sociedad_anonima,
        telefono="0981999999",
        email="contacto@los-cedrales.com",
        pagina_web="los-cedrales.com",
        direccion="LOS CEDRALES",
        latitud=-25.6707073,
        longitud=-54.741203600000006,
        alias="Los Cedrales",
        cargo_descripcion="Vendedor",
        contacto_email="pedro@molinas.com",
        contacto_alias="Pedro",
        gestor_carga=gestor_carga,
        ciudad=salto_del_guaira,
    )
    proveedor_seeds(
        db,
        nombre="PUERTO CAIASA",
        tipo_documento=cedula,
        numero_documento="3400400",
        digito_verificador=None,
        composicion_juridica=sociedad_cooperativa,
        telefono="0982111111",
        email="contacto@puerto-caiasa.com",
        pagina_web="puerto-caiasa.com",
        direccion="km 7 Ruta Villeta-Alberdi (Paraguay)",
        latitud=-25.5802638,
        longitud=-57.56614209999998,
        alias="Caiasa",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_carga=gestor_carga,
        ciudad=villeta,
    )
    proveedor_seeds(
        db,
        nombre="PUERTO UNION",
        tipo_documento=pasaporte,
        numero_documento="p-400400",
        digito_verificador=None,
        composicion_juridica=sociedad_responsabilidad_limitada,
        telefono="0982222222",
        email="contacto@puerto-union.com",
        pagina_web="puerto-union.com",
        direccion="Puerto Union, gral.",
        latitud=-25.2299182,
        longitud=-57.56955529999999,
        alias="Union",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_carga=gestor_carga,
        ciudad=ambato,
    )
    proveedor_seeds(
        db,
        nombre="LDC_POZUELO",
        tipo_documento=ruc,
        numero_documento="800400400",
        digito_verificador="1",
        composicion_juridica=uni_personal,
        telefono="0982333333",
        email="contacto@ldc-pozuelo.com",
        pagina_web="ldc-pozuelo.com",
        direccion="Califórnia, Brazil",
        latitud=-24.57650659999999,
        longitud=-54.34180070000002,
        alias="Pozuelo",
        cargo_descripcion="Vendedor",
        contacto_email="sonia@sanchez.com",
        contacto_alias="Sonia",
        gestor_carga=gestor_carga,
        ciudad=california,
    )
