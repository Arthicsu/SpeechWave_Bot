from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from callback_factory.callback_factory import LanguageCallbackFactory
from database.methods.user import get_subscription_status

menu_kb_builder = ReplyKeyboardBuilder()
menu_kb_builder.row(
    KeyboardButton(text="Изменить язык"),
    KeyboardButton(text="Приобрести премиум"),
    width=2
)
keyboard = menu_kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Клавиатура для выбора языка транскрибации
async def get_language_keyboard(bot, user_id):
    """
    Создаёт клавиатуру для выбора языка транскрибации.
    """
    # Проверяем премиум-статус пользователя
    pool = getattr(bot, "db_pool", None)
    is_premium, subscription_end = await get_subscription_status(pool, user_id)

    # Создаём клавиатуру
    transcription_lang_kb_builder = InlineKeyboardBuilder()

    # Добавляем базовые кнопки
    transcription_lang_kb_builder.row(
        InlineKeyboardButton(
            text="Russian",
            callback_data=LanguageCallbackFactory(lang_code="ru").pack()
        ),
        InlineKeyboardButton(
            text="English",
            callback_data=LanguageCallbackFactory(lang_code="en").pack()
        ),
        width=3
    )

    # Если пользователь премиум, добавляем дополнительные языки
    if is_premium:
        transcription_lang_kb_builder.row(
            InlineKeyboardButton(
                text="Kazakh",
                callback_data=LanguageCallbackFactory(lang_code="kz").pack()
            )
        )

    # Возвращаем объект InlineKeyboardMarkup
    transcription_lang_kb = transcription_lang_kb_builder.as_markup()
    return transcription_lang_kb


# Клавиатура для выбора языка перевода
translation_lang_kb_builder = InlineKeyboardBuilder()
translation_lang_kb_builder.row(
    InlineKeyboardButton(
        text="Russian",
        callback_data=LanguageCallbackFactory(lang_code="ru_translate").pack()
    ),
    InlineKeyboardButton(
        text="English",
        callback_data=LanguageCallbackFactory(lang_code="en_translate").pack()
    ),
    InlineKeyboardButton(
        text="Kazakh",
        callback_data=LanguageCallbackFactory(lang_code="kz_translate").pack()
    ),
    width=3
)
translation_lang_kb_builder.row(
    InlineKeyboardButton(
        text="German",
        callback_data=LanguageCallbackFactory(lang_code="de_translate").pack()
    ),
    InlineKeyboardButton(
        text="Spanish",
        callback_data=LanguageCallbackFactory(lang_code="es_translate").pack()
    ),
    InlineKeyboardButton(
        text="French",
        callback_data=LanguageCallbackFactory(lang_code="fr_translate").pack()
    ),
    width=3
)
translation_lang_kb = translation_lang_kb_builder.as_markup()


