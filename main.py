from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

# Cria as tabelas no banco (se não existirem)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência: cria uma sessão do banco para cada requisição e fecha ao final
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Rota para criar um usuário
@app.post("/usuarios/")
def criar_usuario(nome: str, email: str, db: Session = Depends(get_db)):
    # Verifica se já existe usuário com esse email
    db_user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Cria o usuário
    novo_usuario = models.Usuario(nome=nome, email=email)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)  # Atualiza o objeto com os dados do banco (como o ID)
    return novo_usuario

# Rota para criar uma empresa
@app.post("/empresas/")
def criar_empresa(nome: str, cnpj: str, diretor: str, db: Session = Depends(get_db)):
    # Verifica se já existe usuário com esse cnpj
    db_user = db.query(models.Empresa).filter(models.Empresa.cnpj == cnpj).first()
    if db_user:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

    # Cria o usuário
    nova_empresa = models.Empresa(nome=nome, cnpj=cnpj, diretor=diretor)
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)  # Atualiza o objeto com os dados do banco (como o ID)
    return nova_empresa

# Rota para listar todos os usuários
@app.get("/usuarios/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return usuarios

# Rota para listar todas as empresas
@app.get("/empresas/")
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(models.Empresa).all()
    return empresas

# Rota para buscar um usuário por ID
@app.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# Rota para buscar uma empresa por id
@app.get("/empresas/{empresa_id}")
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa