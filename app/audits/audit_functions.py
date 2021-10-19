from datetime import date, datetime

from simplejson import dumps
from sqlalchemy.orm import Session  # type: ignore

from .audit_database import AuditDatabase
from .audit_mixin import AuditMixin


def get_json(target) -> str:
    target = dict(target.__dict__)
    del target["_sa_instance_state"]
    row = dict(target)
    for key, value in target.items():
        if isinstance(value, datetime) or isinstance(value, date):
            row[key] = value.isoformat()
        elif isinstance(value, AuditMixin):
            del row[key]
        else:
            row[key] = value
    return dumps(row, skipkeys=True, iterable_as_array=True, for_json=True)


def create_audit_database(db_conn, target, action):
    db = Session(bind=db_conn)
    db_audit = AuditDatabase(
        row_id=target.id,
        table_name=target.__tablename__,
        action=action,
        user=target.modified_by,
        row=get_json(target),
    )
    db.add(db_audit)
    db.commit()
