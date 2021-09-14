# from app.database import SessionLocal  # type: ignore
from app.logger import logger


def init() -> None:
    pass
    # db = SessionLocal()
    # init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
