from aiogram import F, Router, Bot  # Импорт необходимых модулей из aiogram
from aiogram.filters import CommandStart  # Фильтр для обработки команды /start
from aiogram.types import Message, CallbackQuery  # Типы сообщений и callback-запросов
from callback_factory.callback_factory import LanguageCallbackFactory  # Фабрика для обработки callback-запросов
from database.methods.statistics import update_statistics  # Функция обновления статистики
from database.methods.user import user_languages, add_user  # Функции работы с пользователями
from lexicon.lexicon import LEXICON_RU, LANG_LEXICON  # Лексиконы для интерфейса
from keyboards.main_menu import keyboard, translation_lang_kb, get_language_keyboard  # Клавиатуры
from aiogram.fsm.context import FSMContext  # Контекст FSM для управления состояниями
from states.states import States  # Состояния FSM

# Инициализация маршрутизатора для обработки сообщений пользователей
user_router = Router()

# Обработка команды /start — первая команда, которую пользователь отправляет боту
@user_router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    """
    Обрабатывает команду /start.
    Проверяет наличие пользователя в базе данных. Если пользователь новый, добавляет его.
    Обновляет статистику и отправляет приветственное сообщение.
    """
    pool = getattr(bot, "db_pool", None)  # Получаем пул соединений с базой данных из бота
    id_bot = bot.id  # ID текущего бота
    user_id = message.from_user.id  # ID пользователя, отправившего сообщение
    username = message.from_user.username  # Имя пользователя в Telegram

    # Работа с базой данных
    async with pool.acquire() as conn:  # Захватываем соединение из пула
        # Проверяем, существует ли пользователь в базе
        existing_user = await conn.fetchrow('SELECT * FROM users WHERE id_telegram = $1', user_id)
        if not existing_user:
            # Если пользователя нет, добавляем его в базу
            await add_user(pool, username, user_id, is_premium=False, subscription_start=None, subscription_end=None)
            # Обновляем статистику для нового пользователя
            await update_statistics(pool, id_bot, total_users=1, today_users=1, total_requests=1, today_requests=1)
        else:
            # Если пользователь существует, обновляем только статистику по запросам
            await update_statistics(pool, id_bot, total_requests=1, today_requests=1)

    # Отправляем приветственное сообщение пользователю
    await message.answer(text=LEXICON_RU['/start'], reply_markup=keyboard)

# Обработка команды "Изменить язык" — переводит пользователя в состояние выбора языка
@user_router.message(F.text == "Изменить язык")
async def change_language(message: Message, state: FSMContext, bot: Bot):
    """
    Обрабатывает команду "Изменить язык".
    Отправляет пользователю список доступных языков транскрибации для выбора.
    """
    pool = getattr(bot, "db_pool", None)  # Получаем пул соединений с базой данных
    id_bot = bot.id  # ID текущего бота
    transcription_lang_kb = await get_language_keyboard(bot, message.from_user.id)  # Генерируем клавиатуру языков
    await update_statistics(pool, id_bot, total_requests=1, today_requests=1)  # Обновляем статистику

    # Устанавливаем состояние ожидания выбора языка транскрибации
    await state.set_state(States.waiting_for_language)

    # Отправляем сообщение с клавиатурой выбора языка транскрибации
    await message.answer(text=LEXICON_RU['/lang_transcrib'], reply_markup=transcription_lang_kb)

# Обработка выбора языка через callback-запрос
@user_router.callback_query(LanguageCallbackFactory.filter())
async def process_language_selection(callback: CallbackQuery, callback_data: LanguageCallbackFactory, state: FSMContext, bot: Bot):
    """
    Обрабатывает выбор языка пользователя.
    Сохраняет выбранный язык транскрибации или перевода в базе данных и обновляет состояние пользователя.
    """
    pool = getattr(bot, "db_pool", None)  # Получаем пул соединений с базой данных
    id_bot = bot.id  # ID текущего бота
    await update_statistics(pool, id_bot, total_requests=1, today_requests=1)  # Обновляем статистику

    user_id = callback.from_user.id  # ID пользователя, сделавшего выбор
    lang_code = callback_data.lang_code  # Код выбранного языка

    # Если выбран язык перевода
    if "translate" in lang_code:
        selected_translation_code = lang_code.replace("_translate", "")  # Извлекаем код языка перевода
        user_languages[f"{user_id}_translate"] = selected_translation_code  # Сохраняем язык перевода для пользователя

        # Получаем лексикон для выбранного языка перевода
        lexicon = LANG_LEXICON.get(selected_translation_code, LEXICON_RU)
        translate_message = lexicon.get(
            'lang_cng',
            f"Вы изменили язык перевода голосового сообщения на {selected_translation_code}."
        )

        # Обновляем состояние и отправляем сообщение пользователю
        await state.update_data(translation_language=selected_translation_code)
        await callback.message.edit_text(text=translate_message)
        await state.set_state(States.waiting_for_voice_message)  # Устанавливаем состояние ожидания голосового сообщения
        await callback.answer()  # Подтверждаем выбор

    else:
        # Если выбран язык транскрибации
        selected_transcription_code = lang_code
        user_languages[user_id] = selected_transcription_code  # Сохраняем язык транскрибации для пользователя

        # Получаем лексикон для выбранного языка транскрибации
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
        await callback.answer()  # Подтверждаем выбор
