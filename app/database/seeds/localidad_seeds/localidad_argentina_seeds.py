from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.database.seeds.ciudad_seeds import ciudad_argentina_seeds
from app.models import Localidad, Pais


def localidad_argentina_seeds(db: Session, argentina: Pais):
    try:
        buenos_aires = Localidad(nombre="Buenos Aires", pais_id=argentina.id)
        catamarca = Localidad(nombre="Catamarca", pais_id=argentina.id)
        chaco = Localidad(nombre="Chaco", pais_id=argentina.id)
        chubut = Localidad(nombre="Chubut", pais_id=argentina.id)
        cordoba = Localidad(nombre="Córdoba", pais_id=argentina.id)
        corrientes = Localidad(nombre="Corrientes", pais_id=argentina.id)
        entre_rios = Localidad(nombre="Entre Ríos", pais_id=argentina.id)
        formosa = Localidad(nombre="Formosa", pais_id=argentina.id)
        jujuy = Localidad(nombre="Jujuy", pais_id=argentina.id)
        la_pampa = Localidad(nombre="La Pampa", pais_id=argentina.id)
        la_rioja = Localidad(nombre="La Rioja", pais_id=argentina.id)
        mendoza = Localidad(nombre="Mendoza", pais_id=argentina.id)
        misiones = Localidad(nombre="Misiones", pais_id=argentina.id)
        neuquen = Localidad(nombre="Neuquén", pais_id=argentina.id)
        rio_negro = Localidad(nombre="Río Negro", pais_id=argentina.id)
        salta = Localidad(nombre="Salta", pais_id=argentina.id)
        san_juan = Localidad(nombre="San Juan", pais_id=argentina.id)
        san_luis = Localidad(nombre="San Luis", pais_id=argentina.id)
        santa_cruz = Localidad(nombre="Santa Cruz", pais_id=argentina.id)
        santa_fe = Localidad(nombre="Santa Fe", pais_id=argentina.id)
        santiago_del_estero = Localidad(
            nombre="Santiago del Estero", pais_id=argentina.id
        )
        tierra_del_fuego = Localidad(nombre="Tierra del Fuego", pais_id=argentina.id)
        tucuman = Localidad(nombre="Tucumán", pais_id=argentina.id)
        db.add(buenos_aires)
        db.add(catamarca)
        db.add(chaco)
        db.add(chubut)
        db.add(cordoba)
        db.add(corrientes)
        db.add(entre_rios)
        db.add(formosa)
        db.add(jujuy)
        db.add(la_pampa)
        db.add(la_rioja)
        db.add(mendoza)
        db.add(misiones)
        db.add(neuquen)
        db.add(rio_negro)
        db.add(salta)
        db.add(san_juan)
        db.add(san_luis)
        db.add(santa_cruz)
        db.add(santa_fe)
        db.add(santiago_del_estero)
        db.add(tierra_del_fuego)
        db.add(tucuman)
        db.commit()
        ciudad_argentina_seeds(
            db,
            buenos_aires,
            catamarca,
            chaco,
            chubut,
            cordoba,
            corrientes,
            entre_rios,
            formosa,
            jujuy,
            la_pampa,
            la_rioja,
            mendoza,
            misiones,
            neuquen,
            rio_negro,
            salta,
            san_juan,
            san_luis,
            santa_cruz,
            santa_fe,
            santiago_del_estero,
            tierra_del_fuego,
            tucuman,
        )
    except IntegrityError:
        db.rollback()
