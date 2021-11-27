from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Usuario import Usuario
from models.Projeto import Projeto
from dataclasses import dataclass

@dataclass
class Avaliacao(Base):
    ava_id: int
    ava_sprint: int
    ava_inicio: str
    ava_termino: str
    ava_avaliado: int
    ava_avaliador: int
    ava_projeto: int

    __tablename__ = "avaliacao"
    ava_id = Column(Integer, primary_key=True)
    ava_sprint = Column(Integer)
    ava_inicio = Column(DateTime)
    ava_termino = Column(DateTime)
    ava_avaliado = Column(Integer, ForeignKey(Usuario.usu_id))
    ava_avaliador = Column(Integer, ForeignKey(Usuario.usu_id))
    ava_projeto = Column(Integer,ForeignKey(Projeto.pro_id))

    avaliado = relationship("Usuario", foreign_keys=ava_avaliado)
    avaliador = relationship("Usuario", foreign_keys=ava_avaliador)
    projeto = relationship("Projeto", foreign_keys=ava_projeto, backref="avaliacoes",lazy=True)
    notas = relationship("Nota",back_populates="avaliacao",lazy=True)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
