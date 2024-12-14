from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from callback_factory.callback_factory import LanguageCallbackFactory

menu_kb_builder = ReplyKeyboardBuilder()
menu_kb_builder.row(
    KeyboardButton(text="Изменить язык"),
    KeyboardButton(text="Приобрести премиум"),
    width=2
)
keyboard = menu_kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

lang_kb_builder = InlineKeyboardBuilder()

lang_kb_builder.row(
    InlineKeyboardButton(
        text="Русский",
        callback_data=LanguageCallbackFactory(lang_code="ru").pack()
    ),
    InlineKeyboardButton(
        text="Английский",
        callback_data=LanguageCallbackFactory(lang_code="en").pack()
    ),
    InlineKeyboardButton(
        text="Казахский",
        callback_data=LanguageCallbackFactory(lang_code="kz").pack()
    ),
    width=3
)
lang_kb_builder.row(
    InlineKeyboardButton(
        text="Немецкий",
        callback_data=LanguageCallbackFactory(lang_code="de").pack()
    ),
    InlineKeyboardButton(
        text="Испанский",
        callback_data=LanguageCallbackFactory(lang_code="es").pack()
    ),
    InlineKeyboardButton(
        text="Французский",
        callback_data=LanguageCallbackFactory(lang_code="fr").pack()
    ),
    width=3
)
inline_keyboard = lang_kb_builder.as_markup()
