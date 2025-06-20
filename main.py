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

    accounts = {
        "Narvaja": os.getenv("REFRESH_TOKEN_NARVAJA"),
        "Budhasleep": os.getenv("REFRESH_TOKEN_BUDHASLEEP")
    }

    for name, refresh_token in accounts.items():
        token_resp = requests.post("https://api.mercadolibre.com/oauth/token", json={
            "grant_type": "refresh_token",
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "refresh_token": refresh_token
        })

        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            print(f"Error con token {name}: {token_data}")
            continue

        # FLEX = "self_service" o "me2" con modo "custom"
        orders_resp = requests.get(
            "https://api.mercadolibre.com/orders/search?seller=me&order.status=paid&tags=ready_to_ship&shipping.mode=me2&shipping.type=default",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        orders_data = orders_resp.json()
        for order in orders_data.get("results", []):
            buyer = order.get("buyer", {})
            shipments.append({
                "id": order["id"],
                "name": buyer.get("nickname", "Sin nombre"),
                "phone": buyer.get("phone", {}).get("number", "Sin teléfono")
            })

    return shipments

@app.post("/mark-delivered/{shipment_id}")
def mark_delivered(shipment_id: str):
    return {"message": f"Pedido {shipment_id} marcado como entregado"}
