import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from database import Database
from payments import StripePayment
from receipts import generate_receipt

# Загружаем переменные окружения
load_dotenv()

# Получаем переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

# Состояния для ConversationHandler
AMOUNT, DESCRIPTION = range(2)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализируем базу данных и процессор платежей
db = Database("payments.db")
stripe_payment = StripePayment(STRIPE_API_KEY)

async def start(update: Update, context) -> None:
    """Отправляет приветственное сообщение при команде /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для обработки платежей.\n"
        "Используйте /pay для создания нового платежа.\n"
        "Используйте /payments для просмотра истории платежей."
    )

async def pay_command(update: Update, context) -> int:
    """Начало процесса оплаты - запрашиваем сумму"""
    await update.message.reply_text(
        "Введите сумму платежа (в USD):\n"
        "Для отмены операции используйте /cancel"
    )
    return AMOUNT

async def amount_received(update: Update, context) -> int:
    """Сохраняем сумму и запрашиваем описание"""
    try:
        amount = float(update.message.text)
        if amount <= 0:
            await update.message.reply_text("Сумма должна быть положительным числом. Попробуйте снова:")
            return AMOUNT
        
        # Сохраняем в контексте пользователя
        context.user_data["amount"] = amount
        
        await update.message.reply_text("Введите описание платежа:")
        return DESCRIPTION
    
    except ValueError:
        # Это обычно происходит, когда пользователь вводит не число
        await update.message.reply_text("Неверный формат суммы. Пожалуйста, введите число:")
        return AMOUNT

async def description_received(update: Update, context) -> int:
    """Обрабатываем платеж с указанным описанием"""
    description = update.message.text
    amount = context.user_data["amount"]
    user_id = update.effective_user.id
    
    try:
        # Создаем платеж в Stripe
        payment_intent = stripe_payment.create_payment(amount, description)
        
        # Проверяем, есть ли ошибка в результате
        if "error" in payment_intent:
            await update.message.reply_text(
                f"Произошла ошибка при создании платежа: {payment_intent['error']}\n"
                "Попробуйте использовать только английские буквы и цифры в описании."
            )
            return ConversationHandler.END
        
        # Сохраняем платеж в базе данных
        db.add_payment(
            user_id=user_id,
            amount=amount,
            description=description,
            payment_id=payment_intent["id"],
            status="pending"
        )
        
        # Создаем URL для оплаты и клавиатуру
        payment_url = payment_intent["checkout_url"]
        keyboard = [
            [InlineKeyboardButton("Оплатить", url=payment_url)],
            [InlineKeyboardButton("Проверить статус", callback_data=f"check_{payment_intent['id']}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Платеж на сумму ${amount:.2f} создан.\n"
            f"Описание: {description}\n\n"
            "Нажмите кнопку ниже, чтобы перейти к оплате:",
            reply_markup=reply_markup
        )
    except Exception as e:
        # В случае любой ошибки показываем сообщение пользователю
        await update.message.reply_text(
            f"Произошла ошибка при создании платежа: {str(e)}\n"
            "Попробуйте использовать только английские буквы и цифры или свяжитесь с администратором."
        )
        # Логируем ошибку для отладки
        logger.error(f"Ошибка при создании платежа: {str(e)}", exc_info=True)
    
    return ConversationHandler.END

async def check_payment_status(update: Update, context) -> None:
    """Проверяем и обновляем статус платежа"""
    query = update.callback_query
    await query.answer()
    
    # Извлекаем payment_id из данных обратного вызова
    payment_id = query.data.split("_")[1]
    
    # Получаем статус платежа из Stripe
    payment_status = stripe_payment.check_payment_status(payment_id)
    
    # Обновляем статус в базе данных
    db.update_payment_status(payment_id, payment_status)
    
    if payment_status == "succeeded":
        # Получаем детали платежа из базы данных
        payment = db.get_payment(payment_id)
        
        # Генерируем квитанцию
        receipt_file = generate_receipt(payment)
        
        await query.message.reply_document(
            document=receipt_file,
            caption=f"Платеж успешно выполнен!\nСумма: ${payment['amount']:.2f}\nОписание: {payment['description']}"
        )
    elif payment_status == "pending":
        await query.message.reply_text(
            "Платеж в обработке. Попробуйте проверить позже.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Проверить снова", callback_data=f"check_{payment_id}")]
            ])
        )
    else:
        await query.message.reply_text(f"Статус платежа: {payment_status}. Возможно, произошла ошибка.")

async def list_payments(update: Update, context) -> None:
    """Показываем список всех платежей пользователя"""
    user_id = update.effective_user.id
    payments = db.get_user_payments(user_id)
    
    if not payments:
        await update.message.reply_text("У вас нет платежей.")
        return
    
    message = "Ваши платежи:\n\n"
    for payment in payments:
        message += (
            f"ID: {payment['payment_id'][:8]}...\n"  # Показываем только часть ID
            f"Сумма: ${payment['amount']:.2f}\n"
            f"Описание: {payment['description']}\n"
            f"Статус: {payment['status']}\n"
            f"Дата: {payment['timestamp']}\n\n"
        )
    
    await update.message.reply_text(message)

async def cancel(update: Update, context) -> int:
    """Отменяем текущую операцию"""
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

def main() -> None:
    """Запускаем бота"""
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Создаем таблицы базы данных, если они не существуют
    db.create_tables()

    # Добавляем обработчик разговора для процесса оплаты
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("pay", pay_command)],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_received)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("payments", list_payments))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(check_payment_status, pattern="^check_"))

    # Запускаем бота
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling()

if __name__ == "__main__":
    main()