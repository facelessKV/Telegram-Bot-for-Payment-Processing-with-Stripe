import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file):
        """Инициализация соединения с базой данных"""
        self.db_file = db_file
        
    def create_tables(self):
        """Создаем необходимые таблицы, если они не существуют"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Создаем таблицу платежей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            payment_id TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_payment(self, user_id, amount, description, payment_id, status):
        """Добавляем новый платеж в базу данных"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Получаем текущие дату и время
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
        INSERT INTO payments (user_id, payment_id, amount, description, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, payment_id, amount, description, status, timestamp))
        
        conn.commit()
        conn.close()
    
    def update_payment_status(self, payment_id, status):
        """Обновляем статус платежа"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE payments SET status = ? WHERE payment_id = ?
        ''', (status, payment_id))
        
        conn.commit()
        conn.close()
    
    def get_payment(self, payment_id):
        """Получаем детали платежа по payment_id"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Возвращаем строки в виде словарей
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM payments WHERE payment_id = ?
        ''', (payment_id,))
        
        payment = cursor.fetchone()
        conn.close()
        
        if payment:
            return dict(payment)
        return None
    
    def get_user_payments(self, user_id):
        """Получаем все платежи пользователя"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Возвращаем строки в виде словарей
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM payments WHERE user_id = ? ORDER BY timestamp DESC
        ''', (user_id,))
        
        payments = cursor.fetchall()
        conn.close()
        
        return [dict(payment) for payment in payments]