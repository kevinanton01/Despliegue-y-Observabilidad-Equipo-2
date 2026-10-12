
import os
import sentry_sdk

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import SessionLocal


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=False
)

app = FastAPI()


# Permitir que el frontend se comunique con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://despliegue-y-observabilidad-equipo-five.vercel.app"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"mensaje": "Backend FastAPI funcionando"}


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    db = SessionLocal()

    try:
        resultado = db.execute(
            text("SELECT id, nombre FROM usuarios WHERE id = :id"),
            {"id": usuario_id}
        ).mappings().first()

        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "id": resultado["id"],
            "nombre": resultado["nombre"]
        }

    finally:
        db.close()


@app.get("/sentry-debug")
async def sentry_debug():
    division = 1 / 0
    return {"resultado": division}
