from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/shipments")
def get_shipments():
    try:
        token1 = os.getenv("REFRESH_TOKEN_NARVAJA")
        token2 = os.getenv("REFRESH_TOKEN_BUDHASLEEP")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        def get_access_token(refresh_token):
            res = requests.post(
                "https://api.mercadolibre.com/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            res.raise_for_status()
            return res.json()["access_token"]

        access_tokens = [get_access_token(token1), get_access_token(token2)]
        all_shipments = []

        for token in access_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get("https://api.mercadolibre.com/flex/shipments", headers=headers)
            response.raise_for_status()
            all_shipments.extend(response.json())

        return all_shipments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
