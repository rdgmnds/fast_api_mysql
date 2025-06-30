from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ROTA PARA CRIAR EMPRESAS
@router.post("/empresas/")
def criar_empresa(nome: str, cnpj: str, diretor: str, nucleo_id: int, endereco: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()
    if db_user:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

    nova_empresa = models.Empresa(nome=nome, cnpj=cnpj, diretor=diretor, nucleo_id=nucleo_id, endereco=endereco, email=email)
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)  
    return nova_empresa

# ROTA PARA LISTAR EMPRESAS
@router.get("/empresas/")
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(models.Empresa).all()
    return empresas

# ROTA PARA BUSCAR EMPRESAS POR ID
@router.get("/empresas/{empresa_id}")
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa