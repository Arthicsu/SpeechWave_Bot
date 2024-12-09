from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
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


@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    selected_language_code = callback.data.split("_")[1]
    lexicon = LANG_LEXICON.get(selected_language_code, LEXICON_RU)  # По умолчанию русский
    await state.update_data(language=selected_language_code)
    await state.set_state(States.waiting_for_voice_message)
    await callback.message.edit_text(
        text=lexicon.get('lang_cng')
    )
    await callback.answer()


# @router.message(TranslationState.waiting_for_voice_message, F.content_type == ContentType.VOICE)
# async def process_voice_message(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     language = user_data.get("language", "ru")  # Дефолтный — русский
#     lexicon = LANGUAGE_LEXICON.get(language, LEXICON_RU)
#
#     await message.answer(
#         text=f"Ваше голосовое сообщение переведено на {language.upper()}."
#     )
