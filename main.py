from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Credentials(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: Credentials):
    if data.username == "julio" and data.password == "admin123":
        return {"message": "Login successful"}
    return {"error": "Invalid credentials"}

@app.get("/shipments")
def get_shipments():
    shipments = []

    tokens = {
        "Narvaja": os.getenv("REFRESH_TOKEN_NARVAJA"),
        "Budhasleep": os.getenv("REFRESH_TOKEN_BUDHASLEEP")
    }

    for account, refresh_token in tokens.items():
        token_response = requests.post("https://api.mercadolibre.com/oauth/token", json={
            "grant_type": "refresh_token",
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "refresh_token": refresh_token
        })

        access_token = token_response.json().get("access_token")
        if not access_token:
            continue

        meli_response = requests.get(
            "https://api.mercadolibre.com/orders/search?seller=me&tags=delivered",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        orders = meli_response.json().get("results", [])
        for o in orders:
            shipments.append({
                "id": o["id"],
                "name": o.get("buyer", {}).get("nickname", "Desconocido"),
                "phone": o.get("buyer", {}).get("phone", {}).get("number", "Sin teléfono")
            })

    return shipments

@app.post("/mark-delivered/{shipment_id}")
def mark_delivered(shipment_id: str):
    return {"message": f"Pedido {shipment_id} marcado como entregado"}
