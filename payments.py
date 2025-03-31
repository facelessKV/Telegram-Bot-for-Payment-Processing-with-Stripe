import stripe
from typing import Dict, Any

class StripePayment:
    def __init__(self, api_key: str):
        """Инициализируем Stripe с предоставленным ключом API"""
        # Нужно установить библиотеку stripe: pip install stripe
        stripe.api_key = api_key
    
    def create_payment(self, amount: float, description: str) -> Dict[str, Any]:
        """
        Создаем платежное намерение в Stripe.
        
        Аргументы:
            amount: Сумма платежа в USD
            description: Описание платежа
            
        Возвращает:
            Словарь с деталями платежного намерения, включая URL для оформления заказа
        """
        try:
            # Конвертируем сумму в центы (Stripe использует наименьшую единицу валюты)
            amount_cents = int(amount * 100)
            
            # Самый простой и надежный способ удаления всех не-ASCII символов
            safe_description = description.encode('ascii', 'ignore').decode('ascii')
            
            # Если после такой обработки описание стало пустым, используем стандартное
            if not safe_description:
                safe_description = "Payment"
            
            print(f"Безопасное описание для Stripe: {safe_description}")
            
            # Создаем сессию оформления заказа
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': safe_description,
                        },
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://t.me/your_bot_username?start=success',
                cancel_url='https://t.me/your_bot_username?start=cancel',
            )
        
        # Возвращаем детали платежа
        return {
            "id": checkout_session.id,
            "checkout_url": checkout_session.url,
            "amount": amount,
            "description": description,
        }
    except Exception as e:
        print(f"Ошибка при создании платежа в Stripe: {e}")
        # Возвращаем информацию об ошибке
        return {
            "error": str(e),
            "amount": amount,
            "description": description,
        }
    
    def check_payment_status(self, session_id: str) -> str:
        """
        Проверяем статус платежа в Stripe.
        
        Аргументы:
            session_id: ID сессии оформления заказа Stripe
            
        Возвращает:
            Статус платежа (succeeded, pending или failed)
        """
        try:
            # Получаем информацию о сессии
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Проверяем статус платежа
            if session.payment_status == "paid":
                return "succeeded"
            elif session.payment_status == "unpaid":
                return "pending"
            else:
                return "failed"
        except Exception as e:
            # Логируем ошибку для отладки
            print(f"Ошибка при проверке статуса платежа: {e}")
            return "error"