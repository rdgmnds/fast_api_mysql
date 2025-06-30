from fastapi import FastAPI, Depends, HTTPException, APIRouter
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

# ROTA PARA CRIAR USUÁRIOS
@router.post("/usuarios/")
def criar_usuario(nome: str, idade: int, email: str, celular: str, endereco: str, cargo: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Cria o usuário
    novo_usuario = models.Usuario(nome=nome, idade=idade, email=email, cargo=cargo, endereco=endereco, celular=celular)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) 
    return novo_usuario 

# ROTA PARA LISTAR USUÁRIOS
@router.get("/usuarios/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return usuarios

# ROTA PARA BUSCAR USUÁRIOS POR ID
@router.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario