from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from models.Base import Base
from models.relationship_tables.projeto_equipe import projeto_equipe
from models.relationship_tables.disciplina_projeto import disciplina_projeto

class Projeto(Base):
    __tablename__ = "projeto"
    pro_id = Column(Integer,primary_key=True)
    pro_equipe = Column(Integer)

    #equipes = relationship("Equipe",secondary=projeto_equipe,back_populates="projetos",lazy=True)
    #disciplinas = relationship("Disciplina",secondary=disciplina_projeto,back_populates="projetos",lazy=True)