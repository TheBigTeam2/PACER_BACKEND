from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Aluno import Aluno
from models.Usuario import Usuario

from models.relationship_tables.aluno_equipe import aluno_equipe
#from models.AlunoEquipe import AlunoEquipe

from models.relationship_tables.projeto_equipe import projeto_equipe
from dataclasses import dataclass

@dataclass
class Equipe(Base):
    equ_id: int
    equ_nome: str
    equ_disciplina: int

    __tablename__ = "equipe"
    equ_id = Column(Integer,primary_key=True)
    equ_nome = Column(String)
    equ_disciplina = Column(Integer)

    alunos = relationship(Usuario,secondary=aluno_equipe,back_populates="equipes", lazy=False)
    projetos = relationship("Projeto",secondary=projeto_equipe,back_populates="equipes")

    def as_dict(self):
       return {
           "equ_id": self.equ_id,
           "equ_disciplina": self.equ_disciplina,
           "equ_nome": self.equ_nome,
           "equ_alunos": [aluno.as_dict_simple() for aluno in self.alunos]
       }
