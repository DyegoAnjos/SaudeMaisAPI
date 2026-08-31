from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from saudemaisapi.routers import (
    categorias,
    eventos,
    fotografias,
    usuarios_comuns,
)

app = FastAPI(title='Saude+API')

origens_permitidas = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', tags=['Status'])
def verificar_api():
    return {'mensagem': 'API Saude+ funcionando'}


app.include_router(eventos.router)
app.include_router(categorias.router)
# app.include_router(unidades_saude.router)
app.include_router(usuarios_comuns.router)
app.include_router(fotografias.router)
