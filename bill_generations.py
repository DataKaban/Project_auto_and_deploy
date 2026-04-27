# Скрипт для генерации файлов продаж

import pandas as pd
import random
import os
import uuid
from datetime import datetime, timedelta

# импорт настроек из config.ini
from config import DATA_DIR, CATEGORIES, ITEMS_MAP, SHOPS_COUNT, CASHES_PER_SHOP

def generate_sales_data(shops_config):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    for shop_id, active_cashes in shops_config.items():
        for cash_num in active_cashes:
            rows = []
            # Генерируем от 1 до 10 чеков на каждую активную кассу
            for _ in range(random.randint(1, 10)):
                doc_id = str(uuid.uuid4())[:8]
                for _ in range(random.randint(1, 4)):
                    category = random.choice(CATEGORIES).strip()
                    items_list = ITEMS_MAP.get(category)
                    
                    if not items_list:
                        print(f"Категория '{category}' не найдена в ITEMS_MAP")
                        continue
                        
                    item = random.choice(items_list).strip()
                    
                    rows.append([
                        doc_id, item, category, 
                        random.randint(1, 5), #Случайное количество от 1 до 5
                        random.randint(1, 5000), # Случайная цена от 1 до 5000
                        random.choice([0, 0, 0, 5, 10, 25, 50]), # Случайная скидка (0% чаще, чем другие)
                        yesterday
                    ])

            df = pd.DataFrame(rows, columns=['doc_id', 'item', 'category', 'amount', 'price', 'discount', 'date'])
            file_name = f"{shop_id}_{cash_num}.csv"
            file_path = os.path.join(DATA_DIR, file_name)
            df.to_csv(file_path, index=False, encoding='utf-8')
            print(f"Файл создан: {file_path}")

    # БЛОК ОПРЕДЕЛЕНИЯ ПЛАНА ГЕНЕРАЦИИ
if __name__ == "__main__":
    #  Обходим все магазины от 1 до SHOPS_COUNT
    shops_plan = {}
    for shop_id in range(1, SHOPS_COUNT + 1):
        active_cashes = []
        # Максимальное количество активных касс сегодня для этого магазина (от 1 до CASHES_PER_SHOP)
        max_cashes_today = random.randint(1, CASHES_PER_SHOP)
        
        for cash_num in range(1, max_cashes_today + 1):
            if random.random() < 0.8:
                active_cashes.append(cash_num)
        
        if not active_cashes:
            active_cashes.append(1)
            
        shops_plan[shop_id] = active_cashes
    
    print(f"--- Запуск генерации ---")
    print(f"Сеть: {SHOPS_COUNT} магазинов. Папка: {DATA_DIR}")
    generate_sales_data(shops_plan)
    print("--- Готово ---")