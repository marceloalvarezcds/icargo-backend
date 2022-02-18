from datetime import datetime
from typing import List

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import BooleanClauseList, and_, or_  # type: ignore

from app.audits.audit_database import AuditDatabase

now = datetime.now()


def get_audit_list_by_table_filter_data_and_daterange(
    db: Session,
    conditions: BooleanClauseList,
    start_date: datetime,
    end_date: datetime = now,
) -> List[AuditDatabase]:
    start = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end = end_date.strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(AuditDatabase)
        .filter(
            and_(
                or_(*conditions),
                AuditDatabase.date_hour >= start,
                AuditDatabase.date_hour <= end,
            )
        )
        .order_by(
            AuditDatabase.date_hour, AuditDatabase.table_name, AuditDatabase.action
        )
        .all()
    )
