from sqlalchemy import  Column,Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.Usuario import Usuario

class Professor(Usuario):
    __tablename__ = "professor"
    pro_usuario = Column(None,ForeignKey("usuario.usu_id"),primary_key=True)
    pro_cpf = Column(Integer)
    
    disciplinas = relationship("Disciplina",back_populates="professor",lazy=True)