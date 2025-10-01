from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.db.session import engine


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But for this example, we'll create them directly
    Base.metadata.create_all(bind=engine)