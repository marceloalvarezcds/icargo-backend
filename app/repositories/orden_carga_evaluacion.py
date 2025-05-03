from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaEvaluacionesHistorial
from app.models.camion import Camion
from app.models.chofer import Chofer
from app.models.propietario import Propietario
from app.models.semi import Semi
from app.schemas import OrdenCargaEvaluacionesHistorialForm
from sqlalchemy import func


def get_evaluacion_list(db: Session) -> List[OrdenCargaEvaluacionesHistorial]:
    return (
        db.query(OrdenCargaEvaluacionesHistorial)
        .order_by(OrdenCargaEvaluacionesHistorial.id.desc())
        .all()
    )

def get_orden_carga_evaluaciones_historial_by_id(db: Session, id: int):
    return db.query(OrdenCargaEvaluacionesHistorial).filter(OrdenCargaEvaluacionesHistorial.id == id).first()


def calcular_promedios(db: Session, gestor_carga_id: int = None):
    query = db.query(
        func.avg(OrdenCargaEvaluacionesHistorial.tracto_rating).label("tracto"),
        func.avg(OrdenCargaEvaluacionesHistorial.semi_rating).label("semi"),
        func.avg(OrdenCargaEvaluacionesHistorial.chofer_rating).label("chofer"),
        func.avg(OrdenCargaEvaluacionesHistorial.propietario_rating).label("propietario"),
        func.avg(OrdenCargaEvaluacionesHistorial.carga_rating).label("carga"),
        func.avg(OrdenCargaEvaluacionesHistorial.descarga_rating).label("descarga"),
    )

    if gestor_carga_id is not None:
        query = query.filter(OrdenCargaEvaluacionesHistorial.gestor_carga_id == gestor_carga_id)

    resultados = query.one()

    # Redondear a 1 decimal
    return {k: round(v, 1) if v is not None else None for k, v in resultados._asdict().items()}


def calcular_promedios_generales(db: Session):
    query = db.query(
        func.avg(OrdenCargaEvaluacionesHistorial.tracto_rating).label("tracto"),
        func.avg(OrdenCargaEvaluacionesHistorial.semi_rating).label("semi"),
        func.avg(OrdenCargaEvaluacionesHistorial.chofer_rating).label("chofer"),
        func.avg(OrdenCargaEvaluacionesHistorial.propietario_rating).label("propietario"),
        func.avg(OrdenCargaEvaluacionesHistorial.carga_rating).label("carga"),
        func.avg(OrdenCargaEvaluacionesHistorial.descarga_rating).label("descarga"),
    )

    # Ejecutar la consulta sin filtro por gestor_carga_id
    resultados = query.one()

    # Redondear a 1 decimal
    return {k: round(v, 1) if v is not None else None for k, v in resultados._asdict().items()}


def contar_calificaciones_generales(db: Session, columna_id, valor_id):
    return db.query(func.count()).filter(columna_id == valor_id).scalar()


def contar_calificaciones_por_gestor(db: Session, columna_id, valor_id, gestor_carga_id):
    return (
        db.query(func.count())
        .filter(columna_id == valor_id)
        .filter(OrdenCargaEvaluacionesHistorial.gestor_carga_id == gestor_carga_id)
        .scalar()
    )


