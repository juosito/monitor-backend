from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

CLIENT_ID = "8230362313334703"
CLIENT_SECRET = "dbRj5M25cxATQkm7H1TAWrXpvgP38WLh"
REDIRECT_URI = "https://monitor-frontend-liard.vercel.app/auth"
AUTH_CODE = "TG-68628983ad107e0001e6203a-349336310"

ACCESS_TOKEN = None

def obtener_token():
    global ACCESS_TOKEN
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": AUTH_CODE,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post("https://api.mercadolibre.com/oauth/token", data=payload)
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
    else:
        print("Error al obtener el token:", response.text)

@app.get("/")
def login():
    return HTMLResponse("<h2>Monitor backend funcionando. Ir a /shipments para ver pedidos.</h2>")

@app.get("/shipments")
def get_shipments():
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        obtener_token()
        if not ACCESS_TOKEN:
            raise HTTPException(status_code=401, detail="Token no disponible")

    response = requests.get("https://api.mercadolibre.com/orders/search?seller=me&shipping_type=custom", headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    })

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error obteniendo los envíos")

    orders = response.json().get("results", [])
    result_html = "<h2>Pedidos FLEX</h2><table border='1'><tr><th>ID</th><th>Nombre</th><th>Teléfono</th></tr>"
    for order in orders:
        buyer = order.get("buyer", {})
        result_html += f"<tr><td>{order.get('id')}</td><td>{buyer.get('nickname')}</td><td>{buyer.get('phone', {}).get('number', '')}</td></tr>"
    result_html += "</table>"
    return HTMLResponse(result_html)
