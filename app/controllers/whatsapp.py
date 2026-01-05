from app.services import waha_service, file_processor_service, ai_service, payment_service
from sqlalchemy.orm import Session
from .payments import payment_controller
from app.schemas.payment import PaymentCreate
from datetime import datetime, date
import os

class MessageController:
    def __init__(self):
        self.allowed_number = os.getenv("SELF_NUMBER")

    async def handle_message(self, db:Session, data: dict):
        print(data)
        if data["fromMe"] and data["to"] == self.allowed_number:
            message = data.get("body", "").lower()

            if message == "registrar pagamento":
                res = "Por favor, envie agora o comprovante de pagamento em formato de imagem (foto) ou PDF."
                waha_service.send_message(self.allowed_number, res)
            
            elif data["hasMedia"]:

                media = data.get("media")

                if not media["url"]:
                    print('Mídia sem url, aguarde')
                    return
                
                if media["mimetype"] == "image/webp":
                    return

                print(media)
                file_info = waha_service.download_file(
                    media_url=media["url"],
                    file_name=media["filename"],
                    mime_type=media["mimetype"]
                )

                waha_service.send_message(
                    self.allowed_number,
                    "📎 **Arquivo recebido com sucesso!**\n\n"
                    "⏳ Processando o comprovante..."
                )

                print("Arquivo salvo em:", file_info["path"])

                extracted_text = file_processor_service.extract_text(
                    file_info["path"],
                    file_info["mime_type"]
                )

                if not extracted_text or len(extracted_text.strip()) < 10:
                    waha_service.send_message(
                        self.allowed_number,
                        "⚠️ Não consegui ler o texto do comprovante.\n"
                        "Por favor, envie uma imagem mais nítida."
                    )
                    return

                ai_result = await ai_service.analyze_payment_text(extracted_text)

                if not isinstance(ai_result, dict):
                    raise ValueError("IA retornou formato inválido")

                validation = payment_service.validate(ai_result)

                print(ai_result)

                if validation["is_valid"]:

                    payment_payload = PaymentCreate(
                        valor=ai_result.get("valor"),
                        data_pagamento=datetime.strptime(
                            ai_result.get("data_pagamento"), "%Y-%m-%d"
                        ).date() if ai_result.get("data_pagamento") else date.today(),
                        tipo=ai_result.get("tipo", "OUTROS"),
                        nome_pagador=ai_result.get("nome_pagador"),
                        banco_origem=ai_result.get("banco_origem"),
                        descricao="Pagamento recebido via WhatsApp",
                        telefone_remetente=self.allowed_number, # AQUI ALTERA-SE PARA O NÚMERO DO USUÁRIO QUE ENVIOU O COMPROVANTE
                        referencia_externa=ai_result.get("referencia_externa"),
                        comprovante_url=ai_result.get("comprovante_url"),
                    )

                    payment = payment_controller.create_payment(db, payment_payload)


                    waha_service.send_message(
                        self.allowed_number,
                        "✅ **Comprovante registrado com sucesso!**\n\n"
                        f"➡️ ID: {payment.id}\n"
                        f"➡️ Banco Origem: {payment.banco_origem or 'Não identificado'}\n"
                        f"➡️ Pagador: {payment.nome_pagador}\n"
                        f"💰 Valor: R$ {payment.valor}\n"
                        f"📅 Data: {payment.data_pagamento}\n"
                        f"🔁 Tipo: {payment.tipo}"
                    )
                else:
                    waha_service.send_message(
                        self.allowed_number,
                        "⚠️ **Não consegui identificar todos os dados do comprovante.**\n\n"
                        "Por favor, envie um comprovante mais legível."
                    )

            else:
                print("recebeu mensagem mas não tem o texto correto")
            return 

        return
    
message_controller = MessageController()