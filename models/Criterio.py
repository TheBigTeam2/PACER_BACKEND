from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base
from dataclasses import dataclass

class Criterio(Base):

    cri_id: int
    cri_nome: str
    
    __tablename__ = "criterio"

    cri_id = Column(Integer,primary_key=True)
    cri_nome = Column(String)

    notas = relationship("Nota",back_populates="criterio",lazy=True)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
