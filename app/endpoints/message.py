from fastapi import APIRouter, Request, Depends
from app.controllers import message_controller
import requests
from app.db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/whatsapp")
async def receive_message(request: Request,  db: Session = Depends(get_db)):
    payload = await request.json()
    
    data = payload.get("payload")

    if not data:
        print('sem dados')
        return
    
    await message_controller.handle_message(db, data)

    return {'status':'ok'}