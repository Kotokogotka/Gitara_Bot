import sqlite3


class Database:
    def __init__(self, db_name):
        # Устанавливаем соединение с базой данных
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Включаем поддержку внешних ключей
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    # Создаем таблицу для хранения информации о клиентах
    def create_table_clients(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name VARCHAR(50),
                phone INTEGER NOT NULL,
                instrument_status VARCHAR(50),
                notes VARCHAR(255)
            )
        """)
        self.conn.commit()

    # Создаем таблицу для хранения информации о платежах
    def create_table_payments(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                payment_amount INTEGER,
                payment_date TEXT,
                payment_type VARCHAR(50),
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    # Создаем таблицу для хранения информации об уроках
    def create_table_lessons(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                lesson_date TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    # Создаем все таблицы, если они еще не существуют
    def create_all_tables(self):
        self.create_table_clients()
        self.create_table_payments()
        self.create_table_lessons()

    # Добавляем информацию о новом ученике в таблицу "clients"
    def adding_student_in_clients(self, full_name, phone, instrument_status, notes):
        self.cursor.execute("""
                    INSERT INTO clients (full_name, phone, instrument_status, notes)
                    VALUES (?, ?, ?, ?)
                """, (full_name, phone, instrument_status, notes))
        self.conn.commit()

    # Выводит id ученика и фамилию имя из таблици clients
    def get_all_clients(self):
        self.cursor.execute("""
        SELECT client_id, full_name FROM clients
        """)
        result = self.cursor.fetchall()
        return result

    # Получаем информацию о клиенте по его полному имени
    def get_info_client_in_clients(self, full_name):
        self.cursor.execute("""
        SELECT * FROM clients WHERE full_name = ?""", (full_name,))
        result = self.cursor.fetchall()
        return result

    # Удаляем запись о клиенте из основной таблицы
    def delete_client_for_name_in_clients(self, full_name):
        self.cursor.execute("""
            DELETE FROM clients WHERE full_name = ?""", (full_name,))
        self.conn.commit()

    # Добавляем информацию о новом уроке в таблицу "lessons"
    def add_lesson_in_lessons_table(self, client_id, lesson_date):
        self.cursor.execute("""
            INSERT INTO lessons (client_id, lesson_date)
            VALUES (?, ?)
            """, (client_id, lesson_date))
        self.conn.commit()

    # Получаем информацию об уроке по полному имени клиента
    def get_info_lesson_from_lessons_table(self, client_id):
        self.cursor.execute("""
        SELECT * FROM lessons WHERE client_id = ?""",
                            (client_id,))
        result = self.cursor.fetchone()
        return result

    # Удаляем запись об уроке по полному имени клиента и дате урока
    def delete_lesson_in_table_lessons(self, client_id, lesson_date):
        self.cursor.execute("""
        DELETE FROM lessons WHERE client_id = ? AND lesson_date = ?""", (client_id, lesson_date,))
        self.conn.commit()

    # Добавляем информацию о новом платеже в таблицу "payments"
    def add_payment(self, client_id, payment_amount, payment_date, payment_type):
        self.cursor.execute("""
            INSERT INTO payments (client_id, payment_amount, payment_date, payment_type) VALUES (?,?,?,?)""",
                            (client_id, payment_amount, payment_date, payment_type,))
        self.conn.commit()

    def get_payments_for_client_payments(self, client_id, month):
        # Преобразуем месяц в формат '%m'
        month_start = f"{month}-01"  # Начало месяца
        month_end = f"{month}-31"  # Конец месяца

        self.cursor.execute("""
            SELECT SUM(payment_amount) AS total_payments
            FROM payments
            WHERE client_id = ? AND SUBSTR(payment_date, 4, 2) = ?
                                  AND SUBSTR(payment_date, 1, 2) BETWEEN '01' AND '31'
        """, (client_id, month))

        result = self.cursor.fetchone()
        return result[0] if result else 0

    # Получаем общую сумму всех платежей за указанный месяц
    def get_payments_for_month(self, month_year):
        self.cursor.execute("""
                    SELECT SUM(payment_amount) AS total_payments
                    FROM payments
                    WHERE SUBSTR(payment_date, 4, 2) = ?
                """, (month_year,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    # Получение общей суммы платежей на указанный день
    def get_total_payments_by_client(self, date_payments):
        self.cursor.execute("""
            SELECT 
                c.client_id,
                c.full_name,
                SUM(p.payment_amount) AS total_payment
            FROM clients c
            LEFT JOIN payments p ON c.client_id = p.client_id
            WHERE p.payment_date = ?
            GROUP BY c.client_id, c.full_name
        """, (date_payments,))

        results = self.cursor.fetchall()
        return results


if __name__ == '__main__':
    db = Database('bad_newz.db')
    db.create_all_tables()
