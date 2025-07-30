from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    z = Column(Integer, nullable=False)

    bucket = relationship(
        "Bucket",
        back_populates="position",
        uselist=False
    )


class Bucket(Base):
    __tablename__ = "buckets"

    id = Column(Integer, primary_key=True)
    material_type = Column(String, nullable=False)
    material_qty = Column(Integer, nullable=False)

    position_id = Column(
        Integer,
        ForeignKey("positions.id"),
        unique=True,
        nullable=True
    )
    position = relationship(
        "Position",
        back_populates="bucket"
    )
