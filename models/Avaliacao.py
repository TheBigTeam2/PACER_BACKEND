from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base

class Avaliacao(Base):

    __tablename__ = "avaliacao"
    ava_id = Column(Integer, primary_key=True)
    ava_sprint = Column(Integer)
    ava_inicio = Column(DateTime)
    ava_termino = Column(DateTime)
    ava_avaliado = Column(None, ForeignKey("usuario.usu_id"))
    ava_avaliador = Column(None, ForeignKey("usuario.usu_id"))
    ava_projeto = Column(None,ForeignKey("projeto.pro_id"))

    avaliado = relationship("Usuario", foreign_keys=ava_avaliado)
    avaliador = relationship("Usuario", foreign_keys=ava_avaliador)
    projeto = relationship("Projeto", foreign_keys=ava_projeto, backref="avaliacoes")
    notas = relationship("Nota",back_populates="avaliacao")
