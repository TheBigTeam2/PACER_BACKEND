from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Avaliacao import Avaliacao
from models.Criterio import Criterio
from dataclasses import dataclass

class Nota(Base):
    not_id: int
    not_avaliacao: int
    not_criterio: int
    not_valor: int
    
    __tablename__ = "nota"
    not_id = Column(Integer,primary_key=True)
    not_avaliacao = Column(Integer,ForeignKey(Avaliacao.ava_id))
    not_criterio = Column(Integer,ForeignKey(Criterio.cri_id))
    not_valor = Column(Integer)

    avaliacao = relationship("Avaliacao",foreign_keys=not_avaliacao,back_populates="notas")
    criterio = relationship("Criterio", foreign_keys=not_criterio, back_populates="notas")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
