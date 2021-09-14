from sqlalchemy.orm import Session  # type: ignore

from .audit_database import AuditDatabase


def get_json(target) -> dict:
    row = dict(target.__dict__)
    del row["_sa_instance_state"]
    return dict(row)


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
