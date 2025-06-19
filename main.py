from fastapi import FastAPI
import requests
import os

app = FastAPI()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.get("/shipments")
def get_shipments():
    if not ACCESS_TOKEN:
        return {"error": "Access token no definido."}

    try:
        url = "https://api.mercadolibre.com/marketplace/shipments/search"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}
