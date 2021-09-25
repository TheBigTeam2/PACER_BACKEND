from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.Base import Base


class Disciplina(Base):

    __tablename__ = "disciplina"
    dis_id = Column(Integer,primary_key=True)
    dis_professor = Column(None,ForeignKey('professor.pro_cpf'))

    professor = relationship("Professor",back_populates="disciplinas")