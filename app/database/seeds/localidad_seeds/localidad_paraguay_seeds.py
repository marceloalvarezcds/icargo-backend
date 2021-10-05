from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.database.seeds.ciudad_seeds import ciudad_paraguay_seeds
from app.models import Localidad, Pais


def localidad_paraguay_seeds(db: Session, paraguay: Pais):
    try:
        alto_paraguay = Localidad(nombre="Alto Paraguay", pais_id=paraguay.id)
        alto_parana = Localidad(nombre="Alto Parana", pais_id=paraguay.id)
        amambay = Localidad(nombre="Amambay", pais_id=paraguay.id)
        boqueron = Localidad(nombre="Boqueron", pais_id=paraguay.id)
        caaguazu = Localidad(nombre="Caaguazu", pais_id=paraguay.id)
        caazapa = Localidad(nombre="Caazapa", pais_id=paraguay.id)
        canindeyu = Localidad(nombre="Canindeyu", pais_id=paraguay.id)
        central = Localidad(nombre="Central", pais_id=paraguay.id)
        concepcion = Localidad(nombre="Concepción", pais_id=paraguay.id)
        cordillera = Localidad(nombre="Cordillera", pais_id=paraguay.id)
        guaira = Localidad(nombre="Guaira", pais_id=paraguay.id)
        itapua = Localidad(nombre="Itapua", pais_id=paraguay.id)
        misiones = Localidad(nombre="Misiones", pais_id=paraguay.id)
        neembucu = Localidad(nombre="Ñeembucu", pais_id=paraguay.id)
        paraguari = Localidad(nombre="Paraguari", pais_id=paraguay.id)
        presidente_hayes = Localidad(nombre="Presidente Hayes", pais_id=paraguay.id)
        san_pedro = Localidad(nombre="San Pedro", pais_id=paraguay.id)
        db.add(alto_paraguay)
        db.add(alto_parana)
        db.add(amambay)
        db.add(boqueron)
        db.add(caaguazu)
        db.add(caazapa)
        db.add(canindeyu)
        db.add(central)
        db.add(concepcion)
        db.add(cordillera)
        db.add(guaira)
        db.add(itapua)
        db.add(misiones)
        db.add(neembucu)
        db.add(paraguari)
        db.add(presidente_hayes)
        db.add(san_pedro)
        db.commit()
        ciudad_paraguay_seeds(
            db,
            alto_paraguay,
            alto_parana,
            amambay,
            boqueron,
            caaguazu,
            caazapa,
            canindeyu,
            central,
            concepcion,
            cordillera,
            guaira,
            itapua,
            misiones,
            neembucu,
            paraguari,
            presidente_hayes,
            san_pedro,
        )
    except IntegrityError:
        db.rollback()
