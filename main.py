from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usuarios para login
USERS = {
    "julio": "1234",  # podés cambiar esto si querés
}

# Ruta de login
@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) == password:
        return {"message": f"Login OK. Bienvenido {username}"}
    return {"error": "Credenciales inválidas"}, 401

# Ruta para ver pedidos FLEX
@app.get("/shipments")
def get_shipments():
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        return {"error": "ACCESS_TOKEN no configurado"}

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get("https://api.mercadolibre.com/marketplace/shipments/labels/search?sla_type=flex", headers=headers)

    if response.status_code == 200:
        data = response.json()
        shipments = []
        for result in data.get("results", []):
            shipments.append({
                "id": result.get("id"),
                "name": result.get("receiver", {}).get("name", "N/A"),
                "phone": result.get("receiver", {}).get("phone", "N/A"),
            })
        return shipments
    else:
        return {"error": response.text}

# Ruta para obtener el token real desde refresh_token
@app.get("/get-token")
def get_token():
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": os.getenv("REFRESH_TOKEN_NARVAJA")
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
