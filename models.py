from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50))
    email = Column(String(50), unique=True, index=True)

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50))
    cnpj = Column(String(14), unique=True, index=True)
    diretor = Column(String(50))