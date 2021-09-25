from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from models.Base import Base
from models.relationship_tables.aluno_equipe import aluno_equipe
from models.relationship_tables.projeto_equipe import projeto_equipe

class Equipe(Base):

    __tablename__ = "equipe"
    equ_id = Column(Integer,primary_key=True)
    equ_disciplina = Column(Integer)
    equ_nome = Column(String)

    alunos = relationship("Aluno",secondary=aluno_equipe,back_populates="equipes")
    projetos = relationship("Projeto",secondary=projeto_equipe,back_populates="equipes")