from sqlalchemy import Column, Integer, String
from app.database import Base


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party_type = Column(String, nullable=False)