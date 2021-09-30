from sqlalchemy import  Column,Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.Usuario import Usuario
from dataclasses import dataclass

@dataclass
class Professor(Usuario):
    pro_id: int
    pro_usuario: int
    pro_cpf: int
    
    __tablename__ = "professor"
    pro_usuario = Column(None,ForeignKey("usuario.usu_id"),primary_key=True)
    pro_cpf = Column(Integer)
    
    disciplinas = relationship("Disciplina",back_populates="professor",lazy=True)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
