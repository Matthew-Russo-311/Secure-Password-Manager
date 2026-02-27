from app import db
from app.models.audit_log import AuditLog

def log_action(user_id, action, entry_id=None):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entry_id=entry_id
    )
    db.session.add(log)
    db.session.commit()