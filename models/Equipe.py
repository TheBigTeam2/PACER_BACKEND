from sqlalchemy import String, Integer, Column
from models.Base import Base

class Equipe(Base):

    equ_id = Column(Integer,primary_key=True)
    equ_disciplina = Column(Integer)
    equ_nome = Column(String)