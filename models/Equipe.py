from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Usuario import Usuario
from models.relationship_tables.aluno_equipe import aluno_equipe
from models.relationship_tables.projeto_equipe import projeto_equipe
from dataclasses import dataclass

@dataclass
class Equipe(Base):
    equ_id: int
    equ_nome: str
    equ_disciplina: int

    __tablename__ = "equipe"
    equ_id = Column(Integer,primary_key=True)
    equ_disciplina = Column(Integer)
    equ_nome = Column(String)

    usuarios = relationship(Usuario,secondary=aluno_equipe,back_populates="equipes")
    projetos = relationship("Projeto",secondary=projeto_equipe,back_populates="equipes")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
