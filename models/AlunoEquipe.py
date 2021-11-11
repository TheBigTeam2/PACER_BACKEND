from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base
# from models.Usuario import Usuario
# from models.Equipe import Equipe
from dataclasses import dataclass

@dataclass
class AlunoEquipe(Base):
    ale_aluno: int
    ale_equipe: int

    __tablename__ = "aluno_equipe"
    #__table_args__ = {'extend_existing': True}

    ale_aluno = Column(Integer, primary_key=True)
    ale_equipe = Column(Integer, primary_key=True)

    usuario = relationship("Usuario",foreign_keys=ale_aluno)#, back_populates="aluno_equipe")
    equipe = relationship("Equipe", foreign_keys=ale_equipe)#, back_populates="aluno_equipe")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
