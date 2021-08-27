from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# local values
DATABASE_URL="localhost"
DATABASE_USER="postgres"
DATABASE_PW="postgres"
DATABASE_DB="postgresql"
DATABASE_DRIVER="postgresql"
DATABASE_NAME="icargo"

# Docker values
""" DATABASE_URL="db"
DATABASE_USER="icargo"
DATABASE_PW="UltraSecurePass"
DATABASE_DB="postgresql"
DATABASE_DRIVER="postgresql"
DATABASE_NAME="icargo" """


SQLALCHEMY_DATABASE_URL = f'{DATABASE_DB}://{DATABASE_USER}:{DATABASE_PW}@{DATABASE_URL}/{DATABASE_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()