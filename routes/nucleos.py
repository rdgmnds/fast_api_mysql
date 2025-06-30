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

# ROTA PARA CRIAR NUCLEOS
@router.post("/nucleos/")
def criar_nucleo(regiao: str, superintendente: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Nucleo).filter(models.Nucleo.id == id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nucleo já cadastrado")

    novo_nucleo = models.Nucleo(regiao=regiao, superintendente=superintendente)
    db.add(novo_nucleo)
    db.commit()
    db.refresh(novo_nucleo)  
    return novo_nucleo

# ROTA PARA LISTAR NUCLEOS 
@router.get("/nucleos/")
def listar_nucleos(db: Session = Depends(get_db)):
    nucleos = db.query(models.Nucleo).all()
    return nucleos

# ROTA PARA BUSCAR NUCLEO POR ID
@router.get("/nucleos/{produto_id}")
def obter_nucleo(nucleo_id: int, db: Session = Depends(get_db)):
    nucleo = db.query(models.Nucleo).filter(models.Nucleo.id == nucleo_id).first()
    if nucleo is None:
        raise HTTPException(status_code=404, detail="Nucleo não encontrado")
    return nucleo