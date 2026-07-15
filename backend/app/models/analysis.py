from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.db.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    input_text = Column(
        Text,
        nullable=False
    )

    credibility_score = Column(
        Integer,
        nullable=False
    )

    verdict = Column(
        String,
        nullable=False
    )

    technologies = Column(
        Text
    )

    reasoning = Column(
        Text
    )