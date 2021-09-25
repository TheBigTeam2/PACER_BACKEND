from sqlalchemy import Integer, ForeignKey, Column
from models.Usuario import Usuario

class Aluno(Usuario):
    __mapper_args__ = {'polymorphic_identity': 'aluno'}

    alu_usuario = Column(None,ForeignKey("usuario.usu_id"))
    alu_ra = Column(Integer)