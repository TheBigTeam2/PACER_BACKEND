from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Usuario import Usuario
from models.Projeto import Projeto

class Avaliacao(Base):

    __tablename__ = "avaliacao"
    ava_id = Column(Integer, primary_key=True)
    ava_sprint = Column(Integer)
    ava_inicio = Column(DateTime)
    ava_termino = Column(DateTime)
    ava_avaliado = Column(Integer, ForeignKey(Usuario.usu_id))
    ava_avaliador = Column(Integer, ForeignKey(Usuario.usu_id))
    ava_projeto = Column(Integer,ForeignKey(Projeto.pro_id))

    avaliado = relationship("Usuario", foreign_keys=ava_avaliado,lazy=True)
    avaliador = relationship("Usuario", foreign_keys=ava_avaliador,lazy=True)
    projeto = relationship("Projeto", foreign_keys=ava_projeto, backref="avaliacoes",lazy=True)
    notas = relationship("Nota",back_populates="avaliacao",lazy=True)
