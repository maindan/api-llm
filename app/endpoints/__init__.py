from fastapi import FastAPI

app = FastAPI(title="Wpp Bot")

@app.get("/")
def health():
    return {"status":"ok"}