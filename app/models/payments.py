from sqlalchemy import Column, String, Numeric, Date, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    valor = Column(Numeric(10, 2), nullable=False)
    data_pagamento = Column(Date, nullable=False)
    tipo = Column(String(30), nullable=False)
    nome_pagador = Column(String(150), nullable=False)
    banco_origem = Column(String(100))

    descricao = Column(Text)
    comprovante_url = Column(Text)

    origem = Column(
        String(20),
        nullable=False,
        server_default=text("'whatsapp'")
    )

    telefone_remetente = Column(String(20))
    referencia_externa = Column(String(100))

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        server_onupdate=text("now()")
    )