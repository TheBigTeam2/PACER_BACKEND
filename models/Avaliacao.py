from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from models.Base import Base

class Avaliacao(Base):

    ava_id = Column(Integer, primary_key=True)
    ava_sprint = Column(Integer)
    ava_inicio = Column(DateTime)
    ava_termino = Column(DateTime)
    ava_avaliado = Column(None, ForeignKey("usuario.usu_id"))
    ava_avaliador = Column(None, ForeignKey("usuario.usu_id"))
    ava_projeto = Column(None,ForeignKey("projeto.pro_id"))