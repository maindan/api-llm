class PaymentValidatorService:

    REQUIRED_FIELDS = [
        "valor",
        "data_pagamento",
        "tipo",
        "nome_pagador"
    ]

    def validate(self, data: dict) -> dict:
        missing = [
            field for field in self.REQUIRED_FIELDS
            if not data.get(field)
        ]

        return {
            "is_valid": len(missing) == 0,
            "missing_fields": missing,
            "data": data
        }


payment_service = PaymentValidatorService()