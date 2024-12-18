import logging
from aiogram import Bot, F, types, Router
from lexicon.lexicon import LANG_LEXICON, LEXICON_EN
from services.file_handling import process_voice_file
from config_data.config import Config, load_config
from external_services.salute_speech_api import create_salute_client
from database.methods.user import user_languages
from external_services.yandex_translate_api import create_yandex_translate

logger = logging.getLogger(__name__)

config = load_config()
yandex_translate = create_yandex_translate(config)

user_router = Router()

@user_router.message(F.voice)
async def handle_voice(message: types.Message, bot: Bot, config: Config):
    salute_client = create_salute_client(config)
    user_id = message.from_user.id    # Получаем язык транскрибации и перевода
    transcription_language = user_languages.get(user_id, "ru-RU")  # язык транскрибации по умолчанию - русский язык
    translation_language = user_languages.get(str(user_id) + "_translate", "en")  # Язык перевода по умолчанию - английский

    try:
        lexicon = LANG_LEXICON.get(translation_language, LEXICON_EN) # Определяем лексикон для выбранного языка перевода
        # Обработка голосового сообщения
        file = await bot.get_file(message.voice.file_id)
        wav_file = await process_voice_file(file, bot)
        transcription_result = await salute_client.audio.transcriptions.create(
            file=wav_file,
            language=transcription_language
        )
        original_text = transcription_result.text
        translated_texts = await yandex_translate.translate_text(
            texts=[original_text],
            target_language=translation_language
        )
        translated_text = translated_texts[0]

        await message.answer(
            f"{original_text}"  # Оригинальный текст
        )
        await message.answer(
            lexicon['translate_on']  #локализованное сообщение
        )
        await message.answer(
            f"{translated_text}"  #уже переведённый текст
        )

    except Exception as e:
        logger.error(f"Ошибка при транскрипции или переводе: {e}")
        await message.reply("Упс :( \n Произошла ошибка при обработке голосового сообщения.")