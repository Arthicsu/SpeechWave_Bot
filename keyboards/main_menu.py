from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from callback_factory.callback_factory import LanguageCallbackFactory

menu_kb_builder = ReplyKeyboardBuilder()
menu_kb_builder.row(
    KeyboardButton(text="Изменить язык"),
    KeyboardButton(text="Приобрести премиум"),
    width=2
)
keyboard = menu_kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Клавиатура для выбора языка транскрибации
transcription_lang_kb_builder = InlineKeyboardBuilder()
transcription_lang_kb_builder.row(
    InlineKeyboardButton(
        text="Russian",
        callback_data=LanguageCallbackFactory(lang_code="ru").pack()
    ),
    InlineKeyboardButton(
        text="English",
        callback_data=LanguageCallbackFactory(lang_code="en").pack()
    ),
    InlineKeyboardButton(
        text="Kazakh",
        callback_data=LanguageCallbackFactory(lang_code="kz").pack()
    ),
    width=3
)

transcription_lang_kb = transcription_lang_kb_builder.as_markup()

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


