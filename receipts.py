import os
from datetime import datetime
from typing import Dict, Any
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_receipt(payment_data: Dict[str, Any]) -> str:
    """
    Генерируем PDF-квитанцию для платежа.
    
    Аргументы:
        payment_data: Словарь с деталями платежа
        
    Возвращает:
        Путь к сгенерированному PDF-файлу
    """
    # Создаем временный файл для квитанции
    # Нужно установить reportlab: pip install reportlab
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_filename = temp_file.name
    temp_file.close()
    
    # Получаем текущие дату и время для квитанции
    receipt_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Создаем PDF с помощью ReportLab
    c = canvas.Canvas(temp_filename, pagesize=letter)
    width, height = letter
    
    # Добавляем заголовок
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, height - inch, "Квитанция об оплате")
    
    # Добавляем информацию о квитанции
    c.setFont("Helvetica", 12)
    
    # Номер квитанции и дата
    c.drawString(inch, height - 1.5*inch, f"Квитанция №: {payment_data['id']}")
    c.drawString(inch, height - 1.8*inch, f"Дата: {receipt_date}")
    
    # Детали платежа
    c.drawString(inch, height - 2.3*inch, "Детали платежа:")
    c.drawString(inch + 0.2*inch, height - 2.6*inch, f"Сумма: ${payment_data['amount']:.2f} USD")
    c.drawString(inch + 0.2*inch, height - 2.9*inch, f"Описание: {payment_data['description']}")
    c.drawString(inch + 0.2*inch, height - 3.2*inch, f"Статус: {payment_data['status'].upper()}")
    c.drawString(inch + 0.2*inch, height - 3.5*inch, f"Дата платежа: {payment_data['timestamp']}")
    
    # Подвал
    c.setFont("Helvetica", 10)
    c.drawString(inch, inch, "Спасибо за ваш платеж!")
    
    # Сохраняем PDF
    c.save()
    
    return temp_filename