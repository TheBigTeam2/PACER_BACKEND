from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Usuario import Usuario
from models.relationship_tables.disciplina_projeto import disciplina_projeto
from dataclasses import dataclass


class Disciplina(Base):
    dis_id: int
    dis_semestre: str
    dis_professor: str
    dis_nome: str

    __tablename__ = "disciplina"
    dis_id = Column(Integer,primary_key=True)
    dis_professor = Column(None,ForeignKey('usuario.usu_id'))

    professor = relationship(Usuario,foreign_keys=dis_professor,back_populates="disciplinas")
    projetos = relationship("Projeto",secondary=disciplina_projeto,back_populates="disciplinas")

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
