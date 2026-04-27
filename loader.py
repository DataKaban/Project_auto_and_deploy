## Загрузка файлов в базу данных

import os
import re  # Импортируем регулярные выражения
import pandas as pd
from config import DB_CONFIG, DATA_DIR
from db_client import PGDatabase

def load_data():
    db = PGDatabase(**DB_CONFIG)
    
    file_pattern = re.compile(r"^\d+_\d+\.csv$")
    
    # Фильтруем файлы: и расширение .csv, и соответствие маске цифра_цифра
    files = [f for f in os.listdir(DATA_DIR) if file_pattern.match(f)]
    
    if not files:
        print(f"В папке {DATA_DIR} не найдено файлов, подходящих под маску 'цифра_цифра.csv'")
        return

    print(f"Найдено подходящих файлов: {len(files)}")

    for filename in files:
        # Теперь мы на 100% уверены, что в имени есть цифры и подчеркивание
        parts = filename.replace('.csv', '').split('_')
        shop_id = int(parts[0])
        cash_num = int(parts[1])
        
        df = pd.read_csv(os.path.join(DATA_DIR, filename))
        
        # 1. Магазин
        db.execute(
            "INSERT INTO shops (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
            (shop_id, f"Магазин №{shop_id}")
        )
        
        # 2. Касса
        db.execute(
            "INSERT INTO cashes (shop_id, cash_num) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (shop_id, cash_num)
        )
        
        # Получаем ID кассы
        cash_res = db.execute(
            "SELECT id FROM cashes WHERE shop_id = %s AND cash_num = %s",
            (shop_id, cash_num)
        )
        cash_id = cash_res[0]

        for _, row in df.iterrows():
            # 3. Категория
            db.execute("INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (row['category'],))
            cat_id = db.execute("SELECT id FROM categories WHERE name = %s", (row['category'],))[0]
            
            # 4. Товар
            db.execute("INSERT INTO products (name, category_id) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING", (row['item'], cat_id))
            prod_id = db.execute("SELECT id FROM products WHERE name = %s", (row['item'],))[0]
            
            # 5. Продажа
            db.execute(
                """INSERT INTO sales (cash_id, product_id, doc_id, amount, price, discount, sale_date) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (cash_id, prod_id, row['doc_id'], row['amount'], row['price'], row['discount'], row['date'])
            )
            
        print(f"Файл {filename} загружен")

        ##Удаляем файл после загрузки
        file_path = os.path.join(DATA_DIR, filename)
        os.remove(file_path)
        print(f"Файл {filename} удален")


    db.close()
    print("\n--- ЗАГРУЗКА ЗАВЕРШЕНА ---")

if __name__ == "__main__":
    load_data()
    
