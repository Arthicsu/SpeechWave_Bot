import logging
from aiogram import Bot, F, types, Router
from salute_speech.speech_recognition import SaluteSpeechClient
from services.file_handling import process_voice_file
from config_data.config import Config, load_config

logger = logging.getLogger(__name__)

user_languages = {}
router = Router()

def create_salute_client(config: Config) -> SaluteSpeechClient:
    return SaluteSpeechClient(client_credentials=config.salute_speech.credentials)

@router.message(F.voice)
async def handle_voice(message: types.Message, bot: Bot, config: Config):
    salute_client = create_salute_client(config)

    user_id = message.from_user.id
    language = user_languages.get(user_id, "ru-RU")

    try:
        file = await bot.get_file(message.voice.file_id)
        wav_file = await process_voice_file(file, bot)
        result = await salute_client.audio.transcriptions.create(
            file=wav_file,
            language=language
        )
        await message.reply(f"{result.text}")

    except Exception as e:
        logger.error(f"Ошибка при транскрипции: {e}")
        await message.reply("Упс :( \n Произошла ошибка при обработке голосового сообщения.")