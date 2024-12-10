from aiogram import F, Router, Bot, types
from aiogram.methods.send_invoice import SendInvoice
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType, CallbackQuery
from keyboards.pay_menu import pay_btn_bldr

router = Router()

@router.message(F.text == "Приобрести премиум")
async def process_purchase_premium(message: Message):
    await message.answer(
        text="Для получения премиум-статуса нажмите кнопку ниже и завершите оплату.",
        reply_markup=pay_btn_bldr.as_markup()
    )

@router.callback_query(F.data == "pay_premium")
async def send_invoice(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Покупка премиум-подписки",
        description="Получите доступ к премиум-статусу для переводчика голосовых сообщений.",
        payload="Payment through a bot",
        provider_token="401643678:TEST:7e898c39-8a0e-4077-b18a-93d0fad639b3",
        currency="rub",
        prices=[
            LabeledPrice(
                label="Покупка премиум-подписки на языки перевода",
                amount=100_00
            ),
            LabeledPrice(
                label="НДС",
                amount=50_00
            ),
            LabeledPrice(
                label="Скидка",
                amount=100_00
            )
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000],
        start_parameter="premium",
        provider_data=None,
        photo_url="https://s.iimg.su/s/05/th_1TszqSOT9R87yPk3FYBfk2pTtiIanqz6jhK3lMxd.jpg",
        photo_size=10,
        photo_width=512,
        photo_height=512,
        need_name=True,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        request_timeout=15
    )
    await callback.answer()

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    total_amount = message.successful_payment.total_amount / 100
    await message.answer(
        text=f"Спасибо за оплату {total_amount} {message.successful_payment.currency}! Ваш премиум-статус активирован."
    )


    # admin_id = 123456789
    # await message.bot.send_message(
    #     chat_id=admin_id,
    #     text=f"Пользователь {message.from_user.full_name} (ID: {user_id}) приобрёл премиум-статус."
    # )