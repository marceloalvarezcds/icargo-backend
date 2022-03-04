from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.repositories import get_caja_by_id, get_moneda_by_simbolo

from .banco_seeds import banco_seeds
from .caja_seeds import caja_seeds


def estado_cuenta_seeds(db: Session, gestor_carga_id: Optional[int]):
    caja = get_caja_by_id(db, 1)
    if not caja:
        modified_by = "System"

        pyg = get_moneda_by_simbolo(db, "PYG")
        usd = get_moneda_by_simbolo(db, "USD")
        brl = get_moneda_by_simbolo(db, "BRL")
        arp = get_moneda_by_simbolo(db, "ARP")
        bop = get_moneda_by_simbolo(db, "BOP")

        banco_seeds(
            db, "10101010", "Titular 1", "Itaú", pyg, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "20202020", "Titular 2", "Itaú", pyg, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "30303030", "Titular 3", "Itaú", usd, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "40404040", "Titular 4", "Itaú", brl, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "50505050", "Titular 5", "Itaú", arp, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "60606060", "Titular 6", "Itaú", bop, gestor_carga_id, modified_by
        )

        banco_seeds(
            db, "70707070", "Titular 7", "BBVA", pyg, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "80808080", "Titular 8", "BBVA", pyg, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "90909090", "Titular 9", "BBVA", usd, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "11011011", "Titular 10", "BBVA", brl, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "11101110", "Titular 11", "BBVA", arp, gestor_carga_id, modified_by
        )
        banco_seeds(
            db, "11211211", "Titular 12", "BBVA", bop, gestor_carga_id, modified_by
        )

        caja_seeds(db, "CajaX", pyg, gestor_carga_id, modified_by)
        caja_seeds(db, "Caja en Guaranies", pyg, gestor_carga_id, modified_by)
        caja_seeds(db, "Caja en Dolares", usd, gestor_carga_id, modified_by)
        caja_seeds(db, "Caja en Reales", brl, gestor_carga_id, modified_by)
        caja_seeds(db, "Caja en Peso Arg", arp, gestor_carga_id, modified_by)
        caja_seeds(db, "Caja en Boliviano", bop, gestor_carga_id, modified_by)
