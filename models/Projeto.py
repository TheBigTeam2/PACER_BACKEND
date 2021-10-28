from sqlalchemy import Column, Integer, String, DateTime
from models.Base import Base
from models.Equipe import Equipe
from sqlalchemy.orm import relationship
from models.Disciplina import Disciplina
from models.relationship_tables.projeto_equipe import projeto_equipe
from models.relationship_tables.disciplina_projeto import disciplina_projeto
from dataclasses import dataclass

class Projeto(Base):
    pro_id: int
    pro_equipe: int
    
    __tablename__ = "projeto"
    pro_id = Column(Integer,primary_key=True)
    pro_tema = Column(String)
    pro_inicio = Column(DateTime)
    pro_termino = Column(DateTime)

    equipes = relationship(Equipe,secondary=projeto_equipe,back_populates="projetos",lazy=True)
    disciplinas = relationship(Disciplina,secondary=disciplina_projeto,back_populates="projetos",lazy=True)


    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    
