
-- 1. Справочник магазинов
CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY,
    address VARCHAR(255) DEFAULT 'Адрес не указан'
);

-- 2. Справочник касс
CREATE TABLE IF NOT EXISTS cashes (
    id SERIAL PRIMARY KEY,
    cash_num INTEGER NOT NULL,
    shop_id INTEGER REFERENCES shops(id),
    UNIQUE(cash_num, shop_id) 
);

-- 3. Справочник категорий
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 4. Справочник товаров
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category_id INTEGER REFERENCES categories(id)
);

-- 5. Таблица фактов: Продажи
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    doc_id VARCHAR(50) NOT NULL,
    product_id INTEGER REFERENCES products(id),
    cash_id INTEGER REFERENCES cashes(id),
    amount INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    discount NUMERIC(10, 2) DEFAULT 0,
    sale_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


