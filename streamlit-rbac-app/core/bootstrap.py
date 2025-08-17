from sqlalchemy import select
from core.db import init_engine
from models.base import Base
# Import all models so tables are registered
from models import user, role, permission, activity_log, domain_tables  # noqa: F401
try:
    from models.associations import role_user, permission_role  # noqa: F401
except Exception:
    pass

def ensure_db_initialized():
    engine, SessionLocal = init_engine()
    # Create tables if not exist
    Base.metadata.create_all(engine)
    # If roles table is empty, run seeder
    from models.role import Role
    with SessionLocal() as db:
        has_role = db.execute(select(Role)).first()
        if not has_role:
            # lazy import seeder
            from core import seed
            seed.main()
