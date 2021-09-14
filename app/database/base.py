from typing import Any

from sqlalchemy.ext.declarative import declarative_base, declared_attr  # type: ignore

from app.utils import camel_to_snake


class CustomBase:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)


Base = declarative_base(cls=CustomBase)
