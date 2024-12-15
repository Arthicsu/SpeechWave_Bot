from aiogram.filters.callback_data import CallbackData

class LanguageCallbackFactory(CallbackData, prefix="lang"):
    lang_code: str