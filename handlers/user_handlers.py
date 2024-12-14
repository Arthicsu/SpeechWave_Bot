from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery

from callback_factory.callback_factory import LanguageCallbackFactory
from handlers.voice_handlers import user_languages
from lexicon.lexicon import LEXICON_RU, LANG_LEXICON
from keyboards.main_menu import keyboard, inline_keyboard
from aiogram.fsm.context import FSMContext
from states.states import States

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],reply_markup=keyboard)

@router.message(F.text == "Изменить язык")
async def process_change_language(message: Message, state: FSMContext):
    await state.set_state(States.waiting_for_language)
    await message.answer(text=LEXICON_RU['/lang'], reply_markup=inline_keyboard)


@router.callback_query(LanguageCallbackFactory.filter())
async def process_language_selection(callback: CallbackQuery, callback_data: LanguageCallbackFactory, state: FSMContext):
    user_id = callback.from_user.id
    selected_language_code = callback_data.lang_code
    user_languages[user_id] = selected_language_code
    lexicon = LANG_LEXICON.get(selected_language_code, LEXICON_RU)  # По умолчанию русский
    await state.update_data(language=selected_language_code)
    await state.set_state(States.waiting_for_voice_message)
    await callback.message.edit_text(
        text=lexicon.get('lang_cng')
    )
    await callback.answer()

