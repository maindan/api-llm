from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional

class PaymentBase(BaseModel):
    valor: Decimal = Field(..., example=1500.00)
    data_pagamento: date = Field(..., example="2025-12-15")
    tipo: str = Field(..., example="pix")
    nome_pagador: str = Field(..., example="Carlos Almeida")
    banco_origem: Optional[str] = Field(None, example="Nubank")
    descricao: Optional[str] = Field(None, example="Pagamento serviço freelance")
    comprovante_url: Optional[str] = Field(None, example="/comprovantes/dez1.jpg")
    telefone_remetente: Optional[str] = Field(None, example="5592999999999")
    referencia_externa: Optional[str] = Field(None, example="MSG-DEZ-001")

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    valor: Optional[Decimal] = None
    data_pagamento: Optional[date] = None
    tipo: Optional[str] = None
    nome_pagador: Optional[str] = None
    banco_origem: Optional[str] = None
    descricao: Optional[str] = None
    comprovante_url: Optional[str] = None
    telefone_remetente: Optional[str] = None
    referencia_externa: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: UUID
    origem: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 2.0

class DashboardMensal(BaseModel):
    mes: datetime
    total: Decimal
