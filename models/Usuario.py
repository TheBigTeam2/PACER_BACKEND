from sqlalchemy import Column, Integer, String
from models.Base import Base
from dataclasses import dataclass

class Usuario(Base):
    usu_id: int
    usu_nome: str
    #usu_email: str
    #usu_senha: str
    
    __tablename__ = "usuario"

    usu_id = Column(Integer,primary_key=True)
    usu_nome = Column(String)    
    #usu_email = Column(String)
    #usu_senha = Column(String)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
