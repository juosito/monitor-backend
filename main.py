from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS para permitir acceso desde el frontend en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o limitá al dominio exacto si querés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para recibir login
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginRequest):
    if data.username == "julio" and data.password == "narvaja":
        return {"status": "ok"}
    return {"status": "error"}, 401

@app.get("/shipments")
def get_shipments():
    return {"message": "Aquí van los envíos FLEX"}
