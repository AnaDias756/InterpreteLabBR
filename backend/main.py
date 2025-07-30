from fastapi import FastAPI

app = FastAPI(title="HemoBR API")

@app.get("/saude")
def saude_check():
    return {"status": "ok"}
