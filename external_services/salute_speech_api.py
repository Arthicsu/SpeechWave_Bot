from salute_speech.speech_recognition import SaluteSpeechClient
from config_data.config import Config

def create_salute_client(config: Config) -> SaluteSpeechClient:
    return SaluteSpeechClient(client_credentials=config.salute_speech.credentials)