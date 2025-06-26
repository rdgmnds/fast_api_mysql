from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ROTA PARA CRIAR USUÁRIOS
@app.post("/usuarios/")
def criar_usuario(nome: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Cria o usuário
    novo_usuario = models.Usuario(nome=nome, email=email)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario) 
    return novo_usuario

# ROTA PARA CRIAR EMPRESAS
@app.post("/empresas/")
def criar_empresa(nome: str, cnpj: str, diretor: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()
    if db_user:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

    nova_empresa = models.Empresa(nome=nome, cnpj=cnpj, diretor=diretor)
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)  
    return nova_empresa

# ROTA PARA LISTAR USUÁRIOS
@app.get("/usuarios/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return usuarios

# ROTA PARA LISTAR EMPRESAS
@app.get("/empresas/")
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(models.Empresa).all()
    return empresas

# ROTA PARA BUSCAR USUÁRIOS POR ID
@app.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# ROTA PARA BUSCAR EMPRESAS POR ID
@app.get("/empresas/{empresa_id}")
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa