import requests
import os
from app.utils.file_utils import ensure_upload_dir, generate_file_name

class WahaService: 
    def __init__(self):
        self.base_url = "http://localhost:3000/api"
        self.api_key = os.getenv("WAHA_API_KEY")
        self.session = "default"

    def send_message(self, chat_id: str, text: str):
        url = f"{self.base_url}/sendText"
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "session": self.session,
            "chatId": chat_id,
            "text": text
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()

    def download_file(self, media_url: str, file_name: str | None, mime_type: str | None) -> dict:
        ensure_upload_dir()

        if(media_url.startswith("/")):
            media_url = f"{self.base_url}{media_url}"

        response = requests.get(
            media_url,
            headers={"X-Api-Key": self.api_key},
            stream=True
        )

        response.raise_for_status()

        final_name = generate_file_name(file_name, mime_type)
        file_path = f"uploads/{final_name}"

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return {
            "path": file_path,
            "file_name": final_name,
            "mime_type": mime_type
        }

waha_service = WahaService()