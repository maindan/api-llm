from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.payments import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate
from datetime import date
from sqlalchemy import extract

class PaymentController:

    def _percentual_variacao(self, atual: float, anterior: float) -> int:
        if anterior == 0:
            return 100 if atual > 0 else 0
        return round(((atual - anterior) / anterior) * 100)

    def create_payment(self, db: Session, payload: PaymentCreate) -> Payment:
        payment = Payment(**payload.model_dump())
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment


    def get_payment(self, db: Session, payment_id):
        return db.query(Payment).filter(Payment.id == payment_id).first()


    def list_payments(self, db: Session, skip: int = 0, limit: int = 20):
        return (
            db.query(Payment)
            .order_by(Payment.data_pagamento.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


    def update_payment(self, db: Session, payment: Payment, payload: PaymentUpdate):
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(payment, field, value)

        db.commit()
        db.refresh(payment)
        return payment


    def delete_payment(self, db: Session, payment: Payment):
        db.delete(payment)
        db.commit()


    def dashboard_mensal(self, db: Session, ano_mes: str):
        ano, mes = map(int, ano_mes.split("-"))

        # mês atual
        query_atual = db.query(Payment).filter(
            extract("year", Payment.data_pagamento) == ano,
            extract("month", Payment.data_pagamento) == mes
        )

        # mês anterior
        if mes == 1:
            ano_ant, mes_ant = ano - 1, 12
        else:
            ano_ant, mes_ant = ano, mes - 1

        query_anterior = db.query(Payment).filter(
            extract("year", Payment.data_pagamento) == ano_ant,
            extract("month", Payment.data_pagamento) == mes_ant
        )

        # === totais ===
        total_atual = query_atual.with_entities(
            func.coalesce(func.sum(Payment.valor), 0)
        ).scalar()

        total_anterior = query_anterior.with_entities(
            func.coalesce(func.sum(Payment.valor), 0)
        ).scalar()

        # === média semanal ===
        media_atual = float(total_atual) / 4 if total_atual else 0
        media_anterior = float(total_anterior) / 4 if total_anterior else 0

        # === PIX ===
        pix_atual = (
            query_atual.filter(Payment.tipo == "PIX")
            .with_entities(func.coalesce(func.sum(Payment.valor), 0))
            .scalar()
        )

        pix_anterior = (
            query_anterior.filter(Payment.tipo == "PIX")
            .with_entities(func.coalesce(func.sum(Payment.valor), 0))
            .scalar()
        )

        # === quantidade ===
        qtd_atual = query_atual.count()
        qtd_anterior = query_anterior.count()

        return {
            "total_arrecadado": {
                "valor": float(total_atual),
                "variacao": self._percentual_variacao(total_atual, total_anterior)
            },
            "media_semanal": {
                "valor": round(media_atual, 2),
                "variacao": self._percentual_variacao(media_atual, media_anterior)
            },
            "pagamentos_pix": {
                "valor": float(pix_atual),
                "variacao": self._percentual_variacao(pix_atual, pix_anterior)
            },
            "total_pagamentos": {
                "valor": qtd_atual,
                "variacao": self._percentual_variacao(qtd_atual, qtd_anterior)
            }
        }
    
    def dashboard_anual(self, db: Session, ano: int):
        por_mes = (
            db.query(
                extract("month", Payment.data_pagamento).label("mes"),
                func.sum(Payment.valor).label("valor")
            )
            .filter(extract("year", Payment.data_pagamento) == ano)
            .group_by("mes")
            .order_by("mes")
            .all()
        )

        por_tipo = (
            db.query(
                Payment.tipo.label("tipo"),
                func.sum(Payment.valor).label("valor")
            )
            .filter(extract("year", Payment.data_pagamento) == ano)
            .group_by(Payment.tipo)
            .all()
        )

        return {
            "por_mes": [
                {"mes": int(row.mes), "valor": float(row.valor)}
                for row in por_mes
            ],
            "por_tipo": [
                {"tipo": row.tipo, "valor": float(row.valor)}
                for row in por_tipo
            ]
        }

    
payment_controller = PaymentController()