#fix en algun momento, es muy largo
def create_orden_carga_evaluacion(
    db: Session,
    data: OrdenCargaEvaluacionesHistorialForm,
    modified_by: str,
) -> OrdenCargaEvaluacionesHistorial:
    # Crear la nueva evaluación
    obj = OrdenCargaEvaluacionesHistorial(
        orden_carga_id=data.orden_carga_id,
        comentarios=data.comentarios,
        tipo_incidente_id=data.tipo_incidente_id,
        gestor_carga_id=data.gestor_carga_id,
        camion_id=data.camion_id,
        semi_id=data.semi_id,
        propietario_id=data.propietario_id,
        chofer_id=data.chofer_id,
        nota=data.nota,
        concepto=data.concepto,
        origen_id=data.origen_id,
        destino_id=data.destino_id,
        producto_id=data.producto_id,
        tracto_rating=data.tracto_rating,
        semi_rating=data.semi_rating,
        chofer_rating=data.chofer_rating,
        propietario_rating=data.propietario_rating,
        carga_rating=data.carga_rating,
        descarga_rating=data.descarga_rating,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # Calcular promedios generales
    promedios_generales = calcular_promedios_generales(db)

    obj.promedio_carga_general = promedios_generales["carga"]
    obj.promedio_descarga_general = promedios_generales["descarga"]
    promedios_por_gestor_carga = calcular_promedios(db, data.gestor_carga_id)
    obj.promedio_carga_gestor = promedios_por_gestor_carga["carga"]

    promedios_por_gestor_descarga = calcular_promedios(db, data.gestor_carga_id)
    obj.promedio_descarga_gestor = promedios_por_gestor_descarga["descarga"]
    # CAMIÓN
    if data.camion_id:
        camion = db.query(Camion).filter(Camion.id == data.camion_id).one()
        # General
        camion.promedio_tracto_general = promedios_generales["tracto"]
        camion.cantidad_tracto_evaluaciones = contar_calificaciones_generales(
            db, OrdenCargaEvaluacionesHistorial.camion_id, data.camion_id
        )
        # Por gestor
        promedios_por_gestor_camion = calcular_promedios(db, data.gestor_carga_id)
        camion.promedio_tracto_gestor = promedios_por_gestor_camion["tracto"]
        camion.cantidad_tracto_evaluaciones_gestor = contar_calificaciones_por_gestor(
            db, OrdenCargaEvaluacionesHistorial.camion_id, data.camion_id,
            data.gestor_carga_id
        )
        # Guardar en la tabla OrdenCargaEvaluacionesHistorial
        obj.promedio_tracto_general = promedios_generales["tracto"]
        obj.promedio_tracto_gestor = promedios_por_gestor_camion["tracto"]
    # SEMI
    if data.semi_id:
        semi = db.query(Semi).filter(Semi.id == data.semi_id).one()

        semi.promedio_semi_general = promedios_generales["semi"]
        semi.cantidad_semi_evaluaciones = contar_calificaciones_generales(
            db, OrdenCargaEvaluacionesHistorial.semi_id, data.semi_id
        )
        # Por gestor
        promedios_por_gestor_semi = calcular_promedios(db, data.gestor_carga_id)
        semi.promedio_semi_gestor = promedios_por_gestor_semi["semi"]
        semi.cantidad_semi_evaluaciones_gestor = contar_calificaciones_por_gestor(
            db, OrdenCargaEvaluacionesHistorial.semi_id, data.semi_id,
            data.gestor_carga_id
        )
        # Guardar en la tabla OrdenCargaEvaluacionesHistorial
        obj.promedio_semi_general = promedios_generales["semi"]
        obj.promedio_semi_gestor = promedios_por_gestor_semi["semi"]

    # CHOFER
    if data.chofer_id:
        chofer = db.query(Chofer).filter(Chofer.id == data.chofer_id).one()

        chofer.promedio_chofer_general = promedios_generales["chofer"]
        chofer.cantidad_chofer_evaluaciones = contar_calificaciones_generales(
            db, OrdenCargaEvaluacionesHistorial.chofer_id, data.chofer_id
        )
        # Por gestor
        promedios_por_gestor_chofer = calcular_promedios(db, data.gestor_carga_id)
        chofer.promedio_chofer_gestor = promedios_por_gestor_chofer["chofer"]
        chofer.cantidad_chofer_evaluaciones_gestor = contar_calificaciones_por_gestor(
            db, OrdenCargaEvaluacionesHistorial.chofer_id, data.chofer_id,
            data.gestor_carga_id
        )
        # Guardar en la tabla OrdenCargaEvaluacionesHistorial
        obj.promedio_chofer_general = promedios_generales["chofer"]
        obj.promedio_chofer_gestor = promedios_por_gestor_chofer["chofer"]

    # PROPIETARIO
    if data.propietario_id:
        propietario = db.query(Propietario).filter(Propietario.id == data.propietario_id).one()

        propietario.promedio_propietario_general = promedios_generales["propietario"]
        propietario.cantidad_propietario_evaluaciones = contar_calificaciones_generales(
            db, OrdenCargaEvaluacionesHistorial.propietario_id, data.propietario_id
        )

        # Por gestor
        promedios_por_gestor_propietario = calcular_promedios(db, data.gestor_carga_id)
        propietario.promedio_propietario_gestor = promedios_por_gestor_propietario["propietario"]
        propietario.cantidad_propietario_evaluaciones_gestor = contar_calificaciones_por_gestor(
            db, OrdenCargaEvaluacionesHistorial.propietario_id, data.propietario_id,
            data.gestor_carga_id
        )
        # Guardar en la tabla OrdenCargaEvaluacionesHistorial
        obj.promedio_propietario_general = promedios_generales["propietario"]
        obj.promedio_propietario_gestor = promedios_por_gestor_propietario["propietario"]

    db.commit()
    db.refresh(obj)

    return obj




