from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import requests

app = FastAPI()

# Token fijo obtenido previamente (cuenta Budha)
ACCESS_TOKEN = "APP_USR-1866199927341274-062313-e5d2f5f76e10bcd5e9d42bcd9b7cf5e2-349336310"

@app.get("/")
def root():
    return HTMLResponse("<h2>Monitor de Envíos FLEX activo. Usá /shipments para ver los pedidos.</h2>")

@app.get("/shipments")
def get_shipments():
    if not ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Token no disponible")

    url = "https://api.mercadolibre.com/orders/search?seller=me&shipping_type=custom"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return HTMLResponse(f"<h2>Error cargando los pedidos (código {response.status_code}).</h2>")

    orders = response.json().get("results", [])

    html = "<h2>Pedidos FLEX</h2><table border='1'><tr><th>ID</th><th>Nombre</th><th>Teléfono</th></tr>"
    for order in orders:
        buyer = order.get("buyer", {})
        nickname = buyer.get("nickname", "N/A")
        phone = buyer.get("phone", {}).get("number", "N/A")
        html += f"<tr><td>{order.get('id')}</td><td>{nickname}</td><td>{phone}</td></tr>"
    html += "</table>"

    return HTMLResponse(html)

@app.get("/auth")
def auth():
    return RedirectResponse(url="/shipments")
