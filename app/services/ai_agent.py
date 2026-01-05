import os
import json
import re
from typing import Dict, Any
from groq import Groq

class AIService:

    def __init__(self):
        self.SYSTEM_INSTRUCTION = (
            "Você é um sistema de extração de dados financeiros.\n\n"
            "Analise textos de comprovantes de pagamento e responda "
            "EXCLUSIVAMENTE com JSON válido, sem texto adicional.\n\n"

            "Regras obrigatórias:\n"
            "- Retorne APENAS os campos definidos abaixo\n"
            "- Campos não identificados devem ser null\n"
            "- O campo 'valor' deve ser numérico (ex: 150.75)\n"
            "- O campo 'data_pagamento' deve ser string no formato YYYY-MM-DD\n"
            "- O campo 'nome_pagador' deve conter apenas o nome da pessoa\n"
            "- O campo 'banco_origem' deve conter apenas o nome do banco\n"
            "- O campo 'referencia_externa' deve conter apenas o identificador da transação\n"
            "- O campo 'tipo' deve ser SEMPRE MAIÚSCULO\n\n"

            "Tipos permitidos:\n"
            "PIX | BOLETO | TED | DOC | CARTAO | TRANSFERENCIA | OUTROS\n\n"

            "Inferência do tipo:\n"
            "- Se existir chave PIX ou QR Code → PIX\n"
            "- Se existir código de barras → BOLETO\n"
            "- Se existir agência e conta → TED\n"
            "- Se não for possível identificar → OUTROS\n\n"

            "Estrutura obrigatória:\n"
            "{\n"
            "  \"valor\": number | null,\n"
            "  \"data_pagamento\": string | null,\n"
            "  \"tipo\": string,\n"
            "  \"nome_pagador\": string | null,\n"
            "  \"banco_origem\": string | null,\n"
            "  \"referencia_externa\": string | null\n"
            "}"
        )

        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
        self.model = "llama-3.3-70b-versatile"

    async def analyze_payment_text(self, text: str) -> Dict[str, Any]:

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_INSTRUCTION
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )

            raw_text = completion.choices[0].message.content
            data = self._safe_json_parse(raw_text)

            # Regra obrigatória: tipo nunca pode ser vazio
            if not data.get("tipo"):
                data["tipo"] = "OUTROS"

            data["tipo"] = data["tipo"].upper()

            return data

        except Exception as e:
            print(f"Erro na chamada da IA (Groq): {e}")
            return {}

    def _safe_json_parse(self, text: str) -> dict:
        clean_text = re.sub(r"```json\s*|\s*```", "", text).strip()

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", clean_text)
            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    pass
            return {}

ai_service = AIService()