import psycopg2
from psycopg2 import extras

class PGDatabase:
    def __init__(self, host, port, database, user, password):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=int(port),
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            self.connection.autocommit = True
            print("✅ Подключение к PostgreSQL (psycopg2) установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            raise

    def execute(self, query, args=None):
        try:
            self.cursor.execute(query, args)
            # Если запрос предполагает возврат данных (например, SELECT)
            if self.cursor.description:
                return self.cursor.fetchone()
            return None
        except Exception as e:
            print(f"❌ Ошибка SQL: {e}")
            return None

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("🔌 Соединение закрыто")

# Тестирование подключения при запуске скрипта напрямую
if __name__ == "__main__":
    from config import DB_CONFIG
    print("Проверка подключения (psycopg2)...")
    db = PGDatabase(**DB_CONFIG)
    res = db.execute("SELECT version();")
    print(f"Версия базы: {res[0]}")
    db.close()