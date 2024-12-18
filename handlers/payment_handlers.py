from aiogram import F, Router, Bot  # Импортируем необходимые модули из aiogram
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType, CallbackQuery  # Импорт типов данных для работы с сообщениями, оплатами и callback-запросами
from datetime import datetime, timedelta  # Импортируем модули для работы с датами и временем
from keyboards.pay_menu import pay_btn_bldr  # Импортируем генератор клавиатуры для оплаты
from database.methods.user import add_user, get_subscription_status  # Импортируем функции для работы с пользователями и подписками

# Создание маршрутизатора для обработки сообщений пользователей
user_router = Router()

# Обработка сообщения с текстом "Приобрести премиум"
@user_router.message(F.text == "Приобрести премиум")
async def process_purchase_premium(message: Message, bot: Bot):
    """
    Обрабатывает запрос пользователя на приобретение премиум-статуса.
    Если у пользователя уже есть активная подписка, сообщает об этом.
    Если подписки нет, отправляет кнопку для оплаты.
    """
    pool = getattr(bot, "db_pool", None)  # Получаем пул соединений с базой данных из бота
    user_id = message.from_user.id  # Получаем ID пользователя

    # Получаем статус подписки пользователя
    is_premium, subscription_end = await get_subscription_status(pool, user_id)
    if is_premium:
        # Если подписка активна, отправляем информацию о дате окончания подписки
        subscription_end_date = datetime.strptime(
            str(subscription_end), "%Y-%m-%d %H:%M:%S.%f"
        ).strftime('%d-%m-%Y')  # Форматируем дату окончания подписки
        await message.answer(
            text=f"У Вас уже приобретена подписка.\nПодписка действует до {subscription_end_date}."
        )
    else:
        # Если подписки нет, отправляем сообщение с кнопкой для оплаты
        await message.answer(
            text="Для получения премиум-статуса нажмите кнопку ниже и завершите оплату.",
            reply_markup=pay_btn_bldr.as_markup()  # Кнопка для оплаты
        )


# Обработка callback-запроса, когда пользователь нажимает кнопку "pay_premium"
@user_router.callback_query(F.data == "pay_premium")
async def send_invoice(callback: CallbackQuery, bot: Bot):
    """
    Отправляет пользователю счет для оплаты премиум-подписки.
    """
    await bot.send_invoice(
        chat_id=callback.message.chat.id,  # ID чата, в который отправляется счет
        title="Покупка премиум-подписки",  # Название товара (счета)
        description="Получите доступ к премиум-статусу для переводчика голосовых сообщений.",  # Описание товара
        payload="Payment through a bot",  # Данные для передачи
        provider_token="401643678:TEST:7e898c39-8a0e-4077-b18a-93d0fad639b3",  # Токен платежного провайдера
        currency="rub",  # Валюта
        prices=[  # Цены, включая НДС и скидку
            LabeledPrice(
                label="Покупка премиум-подписки на языки перевода",
                amount=100_00  # 100 рублей
            ),
            LabeledPrice(
                label="НДС",
                amount=50_00  # 50 рублей
            ),
            LabeledPrice(
                label="Скидка",
                amount=100_00  # 100 рублей скидки
            )
        ],
        max_tip_amount=5000,  # Максимальная сумма чаевых
        suggested_tip_amounts=[1000, 2000, 3000],  # Рекомендуемые суммы чаевых
        start_parameter="premium",  # Параметр, который будет передан при успешной оплате
        provider_data=None,  # Дополнительные данные от провайдера (не используются)
        photo_url="https://s.iimg.su/s/05/th_1TszqSOT9R87yPk3FYBfk2pTtiIanqz6jhK3lMxd.jpg",  # URL изображения для счета
        photo_size=10,  # Размер фото (в данном случае это просто пример)
        photo_width=512,  # Ширина фото
        photo_height=512,  # Высота фото
        need_name=True,  # Запрашивать ли имя пользователя
        need_phone_number=False,  # Запрашивать ли номер телефона
        need_email=False,  # Запрашивать ли email
        need_shipping_address=False,  # Запрашивать ли адрес доставки
        request_timeout=15  # Время ожидания ответа от пользователя
    )
    await callback.answer()  # Подтверждаем обработку callback-запроса

# Обработка предоплаты (когда пользователь нажимает на кнопку оплаты)
@user_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    """
    Обрабатывает предоплату, отвечая на запрос подтверждения.
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # Подтверждаем предоплату

# Обработка успешной оплаты
@user_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message, bot: Bot):
    """
    Обрабатывает успешную оплату, активирует премиум-статус и обновляет данные пользователя.
    """
    pool = getattr(bot, "db_pool", None)  # Получаем пул соединений с базой данных
    user_id = message.from_user.id  # Получаем ID пользователя
    username = message.from_user.username  # Получаем имя пользователя
    subscription_start = datetime.now()  # Дата начала подписки
    subscription_end = subscription_start + timedelta(days=30)  # Подписка активируется на 30 дней

    # Добавляем или обновляем пользователя в базе данных
    await (add_user
        (
        pool,
        username=username,
        id_telegram=user_id,
        is_premium=True,  # Устанавливаем флаг премиум-подписки
        subscription_start=subscription_start,
        subscription_end=subscription_end
       )
    )

    # Извлекаем сумму успешной оплаты и отправляем подтверждение пользователю
    total_amount = message.successful_payment.total_amount / 100  # Сумма оплаты в рублях
    await message.answer(
        text=f"Спасибо за оплату {total_amount} {message.successful_payment.currency}! Ваш премиум-статус активирован на 1 месяц."
    )