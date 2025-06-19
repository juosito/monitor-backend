@app.get("/get-token")
def get_token():
    return {"access_token": refresh_access_token()}
