from fastapi import (
    FastAPI,
)

from saudemaisapi.routers import (
    eventos,
    fotografias,
    usuarios_comuns,
)

app = FastAPI(title='Saude+API')

app.include_router(eventos.router)
app.include_router(usuarios_comuns.router)
app.include_router(fotografias.router)
