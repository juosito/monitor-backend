from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir acceso desde el frontend en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para obtener envíos FLEX
@app.get("/shipments")
def get_shipments():
    return [
        {
            "id": "001",
            "name": "Juan Pérez",
            "phone": "091234567"
        },
        {
            "id": "002",
            "name": "Lucía García",
            "phone": "092345678"
        }
    ]
