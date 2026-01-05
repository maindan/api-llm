from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.deps import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
    DashboardMensal
)
from app.controllers import payment_controller

router = APIRouter()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def criar_pagamento(payload: PaymentCreate, db: Session = Depends(get_db)):
    return payment_controller.create_payment(db, payload)


@router.get("/", response_model=list[PaymentResponse])
def listar_pagamentos(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return payment_controller.list_payments(db, skip, limit)


@router.get("/{payment_id}", response_model=PaymentResponse)
def buscar_pagamento(payment_id: UUID, db: Session = Depends(get_db)):
    payment = payment_controller.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def atualizar_pagamento(
    payment_id: UUID,
    payload: PaymentUpdate,
    db: Session = Depends(get_db)
):
    payment = payment_controller.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    return payment_controller.update_payment(db, payment, payload)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pagamento(payment_id: UUID, db: Session = Depends(get_db)):
    payment = payment_controller.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    payment_controller.delete_payment(db, payment)

@router.get("/dashboard/mensal")
def dashboard_mensal(
    ano_mes: str,
    db: Session = Depends(get_db)
):
    return payment_controller.dashboard_mensal(db, ano_mes)

@router.get("/dashboard/anual")
def dashboard_anual(
    ano: int,
    db: Session = Depends(get_db)
):
    return payment_controller.dashboard_anual(db, ano)