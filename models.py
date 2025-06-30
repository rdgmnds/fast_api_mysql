from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50))
    idade = Column(Integer)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    empresa = relationship("Empresa", back_populates="usuarios")
    
    endereco = Column(String(50))
    cargo = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    celular = Column(String(13))

##########################################################################################

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50))
    cnpj = Column(String(14), unique=True, index=True)
    usuarios = relationship("Usuario", back_populates="empresa")

    nucleo_id = Column(Integer, ForeignKey("nucleos.id"))
    nucleo = relationship("Nucleo", back_populates="empresas")

    endereco = Column(String(50))
    email = Column(String(50))
    diretor = Column(String(50))

##########################################################################################

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50))
    preco = Column(Float)
    categoria = Column(String(50))
    sub_categoria = Column(String(50))

##########################################################################################

class Nucleo(Base):
    __tablename__ = "nucleos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    regiao = Column(String(50))
    superintendente = Column(String(50))
    empresas = relationship("Empresa", back_populates="nucleo")


