from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import CentroOperativo


def centro_operativo_seeds(db: Session):
    try:
        db.add(
            CentroOperativo(
                nombre="CARGILL CEDRALES",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="CEDRALES",
                latitud=-25.658948139894708,
                longitud=-54.717514329980474,
                clasificacion_id=1,
                ciudad_id=13,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="ADM SANTA RITA",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="SANTA RITA",
                latitud=-25.7917136,
                longitud=-55.08793379999997,
                clasificacion_id=2,
                ciudad_id=7,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="GICAL KM12",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="GICAL KM 12",
                latitud=-25.4921592,
                longitud=-54.72833349999996,
                clasificacion_id=3,
                ciudad_id=11,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="LA PAZ",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion=None,
                latitud=-26.991085,
                longitud=-55.89410369999996,
                clasificacion_id=4,
                ciudad_id=139,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="PUERTO TROCIUCK",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion=None,
                latitud=-27.2996615,
                longitud=-56.02708849999999,
                clasificacion_id=5,
                ciudad_id=128,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="PUERTO SAN ANTONIO",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Av. San Antonio",
                latitud=-25.428378380516225,
                longitud=-57.55939476199342,
                clasificacion_id=6,
                ciudad_id=72,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="AGROFERTIL SANTA FE",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Ciudad de Santa Fe - Alto Paraná",
                latitud=-25.2215574,
                longitud=-54.70587929999999,
                clasificacion_id=7,
                ciudad_id=11,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="ITAKYRY",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="ITAKYRY",
                latitud=-24.9852879,
                longitud=-55.15138009999998,
                clasificacion_id=8,
                ciudad_id=12,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="ESTANCIA YBY PORA",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion=None,
                latitud=-24.4724333,
                longitud=-55.69672809999997,
                clasificacion_id=1,
                ciudad_id=62,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="KM 28 - CARGILL SAECA",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="MINGA GUAZU KM 28",
                latitud=-25.4838585,
                longitud=-54.885111300000005,
                clasificacion_id=2,
                ciudad_id=15,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="LOS CEDRALES",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="LOS CEDRALES",
                latitud=-25.6707073,
                longitud=-54.741203600000006,
                clasificacion_id=3,
                ciudad_id=13,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="CARGILL_NUEVA TOLEDO",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Carlos A. López, Toledo",
                latitud=-24.972151,
                longitud=-55.618852100000026,
                clasificacion_id=4,
                ciudad_id=35,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="CARGILL_VAQUERIA",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Unnamed Road, Vaquería",
                latitud=-24.9959388,
                longitud=-55.821775,
                clasificacion_id=5,
                ciudad_id=35,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="CARGILL_PACURI",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Departamento de Alto Paraná",
                latitud=-25.48814618098412,
                longitud=-54.89485988242188,
                clasificacion_id=6,
                ciudad_id=14,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="PUERTO UNION",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Puerto Union, gral.",
                latitud=-25.2299182,
                longitud=-57.56955529999999,
                clasificacion_id=7,
                ciudad_id=65,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="PUERTO CAIASA",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="km 7 Ruta Villeta-Alberdi (Paraguay)",
                latitud=-25.5802638,
                longitud=-57.56614209999998,
                clasificacion_id=8,
                ciudad_id=79,
                contacto_id=None,
            )
        )
        db.add(
            CentroOperativo(
                nombre="LDC_POZUELO",
                nombre_corto=None,
                logo=None,
                es_moderado=True,
                direccion="Canindeyú, Paraguay",
                latitud=-24.57650659999999,
                longitud=-54.34180070000002,
                clasificacion_id=1,
                ciudad_id=63,
                contacto_id=None,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
