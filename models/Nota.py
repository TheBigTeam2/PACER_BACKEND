from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base

class Nota(Base):
    __tablename__ = "nota"
    not_id = Column(Integer,primary_key=True)
    not_avaliacao = Column(None,ForeignKey("avaliacao.ava_id"))
    not_criterio = Column(String)
    not_valor = Column(Integer)

    avaliacao = relationship("Avaliacao",foreign_keys=not_avaliacao,back_populates="notas")