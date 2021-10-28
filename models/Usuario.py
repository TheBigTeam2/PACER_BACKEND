from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.Base import Base
from dataclasses import dataclass
from models.relationship_tables.aluno_equipe import aluno_equipe

class Usuario(Base):
    usu_id: int
    usu_rg: str
    usu_cpf: str
    usu_nome: str
    usu_auth: str

    
    __tablename__ = "usuario"

    usu_id = Column(Integer,primary_key=True)
    usu_rg = Column(String)
    usu_cpf = Column(String)
    usu_nome = Column(String)    
    usu_auth = Column(String)

    equipes = relationship("Equipe",secondary=aluno_equipe,back_populates="alunos")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
