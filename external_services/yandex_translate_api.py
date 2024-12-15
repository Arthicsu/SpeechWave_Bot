import requests
from config_data.config import Config
class YandexTranslateAPI:
    def __init__(self, iam_token: str, folder_id: str):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.url = "https://translate.api.cloud.yandex.net/translate/v2/translate"

    async def translate_text(self, texts: list[str], target_language: str) -> list[str]:
        body = {
            "targetLanguageCode": target_language,
            "texts": texts,
            "folderId": self.folder_id,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.iam_token}",
        }

        response = requests.post(self.url, json=body, headers=headers)
        response.raise_for_status()
        translated_texts = response.json().get("translations", [])
        return [item["text"] for item in translated_texts]

def create_yandex_translate(config: Config) -> YandexTranslateAPI:
    return YandexTranslateAPI(
        iam_token=config.yandex_translate.iam_token,
        folder_id=config.yandex_translate.folder_id
    )