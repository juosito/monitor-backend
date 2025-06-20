import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ajusta si quieres restringir
    allow_methods=["*"],
    allow_headers=["*"],
)

ML_BASE = "https://api.mercadolibre.com"

# Refresh tokens y app credentials leídos de variables de entorno
CLIENT_ID     = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REFRESH_TOKENS = {
    "NARVAJA":    os.getenv("REFRESH_TOKEN_NARVAJA"),
    "BUDHASLEEP": os.getenv("REFRESH_TOKEN_BUDHASLEEP")
}

if not CLIENT_ID or not CLIENT_SECRET or None in REFRESH_TOKENS.values():
    raise RuntimeError("🛑 Variables de entorno ML incompletas")

async def get_access_token(refresh_token: str) -> str:
    """Intercambia un refresh_token por un access_token"""
    url = f"{ML_BASE}/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, data=data)
        r.raise_for_status()
    return r.json()["access_token"]

async def list_flex_shipments(token: str):
    """Obtiene los envíos FLEX pendientes de esta cuenta"""
    params = {"q": "status:ready_to_ship", "tags": "self_service_in" }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{ML_BASE}/shipments/search", params=params,
                             headers={"Authorization": f"Bearer {token}"})
        r.raise_for_status()
    return r.json().get("results", [])

@app.get("/")
def root():
    return {"message": "Aquí van los envíos FLEX"}

@app.get("/get-token/{account}")
async def _get_token(account: str):
    """Devuelve el access_token de una cuenta (debug opcional)"""
    account = account.upper()
    if account not in REFRESH_TOKENS:
        raise HTTPException(404, "Cuenta desconocida")
    return {"access_token": await get_access_token(REFRESH_TOKENS[account])}

@app.get("/shipments")
async def shipments():
    """Une los envíos FLEX de todas las cuentas configuradas"""
    shipments_all = []
    for acc, ref_tok in REFRESH_TOKENS.items():
        try:
            token = await get_access_token(ref_tok)
            shps  = await list_flex_shipments(token)
            # agrega el nombre de la cuenta para distinguir
            for s in shps:
                s["account"] = acc
            shipments_all.extend(shps)
        except httpx.HTTPStatusError as e:
            raise HTTPException(502, f"Mercado Libre error ({acc}): {e.response.text}") from e
    return shipments_all
