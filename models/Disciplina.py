from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.Base import Base
from models.Professor import Professor
from models.relationship_tables.disciplina_projeto import disciplina_projeto


class Disciplina(Base):

    __tablename__ = "disciplina"
    dis_id = Column(Integer,primary_key=True)
    dis_professor = Column(None,ForeignKey('professor.pro_cpf'))

    professor = relationship(Professor,foreign_keys=dis_professor,back_populates="disciplinas")
    projetos = relationship("Projeto",secondary=disciplina_projeto,back_populates="disciplinas")