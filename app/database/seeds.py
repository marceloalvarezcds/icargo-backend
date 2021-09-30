from sqlalchemy.orm import Session  # type: ignore

from app.models import User
from app.repositories import user


def seeds(db: Session):
    admin_username = "admin-icargo"
    admin_user = user.get_by_username(db, admin_username)
    if admin_user is None:
        admin_user = User(
            token="",
            first_name="Icargo",
            last_name="Admin",
            username=admin_username,
            surname=admin_username,
            email="admin@icargo.com",
            is_activated=True,
            is_guest=False,
            is_superuser=True,
            password="1c4rg0",
            modified_by="system",
        )
    db.add(admin_user)
    db.commit()
