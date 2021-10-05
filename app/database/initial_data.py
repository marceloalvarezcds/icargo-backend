from sqlalchemy.orm import Session  # type: ignore

from app.config import ENV
from app.database.populate import populate
from app.database.seeds import seeds
from app.dependencies.database_connection import get_database_connection
from app.logger import logger


def init() -> None:
    db = Session(bind=get_database_connection())
    seeds(db)
    if ENV == "development":
        populate(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
