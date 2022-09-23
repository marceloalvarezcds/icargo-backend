from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum


class TransactionalUserBaseModel(BaseModel):
    numero_documento: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    punto_venta_id: Optional[int] = None


class TransactionalUserCreateForm(TransactionalUserBaseModel):
    is_activated: Optional[bool] = None

    def dict(self, exclude_none: bool = True, **kargs):
        self.is_activated = None
        return super().dict(exclude_none=exclude_none, **kargs)


class TransactionalUserEditForm(TransactionalUserCreateForm):
    estado: Optional[str] = None
    pin: Optional[str] = None

    def dict(self, **kargs):
        self.estado = (
            EstadoEnum.ACTIVO.value if self.is_activated else EstadoEnum.INACTIVO.value
        )
        return super().dict(**kargs)


class TransactionalUser(TransactionalUserBaseModel):
    id: int
    is_activated: bool

    class Config:
        orm_mode = True
