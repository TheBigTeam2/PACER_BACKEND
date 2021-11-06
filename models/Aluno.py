from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.orm import relationship
from models.Usuario import Usuario

from models.relationship_tables.aluno_equipe import aluno_equipe
# from models.AlunoEquipe import AlunoEquipe

from dataclasses import dataclass

@dataclass
class Aluno(Usuario):
    alu_id: int
    alu_ra: int
    alu_usuario: int

    __mapper_args__ = {'polymorphic_identity': 'aluno'}
    __tablename__ = "aluno"
    alu_usuario = Column(None,ForeignKey("usuario.usu_id"),primary_key=True)
    alu_ra = Column(Integer)

    equipes = relationship("Equipe",secondary=aluno_equipe,back_populates="alunos")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
