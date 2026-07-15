from app.db.database import engine
from app.models.analysis import Analysis
from app.models.feedback import Feedback
from app.db.database import Base


def create_tables():
    Base.metadata.create_all(
        bind=engine
    )