from sqlalchemy.orm import Session

from app.db import base  # noqa: F401
from app.db.session import engine


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But for this example, we'll create them directly
    base.Base.metadata.create_all(bind=engine)