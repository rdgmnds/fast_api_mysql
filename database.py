from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# SQLite: cria um arquivo `meu_banco.db`
DATABASE_URL = settings.database_url

# Cria a engine do banco
engine = create_engine(DATABASE_URL)

# Cada instância da classe SessionLocal será uma sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos declarativos
Base = declarative_base()