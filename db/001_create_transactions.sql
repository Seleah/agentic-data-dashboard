CREATE TABLE stores (
    store_id VARCHAR(5) PRIMARY KEY
);

CREATE TABLE categories (
    category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name TEXT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL REFERENCES categories(category_id)
);

CREATE TABLE transactions (
    transaction_id VARCHAR(9) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    store_id VARCHAR(5) NOT NULL REFERENCES stores(store_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price > 0),
    discount_percent NUMERIC(5, 2) NOT NULL
        CHECK (discount_percent >= 0 AND discount_percent <= 100),
    transaction_type TEXT NOT NULL
        CHECK (transaction_type IN ('sale', 'return'))
);
