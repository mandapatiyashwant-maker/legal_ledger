from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class RRRDocument(Base):
    __tablename__ = "rrr_documents"

    id = Column(Integer, primary_key=True, index=True)

    rrr_id = Column(
        Integer,
        ForeignKey("rrrs.id"),
        nullable=False
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )