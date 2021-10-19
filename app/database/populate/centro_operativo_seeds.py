from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import CentroOperativo, GestorCarga
from app.repositories import (
    get_cargo_by_descripcion,
    get_centro_operativo_clasificacion_by_nombre,
    get_ciudad_by_nombre_and_localidad_id,
    get_contacto_by_email,
    get_localidad_by_nombre_and_pais_id,
    get_pais_by_nombre_corto,
)

from .centro_operativo_contacto_gestor_carga_seeds import (
    centro_operativo_contacto_gestor_carga_seeds,
)
from .gestor_carga_centro_operativo_seeds import gestor_carga_centro_operativo_seeds


def centro_operativo_seeds(db: Session, gestor_carga: GestorCarga):
    try:
        silo = get_centro_operativo_clasificacion_by_nombre(db, "Silo")
        puerto_seco = get_centro_operativo_clasificacion_by_nombre(db, "Puerto seco")
        puerto_multimodal = get_centro_operativo_clasificacion_by_nombre(
            db, "Puerto multimodal"
        )
        deposito = get_centro_operativo_clasificacion_by_nombre(db, "Deposito")
        centro_distribucion = get_centro_operativo_clasificacion_by_nombre(
            db, "Centro de distribución"
        )
        campo = get_centro_operativo_clasificacion_by_nombre(db, "Campo")
        aduana = get_centro_operativo_clasificacion_by_nombre(db, "Aduana")
        acopio = get_centro_operativo_clasificacion_by_nombre(db, "Acopio")

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
        caaguazu_localidad = (
            get_localidad_by_nombre_and_pais_id(db, "Caaguazu", paraguay.id)
            if paraguay
            else None
        )
        catamarca = (
            get_localidad_by_nombre_and_pais_id(db, "Catamarca", argentina.id)
            if argentina
            else None
        )
        parana = (
            get_localidad_by_nombre_and_pais_id(db, "Paraná", brasil.id)
            if brasil
            else None
        )

        los_cedrales = (
            get_ciudad_by_nombre_and_localidad_id(db, "Los Cedrales", alto_parana.id)
            if alto_parana
            else None
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
        villeta = (
            get_ciudad_by_nombre_and_localidad_id(db, "Ambato", central.id)
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

        cedrales_co = CentroOperativo(
            nombre="CARGILL CEDRALES",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="CEDRALES",
            latitud=-25.658948139894708,
            longitud=-54.717514329980474,
            clasificacion_id=silo.id if silo else None,
            ciudad_id=los_cedrales.id if los_cedrales else None,
        )
        santa_rita_co = CentroOperativo(
            nombre="ADM SANTA RITA",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="SANTA RITA",
            latitud=-25.7917136,
            longitud=-55.08793379999997,
            clasificacion_id=puerto_seco.id if puerto_seco else None,
            ciudad_id=santa_rita.id if santa_rita else None,
        )
        km12_co = CentroOperativo(
            nombre="GICAL KM12",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="GICAL KM 12",
            latitud=-25.4921592,
            longitud=-54.72833349999996,
            clasificacion_id=puerto_multimodal.id if puerto_multimodal else None,
            ciudad_id=hernandarias.id if hernandarias else None,
        )
        la_paz_co = CentroOperativo(
            nombre="LA PAZ",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion=None,
            latitud=-26.991085,
            longitud=-55.89410369999996,
            clasificacion_id=deposito.id if deposito else None,
            ciudad_id=la_paz.id if la_paz else None,
        )
        trociuck_co = CentroOperativo(
            nombre="PUERTO TROCIUCK",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion=None,
            latitud=-27.2996615,
            longitud=-56.02708849999999,
            clasificacion_id=centro_distribucion.id if centro_distribucion else None,
            ciudad_id=encarnacion.id if encarnacion else None,
        )
        san_antonio_co = CentroOperativo(
            nombre="PUERTO SAN ANTONIO",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Av. San Antonio",
            latitud=-25.428378380516225,
            longitud=-57.55939476199342,
            clasificacion_id=campo.id if campo else None,
            ciudad_id=san_antonio.id if san_antonio else None,
        )
        santa_fe_co = CentroOperativo(
            nombre="AGROFERTIL SANTA FE",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Ciudad de Santa Fe - Alto Paraná",
            latitud=-25.2215574,
            longitud=-54.70587929999999,
            clasificacion_id=aduana.id if aduana else None,
            ciudad_id=hernandarias.id if hernandarias else None,
        )
        itakyry_co = CentroOperativo(
            nombre="ITAKYRY",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="ITAKYRY",
            latitud=-24.9852879,
            longitud=-55.15138009999998,
            clasificacion_id=acopio.id if acopio else None,
            ciudad_id=itakyry.id if itakyry else None,
        )
        yby_pora_co = CentroOperativo(
            nombre="ESTANCIA YBY PORA",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion=None,
            latitud=-24.4724333,
            longitud=-55.69672809999997,
            clasificacion_id=silo.id if silo else None,
            ciudad_id=san_isidro.id if san_isidro else None,
        )
        cargill_co = CentroOperativo(
            nombre="KM 28 - CARGILL SAECA",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="MINGA GUAZU KM 28",
            latitud=-25.4838585,
            longitud=-54.885111300000005,
            clasificacion_id=puerto_seco.id if puerto_seco else None,
            ciudad_id=minga_guazu.id if minga_guazu else None,
        )
        los_cedrales_co = CentroOperativo(
            nombre="LOS CEDRALES",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="LOS CEDRALES",
            latitud=-25.6707073,
            longitud=-54.741203600000006,
            clasificacion_id=puerto_multimodal.id if puerto_multimodal else None,
            ciudad_id=salto_del_guaira.id if salto_del_guaira else None,
        )
        toledo_co = CentroOperativo(
            nombre="CARGILL_NUEVA TOLEDO",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Carlos A. López, Toledo",
            latitud=-24.972151,
            longitud=-55.618852100000026,
            clasificacion_id=deposito.id if deposito else None,
            ciudad_id=caaguazu.id if caaguazu else None,
        )
        vaqueria_co = CentroOperativo(
            nombre="CARGILL_VAQUERIA",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Unnamed Road, Vaquería",
            latitud=-24.9959388,
            longitud=-55.821775,
            clasificacion_id=centro_distribucion.id if centro_distribucion else None,
            ciudad_id=asuncion.id if asuncion else None,
        )
        pacuri_co = CentroOperativo(
            nombre="CARGILL_PACURI",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Departamento de Alto Paraná",
            latitud=-25.48814618098412,
            longitud=-54.89485988242188,
            clasificacion_id=campo.id if campo else None,
            ciudad_id=ciudad_del_este.id if ciudad_del_este else None,
        )
        caiasa_co = CentroOperativo(
            nombre="PUERTO CAIASA",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="km 7 Ruta Villeta-Alberdi (Paraguay)",
            latitud=-25.5802638,
            longitud=-57.56614209999998,
            clasificacion_id=acopio.id if acopio else None,
            ciudad_id=villeta.id if villeta else None,
        )
        union_co = CentroOperativo(
            nombre="PUERTO UNION",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Puerto Union, gral.",
            latitud=-25.2299182,
            longitud=-57.56955529999999,
            clasificacion_id=aduana.id if aduana else None,
            ciudad_id=ambato.id if ambato else None,
        )
        pozuelo_co = CentroOperativo(
            nombre="LDC_POZUELO",
            nombre_corto=None,
            logo=None,
            estado=EstadoEnum.ACTIVO.value,
            direccion="Califórnia, Brazil",
            latitud=-24.57650659999999,
            longitud=-54.34180070000002,
            clasificacion_id=silo.id if silo else None,
            ciudad_id=california.id if california else None,
        )

        db.add(cedrales_co)
        db.add(santa_rita_co)
        db.add(km12_co)
        db.add(la_paz_co)
        db.add(trociuck_co)
        db.add(san_antonio_co)
        db.add(santa_fe_co)
        db.add(itakyry_co)
        db.add(yby_pora_co)
        db.add(cargill_co)
        db.add(los_cedrales_co)
        db.add(toledo_co)
        db.add(vaqueria_co)
        db.add(pacuri_co)
        db.add(caiasa_co)
        db.add(union_co)
        db.add(pozuelo_co)
        db.commit()

        gestor_carga_centro_operativo_seeds(db, cedrales_co, gestor_carga, "Cedrales")
        gestor_carga_centro_operativo_seeds(
            db, santa_rita_co, gestor_carga, "Santa Rita"
        )
        gestor_carga_centro_operativo_seeds(db, km12_co, gestor_carga, "KM12")
        gestor_carga_centro_operativo_seeds(db, la_paz_co, gestor_carga, "La Paz")
        gestor_carga_centro_operativo_seeds(db, trociuck_co, gestor_carga, "Trociuck")
        gestor_carga_centro_operativo_seeds(
            db, san_antonio_co, gestor_carga, "San Antonio"
        )
        gestor_carga_centro_operativo_seeds(db, santa_fe_co, gestor_carga, "Santa Fe")
        gestor_carga_centro_operativo_seeds(db, itakyry_co, gestor_carga, "Itakyry")
        gestor_carga_centro_operativo_seeds(db, yby_pora_co, gestor_carga, "Yby Pora")
        gestor_carga_centro_operativo_seeds(db, cargill_co, gestor_carga, "Cargill")
        gestor_carga_centro_operativo_seeds(
            db, los_cedrales_co, gestor_carga, "Los Cedrales"
        )
        gestor_carga_centro_operativo_seeds(db, toledo_co, gestor_carga, "Toledo")
        gestor_carga_centro_operativo_seeds(db, vaqueria_co, gestor_carga, "Vaqueria")
        gestor_carga_centro_operativo_seeds(db, pacuri_co, gestor_carga, "Pacuri")
        gestor_carga_centro_operativo_seeds(db, caiasa_co, gestor_carga, "Caiasa")
        gestor_carga_centro_operativo_seeds(db, union_co, gestor_carga, "Union")
        gestor_carga_centro_operativo_seeds(db, pozuelo_co, gestor_carga, "Pozuelo")

        cargo_gerente = get_cargo_by_descripcion(db, "Gerente")
        cargo_vendedor = get_cargo_by_descripcion(db, "Vendedor")

        contacto1 = get_contacto_by_email(db, "maria@cardozo.com")
        contacto2 = get_contacto_by_email(db, "pedro@molinas.com")
        contacto3 = get_contacto_by_email(db, "sonia@sanchez.com")

        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, cedrales_co, contacto1, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, santa_rita_co, contacto1, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, km12_co, contacto1, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, la_paz_co, contacto1, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, trociuck_co, contacto1, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, san_antonio_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, santa_fe_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_gerente, itakyry_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, yby_pora_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, cargill_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, los_cedrales_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, toledo_co, contacto2, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, vaqueria_co, contacto3, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, pacuri_co, contacto3, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, caiasa_co, contacto3, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, union_co, contacto3, gestor_carga
        )
        centro_operativo_contacto_gestor_carga_seeds(
            db, cargo_vendedor, pozuelo_co, contacto3, gestor_carga
        )
    except IntegrityError:
        db.rollback()
