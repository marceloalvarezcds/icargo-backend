from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.database.seeds.ciudad_seeds import ciudad_brasil_seeds
from app.models import Localidad, Pais


def localidad_brasil_seeds(db: Session, brasil: Pais):
    try:
        acre = Localidad(nombre="Acre", pais_id=brasil.id)
        alagoas = Localidad(nombre="Alagoas", pais_id=brasil.id)
        amapa = Localidad(nombre="Amapá", pais_id=brasil.id)
        amazonas = Localidad(nombre="Amazonas", pais_id=brasil.id)
        bahia = Localidad(nombre="Bahia", pais_id=brasil.id)
        ceara = Localidad(nombre="Ceará", pais_id=brasil.id)
        distrito_federal = Localidad(nombre="Distrito Federal", pais_id=brasil.id)
        espirito_santo = Localidad(nombre="Espírito Santo", pais_id=brasil.id)
        goias = Localidad(nombre="Goiás", pais_id=brasil.id)
        maranhao = Localidad(nombre="Maranhão", pais_id=brasil.id)
        mato_grosso_do_sul = Localidad(nombre="Mato Grosso do Sul", pais_id=brasil.id)
        mato_grosso = Localidad(nombre="Mato Grosso", pais_id=brasil.id)
        minas_gerais = Localidad(nombre="Minas Gerais", pais_id=brasil.id)
        para = Localidad(nombre="Pará", pais_id=brasil.id)
        paraiba = Localidad(nombre="Paraíba", pais_id=brasil.id)
        parana = Localidad(nombre="Paraná", pais_id=brasil.id)
        pernambuco = Localidad(nombre="Pernambuco", pais_id=brasil.id)
        piaui = Localidad(nombre="Piauí", pais_id=brasil.id)
        rio_de_janeiro = Localidad(nombre="Rio de Janeiro", pais_id=brasil.id)
        rio_grande_do_norte = Localidad(nombre="Rio Grande do Norte", pais_id=brasil.id)
        rio_grande_do_sul = Localidad(nombre="Rio Grande do Sul", pais_id=brasil.id)
        rondonia = Localidad(nombre="Rondônia", pais_id=brasil.id)
        roraima = Localidad(nombre="Roraima", pais_id=brasil.id)
        sao_paulo = Localidad(nombre="São Paulo", pais_id=brasil.id)
        santa_catarina = Localidad(nombre="Santa Catarina", pais_id=brasil.id)
        sergipe = Localidad(nombre="Sergipe", pais_id=brasil.id)
        tocantins = Localidad(nombre="Tocantins", pais_id=brasil.id)
        db.add(acre)
        db.add(alagoas)
        db.add(amapa)
        db.add(amazonas)
        db.add(bahia)
        db.add(ceara)
        db.add(distrito_federal)
        db.add(espirito_santo)
        db.add(goias)
        db.add(maranhao)
        db.add(mato_grosso_do_sul)
        db.add(mato_grosso)
        db.add(minas_gerais)
        db.add(para)
        db.add(paraiba)
        db.add(parana)
        db.add(pernambuco)
        db.add(piaui)
        db.add(rio_de_janeiro)
        db.add(rio_grande_do_norte)
        db.add(rio_grande_do_sul)
        db.add(rondonia)
        db.add(roraima)
        db.add(sao_paulo)
        db.add(santa_catarina)
        db.add(sergipe)
        db.add(tocantins)
        db.commit()
        ciudad_brasil_seeds(
            db,
            acre,
            alagoas,
            amapa,
            amazonas,
            bahia,
            ceara,
            distrito_federal,
            espirito_santo,
            goias,
            maranhao,
            mato_grosso_do_sul,
            mato_grosso,
            minas_gerais,
            para,
            paraiba,
            parana,
            pernambuco,
            piaui,
            rio_de_janeiro,
            rio_grande_do_norte,
            rio_grande_do_sul,
            rondonia,
            roraima,
            sao_paulo,
            santa_catarina,
            sergipe,
            tocantins,
        )
    except IntegrityError:
        db.rollback()
