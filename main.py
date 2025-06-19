from fastapi import FastAPI

app = FastAPI()

@app.get("/shipments")
def get_shipments():
    return {"message": "Aquí van los envíos FLEX"}
