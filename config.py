import configparser
import os

def get_config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(BASE_DIR, filename)

    parser = configparser.ConfigParser()
    parser.optionxform = str  # Сохраняем регистр ключей
    parser.read(filename, encoding='utf-8')

    if not parser.sections():
        raise Exception(f"Файл конфигурации {filename} не найден или пуст!")

    config = {
        'db': {k: v.strip() for k, v in parser.items('postgresql')},
        'data_dir': parser.get('paths', 'data_dir'),
        'shops_count': parser.getint('network', 'shops_count'),
        'cashes_per_shop': parser.getint('network', 'cashes_per_shop'),
        # Чистим пробелы в списке категорий:
        'categories': [c.strip() for c in parser.get('categories', 'list').split(',')],
        # Чистим пробелы в ключах и значениях товаров:
        'items': {
            cat.strip(): [i.strip() for i in parser.get('items', cat).split(',')] 
            for cat in parser.options('items')
        }
    }
    return config

# переменные для использования в других скриптах
FULL_CONFIG = get_config()
DB_CONFIG = FULL_CONFIG['db']
DATA_DIR = FULL_CONFIG['data_dir']
SHOPS_COUNT = FULL_CONFIG['shops_count']
CASHES_PER_SHOP = FULL_CONFIG['cashes_per_shop']
CATEGORIES = FULL_CONFIG['categories']
ITEMS_MAP = FULL_CONFIG['items']