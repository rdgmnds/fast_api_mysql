from fastapi import Depends, HTTPException, APIRouter
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

# ROTA PARA CRIAR PRODUTOS
@router.post("/produtos/")
def criar_produto(nome: str, preco: float, categoria: str, sub_categoria: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Produto).filter(models.Produto.id == id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Produto já cadastrado")

    novo_produto = models.Produto(nome=nome, preco=preco, categoria=categoria, sub_categoria=sub_categoria)
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)  
    return novo_produto

# ROTA PARA LISTAR PRODUTOS
@router.get("/produtos/")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(models.Produto).all()
    return produtos

# ROTA PARA BUSCAR PRODUTOS POR ID
@router.get("/produtos/{produto_id}")
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto