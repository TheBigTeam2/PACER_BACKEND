from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.orm import relationship
from models.Usuario import Usuario
from models.relationship_tables.aluno_equipe import aluno_equipe

class Aluno(Usuario):

    __mapper_args__ = {'polymorphic_identity': 'aluno'}
    __tablename__ = "aluno"
    alu_usuario = Column(None,ForeignKey("usuario.usu_id"),primary_key=True)
    alu_ra = Column(Integer)

    equipes = relationship("Equipe",secondary=aluno_equipe,back_populates="alunos")