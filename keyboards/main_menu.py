from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

menu_kb_builder = ReplyKeyboardBuilder()
menu_kb_builder.row(
    KeyboardButton(text="Изменить язык"),
    KeyboardButton(text="Приобрести премиум"),
    width=2
)
keyboard = menu_kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

lang_kb_builder = InlineKeyboardBuilder()
lang_kb_builder.row(
    InlineKeyboardButton(text="Russian", callback_data="lang_ru"),
    InlineKeyboardButton(text="English", callback_data="lang_en"),
    InlineKeyboardButton(text="Kazakh", callback_data="lang_kz"),
    width=3
)
lang_kb_builder.row(
    InlineKeyboardButton(text="German", callback_data="lang_de"),
    InlineKeyboardButton(text="Spanish", callback_data="lang_es"),
    InlineKeyboardButton(text="French", callback_data="lang_fr"),
    width=3
)
inline_keyboard = lang_kb_builder.as_markup()