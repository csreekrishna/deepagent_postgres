-- Sample Data for DeepAgent Testing
-- This creates a realistic e-commerce-like database with multiple related tables

-- Create Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    country VARCHAR(50),
    city VARCHAR(50)
);

-- Create Categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    description TEXT,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT,
    payment_method VARCHAR(50)
);

-- Create Order Items table
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL
);

-- Create Reviews table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    product_id INTEGER REFERENCES products(product_id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified_purchase BOOLEAN DEFAULT FALSE
);

-- Insert sample data

-- Insert Categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Books', 'Physical and digital books'),
('Clothing', 'Apparel and fashion items'),
('Home & Garden', 'Home improvement and gardening supplies'),
('Sports & Outdoors', 'Sports equipment and outdoor gear'),
('Toys & Games', 'Toys, games, and entertainment'),
('Health & Beauty', 'Health, wellness, and beauty products'),
('Automotive', 'Car parts and automotive supplies');

-- Insert Users
INSERT INTO users (username, email, first_name, last_name, date_of_birth, country, city) VALUES
('john_doe', 'john.doe@email.com', 'John', 'Doe', '1985-03-15', 'USA', 'New York'),
('jane_smith', 'jane.smith@email.com', 'Jane', 'Smith', '1990-07-22', 'Canada', 'Toronto'),
('mike_johnson', 'mike.j@email.com', 'Mike', 'Johnson', '1988-11-08', 'USA', 'Los Angeles'),
('emily_brown', 'emily.brown@email.com', 'Emily', 'Brown', '1992-04-18', 'UK', 'London'),
('david_wilson', 'david.w@email.com', 'David', 'Wilson', '1987-09-12', 'Australia', 'Sydney'),
('sarah_davis', 'sarah.davis@email.com', 'Sarah', 'Davis', '1991-12-03', 'USA', 'Chicago'),
('alex_miller', 'alex.miller@email.com', 'Alex', 'Miller', '1989-06-25', 'Germany', 'Berlin'),
('lisa_taylor', 'lisa.taylor@email.com', 'Lisa', 'Taylor', '1986-01-30', 'France', 'Paris'),
('tom_anderson', 'tom.anderson@email.com', 'Tom', 'Anderson', '1993-08-14', 'USA', 'Seattle'),
('maria_garcia', 'maria.garcia@email.com', 'Maria', 'Garcia', '1990-05-07', 'Spain', 'Madrid');

-- Insert Products
INSERT INTO products (product_name, category_id, price, stock_quantity, description, is_featured) VALUES
-- Electronics
('iPhone 15 Pro', 1, 999.99, 50, 'Latest Apple smartphone with advanced features', TRUE),
('Samsung Galaxy S24', 1, 899.99, 45, 'Premium Android smartphone', TRUE),
('MacBook Air M2', 1, 1199.99, 30, 'Lightweight laptop with M2 chip', TRUE),
('Sony WH-1000XM5', 1, 299.99, 75, 'Noise-cancelling wireless headphones', FALSE),
('iPad Pro 12.9"', 1, 1099.99, 25, 'Professional tablet for creative work', FALSE),

-- Books
('The Great Gatsby', 2, 12.99, 100, 'Classic American novel by F. Scott Fitzgerald', FALSE),
('Python Programming', 2, 45.99, 60, 'Comprehensive guide to Python programming', TRUE),
('Data Science Handbook', 2, 39.99, 40, 'Essential resource for data scientists', FALSE),
('The Art of War', 2, 8.99, 80, 'Ancient Chinese military treatise', FALSE),
('Clean Code', 2, 42.99, 35, 'A handbook of agile software craftsmanship', TRUE),

-- Clothing
('Nike Air Max', 3, 129.99, 90, 'Popular running shoes', TRUE),
('Levi''s 501 Jeans', 3, 89.99, 120, 'Classic straight-leg jeans', FALSE),
('North Face Jacket', 3, 199.99, 65, 'Weather-resistant outdoor jacket', TRUE),
('Adidas T-Shirt', 3, 24.99, 150, 'Comfortable cotton t-shirt', FALSE),
('Ray-Ban Sunglasses', 3, 149.99, 40, 'Classic aviator sunglasses', FALSE),

-- Home & Garden
('KitchenAid Mixer', 4, 299.99, 30, 'Professional stand mixer for baking', TRUE),
('Dyson Vacuum V15', 4, 449.99, 20, 'Powerful cordless vacuum cleaner', TRUE),
('Garden Tool Set', 4, 79.99, 55, 'Complete set of gardening tools', FALSE),
('Smart Thermostat', 4, 199.99, 35, 'WiFi-enabled programmable thermostat', FALSE),
('LED Desk Lamp', 4, 49.99, 70, 'Adjustable LED desk lamp', FALSE),

-- Sports & Outdoors
('Yoga Mat', 5, 29.99, 100, 'Non-slip exercise mat', FALSE),
('Tennis Racket', 5, 149.99, 25, 'Professional-grade tennis racket', FALSE),
('Hiking Backpack', 5, 89.99, 40, '40L hiking backpack with multiple compartments', TRUE),
('Basketball', 5, 24.99, 60, 'Official size basketball', FALSE),
('Camping Tent', 5, 199.99, 15, '4-person waterproof camping tent', TRUE);

