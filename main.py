import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ACCESS_TOKEN = "TU_ACCESS_TOKEN_AQUÍ"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O poné tu frontend en producción
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/shipments")
def get_shipments():
    url = "https://api.mercadolibre.com/marketplace/shipments/search"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "status": "ready_to_ship",
        "shipping_type": "fulfillment",
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    shipments = response.json()

    # Transformar a formato usable por el frontend
    result = []
    for s in shipments.get("results", []):
        result.append({
            "id": s["id"],
            "name": s.get("receiver", {}).get("name", "Desconocido"),
            "phone": s.get("receiver", {}).get("phone", "Sin teléfono")
        })

    return result
