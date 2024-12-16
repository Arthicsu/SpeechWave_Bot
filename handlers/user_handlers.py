from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from callback_factory.callback_factory import LanguageCallbackFactory
from database.methods.statistics import update_statistics
from database.methods.user import user_languages, add_user
from lexicon.lexicon import LEXICON_RU, LANG_LEXICON
from keyboards.main_menu import keyboard, transcription_lang_kb, translation_lang_kb
from aiogram.fsm.context import FSMContext
from states.states import States
from datetime import datetime, date
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    pool = getattr(bot, "db_pool", None)
    id_bot = bot.id
    user_id = message.from_user.id
    username = message.from_user.username

    async with pool.acquire() as conn:
        # Проверяем, существует ли пользователь
        existing_user = await conn.fetchrow('SELECT * FROM users WHERE id_telegram = $1', user_id)
        if not existing_user:
            # Добавляем нового пользователя
            await add_user(pool, username, user_id, is_premium=False, subscription_start=None, subscription_end=None)

            # Обновляем статистику пользователей
            await update_statistics(pool, id_bot, total_users=1, today_users=1)
        else:
            # Если пользователь существует, обновляем только другие метрики
            await update_statistics(pool, id_bot, total_requests=1, today_requests=1)

    # Отправляем ответ пользователю
    await message.answer(text=LEXICON_RU['/start'], reply_markup=keyboard)


@router.message(F.text == "Изменить язык")
async def change_language(message: Message, state: FSMContext, bot: Bot):
    pool = getattr(bot, "db_pool", None)
    id_bot = bot.id
    await update_statistics(pool, id_bot, total_requests=1, today_requests=1)
    await state.set_state(States.waiting_for_language)
    await message.answer(text=LEXICON_RU['/lang_transcrib'], reply_markup=transcription_lang_kb)

@router.callback_query(LanguageCallbackFactory.filter())
async def process_language_selection(callback: CallbackQuery, callback_data: LanguageCallbackFactory, state: FSMContext, bot: Bot):
    pool = getattr(bot, "db_pool", None)
    id_bot = bot.id
    await update_statistics(pool, id_bot, total_requests=1, today_requests=1)
    user_id = callback.from_user.id
    lang_code = callback_data.lang_code

    if "translate" in lang_code:
        # Обработка выбора языка перевода
        selected_translation_code = lang_code.replace("_translate", "")
        user_languages[f"{user_id}_translate"] = selected_translation_code

        # Используем лексикон перевода, если доступен
        lexicon = LANG_LEXICON.get(selected_translation_code, LEXICON_RU)
        translate_message = lexicon.get(
            'lang_cng',
            f"Вы изменили язык перевода голосового сообщения на {selected_translation_code}."
        )

        await state.update_data(translation_language=selected_translation_code)
        await callback.message.edit_text(
            text=translate_message
        )
        await state.set_state(States.waiting_for_voice_message)
        await callback.answer()

    else:
        # Обработка выбора языка транскрибации
        selected_transcription_code = lang_code
        user_languages[user_id] = selected_transcription_code

        # Используем лексикон транскрибации
        lexicon = LANG_LEXICON.get(selected_transcription_code, LEXICON_RU)
        transcription_message = lexicon.get(
            'lang_cng',
            f"Вы изменили язык транскрибации на {selected_transcription_code}."
        )

        # Переход к выбору языка перевода
        await callback.message.edit_text(
            text="Отлично!\nТеперь выберите язык перевода голосового сообщения:",
            reply_markup=translation_lang_kb
        )
        await callback.answer()