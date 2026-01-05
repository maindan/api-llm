from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import message, payments

app = FastAPI(title="Wpp Bot")

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message.router, prefix="/message", tags=['message'])
app.include_router(payments.router, prefix="/payments", tags=['payments'])

@app.get("/")
def main():
    return {"status":"ok"}