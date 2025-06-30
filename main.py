from fastapi import FastAPI
from routes import usuarios, empresas, produtos, nucleos
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(usuarios.router)
app.include_router(empresas.router)
app.include_router(produtos.router)
app.include_router(nucleos.router)
