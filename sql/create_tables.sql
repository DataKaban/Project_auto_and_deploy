-- public.categories определение

-- Drop table

-- DROP TABLE public.categories;

CREATE TABLE public.categories (
	id serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	CONSTRAINT categories_name_key UNIQUE (name),
	CONSTRAINT categories_pkey PRIMARY KEY (id)
);


-- public.shops определение

-- Drop table

-- DROP TABLE public.shops;

CREATE TABLE public.shops (
	id int4 NOT NULL,
	"name" varchar(255) DEFAULT 'Адрес не указан'::character varying NULL,
	CONSTRAINT shops_pkey PRIMARY KEY (id)
);


-- public.cashes определение

-- Drop table

-- DROP TABLE public.cashes;

CREATE TABLE public.cashes (
	id serial4 NOT NULL,
	cash_num int4 NOT NULL,
	shop_id int4 NULL,
	CONSTRAINT cashes_cash_num_shop_id_key UNIQUE (cash_num, shop_id),
	CONSTRAINT cashes_pkey PRIMARY KEY (id),
	CONSTRAINT cashes_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES public.shops(id)
);


-- public.products определение

-- Drop table

-- DROP TABLE public.products;

CREATE TABLE public.products (
	id serial4 NOT NULL,
	"name" varchar(255) NOT NULL,
	category_id int4 NULL,
	CONSTRAINT products_name_key UNIQUE (name),
	CONSTRAINT products_pkey PRIMARY KEY (id),
	CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id)
);


-- public.sales определение

-- Drop table

-- DROP TABLE public.sales;

CREATE TABLE public.sales (
	id serial4 NOT NULL,
	doc_id varchar(50) NOT NULL,
	product_id int4 NULL,
	cash_id int4 NULL,
	amount int4 NOT NULL,
	price numeric(10, 2) NOT NULL,
	discount numeric(10, 2) DEFAULT 0 NULL,
	sale_date date NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT sales_pkey PRIMARY KEY (id),
	CONSTRAINT sales_cash_id_fkey FOREIGN KEY (cash_id) REFERENCES public.cashes(id),
	CONSTRAINT sales_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id)
);