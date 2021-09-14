from sqlalchemy import event  # type: ignore

from app.audits.audit_functions import create_audit_database

from .audit_mixin import AuditMixin


@event.listens_for(AuditMixin, "after_insert", propagate=True)
def after_insert(_, db_conn, target):
    create_audit_database(db_conn, target, action="insert")


@event.listens_for(AuditMixin, "after_update", propagate=True)
def after_update(_, db_conn, target):
    create_audit_database(db_conn, target, action="update")


@event.listens_for(AuditMixin, "before_delete", propagate=True)
def before_delete(_, db_conn, target):
    create_audit_database(db_conn, target, action="delete")
