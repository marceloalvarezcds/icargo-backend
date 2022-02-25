from datetime import date, datetime

from simplejson import dumps
from sqlalchemy import inspect  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from .audit_database import AuditDatabase
from .audit_mixin import AuditMixin


def get(value):
    if isinstance(value, list):
        return value[0]
    return value


def serialize_value(value):
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    else:
        return value


def get_json(data) -> str:
    target = dict(data.__dict__)
    del target["_sa_instance_state"]
    row = dict(target)
    for key, value in target.items():
        if isinstance(value, AuditMixin):
            del row[key]
        else:
            row[key] = serialize_value(value)
    return dumps(row, skipkeys=True, iterable_as_array=True, for_json=True)


def save_audit_database(db_conn, id, table_name, action, modified_by, row):
    db = Session(bind=db_conn)
    db_audit = AuditDatabase(
        row_id=id,
        table_name=table_name,
        action=action,
        user=modified_by,
        row=row,
    )
    db.add(db_audit)
    db.commit()


def create_audit_database(db_conn, target, action):
    save_audit_database(
        db_conn,
        target.id,
        target.__tablename__,
        action,
        target.modified_by,
        get_json(target),
    )


def create_audit_database_for_update(db_conn, target):
    state = inspect(target)
    changes = {}
    for attr in state.attrs:
        key = attr.key
        hist = attr.load_history()
        value = hist.added
        if (
            not hist.has_changes()
            or isinstance(value, AuditMixin)
            or key == "modified_by"
            or key == "modified_at"
        ):
            continue
        if key not in changes:
            changes[key] = {}
        changes[key]["old"] = serialize_value(get(hist.deleted))
        changes[key]["new"] = serialize_value(get(value))
    save_audit_database(
        db_conn,
        target.id,
        target.__tablename__,
        "update",
        target.modified_by,
        dumps(changes, skipkeys=True, iterable_as_array=True, for_json=True),
    )