-- Insert Orders
INSERT INTO orders (user_id, status, total_amount, shipping_address, payment_method) VALUES
(1, 'completed', 1199.99, '123 Main St, New York, NY 10001', 'credit_card'),
(2, 'completed', 342.98, '456 Oak Ave, Toronto, ON M5V 3A8', 'paypal'),
(3, 'pending', 129.99, '789 Pine St, Los Angeles, CA 90210', 'credit_card'),
(4, 'shipped', 89.99, '321 High St, London, UK EC1A 1BB', 'debit_card'),
(5, 'completed', 549.98, '654 George St, Sydney, NSW 2000', 'credit_card'),
(1, 'completed', 79.99, '123 Main St, New York, NY 10001', 'credit_card'),
(6, 'pending', 299.99, '987 Lake Shore Dr, Chicago, IL 60611', 'paypal'),
(7, 'completed', 199.99, '147 Unter den Linden, Berlin, 10117', 'credit_card'),
(8, 'shipped', 149.99, '258 Champs-Élysées, Paris, 75008', 'paypal'),
(9, 'completed', 74.98, '369 Pine St, Seattle, WA 98101', 'credit_card');

-- Insert Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
-- Order 1: MacBook Air
(1, 3, 1, 1199.99, 1199.99),
-- Order 2: Sony Headphones + Python Book
(2, 4, 1, 299.99, 299.99),
(2, 7, 1, 45.99, 45.99),
-- Order 3: Nike Shoes
(3, 11, 1, 129.99, 129.99),
-- Order 4: Levi's Jeans
(4, 12, 1, 89.99, 89.99),
-- Order 5: KitchenAid + Yoga Mat
(5, 16, 1, 299.99, 299.99),
(5, 21, 1, 29.99, 29.99),
-- Order 6: Garden Tools
(6, 18, 1, 79.99, 79.99),
-- Order 7: KitchenAid Mixer
(7, 16, 1, 299.99, 299.99),
-- Order 8: Ray-Ban Sunglasses
(8, 15, 1, 149.99, 149.99),
-- Order 9: Adidas T-Shirt + Basketball
(9, 14, 2, 24.99, 49.98),
(9, 24, 1, 24.99, 24.99);

-- Insert Reviews
INSERT INTO reviews (user_id, product_id, rating, review_text, is_verified_purchase) VALUES
(1, 3, 5, 'Excellent laptop, very fast and lightweight. Perfect for development work.', TRUE),
(2, 4, 4, 'Great noise cancellation, comfortable for long listening sessions.', TRUE),
(2, 7, 5, 'Best Python book I''ve read. Clear explanations and practical examples.', TRUE),
(4, 12, 4, 'Good quality jeans, fit as expected. Classic style.', TRUE),
(5, 16, 5, 'Amazing mixer! Makes baking so much easier. Highly recommend.', TRUE),
(5, 21, 4, 'Good yoga mat, non-slip surface works well.', TRUE),
(7, 16, 5, 'Love this mixer! Built like a tank and works perfectly.', TRUE),
(8, 15, 3, 'Stylish sunglasses but a bit overpriced for what you get.', TRUE),
(9, 14, 4, 'Comfortable t-shirt, good quality cotton.', TRUE),
(1, 1, 5, 'iPhone 15 Pro is incredible. Camera quality is outstanding.', FALSE),
(3, 11, 5, 'Most comfortable running shoes I''ve ever owned!', FALSE),
(6, 2, 4, 'Great Android phone, battery life is excellent.', FALSE);

-- Create some indexes for better query performance
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Add some constraints
ALTER TABLE products ADD CONSTRAINT chk_price_positive CHECK (price > 0);
ALTER TABLE products ADD CONSTRAINT chk_stock_non_negative CHECK (stock_quantity >= 0);
ALTER TABLE order_items ADD CONSTRAINT chk_quantity_positive CHECK (quantity > 0);
ALTER TABLE order_items ADD CONSTRAINT chk_unit_price_positive CHECK (unit_price > 0);

-- Create a view for order summaries
CREATE VIEW order_summary AS
SELECT 
    o.order_id,
    u.username,
    u.first_name,
    u.last_name,
    o.order_date,
    o.status,
    o.total_amount,
    COUNT(oi.order_item_id) as item_count
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, u.username, u.first_name, u.last_name, o.order_date, o.status, o.total_amount
ORDER BY o.order_date DESC;

-- Create a view for product statistics
CREATE VIEW product_stats AS
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    p.price,
    p.stock_quantity,
    COUNT(r.review_id) as review_count,
    ROUND(AVG(r.rating), 2) as avg_rating,
    COUNT(oi.order_item_id) as times_ordered,
    SUM(oi.quantity) as total_quantity_sold
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN reviews r ON p.product_id = r.product_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, c.category_name, p.price, p.stock_quantity
ORDER BY total_quantity_sold DESC NULLS LAST;