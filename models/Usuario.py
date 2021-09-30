from sqlalchemy import Column, Integer, String
from models.Base import Base

class Usuario(Base):
    __tablename__ = "usuario"

    usu_id = Column(Integer,primary_key=True)
    usu_nome = Column(String)    
    usu_email = Column(String)
    usu_senha = Column(String)