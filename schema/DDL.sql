CREATE DATABASE IF NOT EXISTS fintech_app;
USE fintech_app;

-- 1. Table for users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table for standard financial transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Let's insert a mock user to test our Python bridge shortly
INSERT INTO users (username, email) VALUES ('rajdeep_kumar', 'rajdeep@example.com');

USE fintech_app;

-- 1. Create a table for Service Providers / Merchants
CREATE TABLE merchants (
    merchant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) DEFAULT 'Digital Service',
    support_email VARCHAR(100)
);

-- 2. Create a catalog of available premium sub packages
CREATE TABLE subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id INT,
    plan_name VARCHAR(50) NOT NULL,
    billing_cycle ENUM('monthly', 'yearly') DEFAULT 'monthly',
    cost DECIMAL(10, 2) NOT NULL,
    -- Database Validation: Prevent input errors or negative charges
    CONSTRAINT chk_positive_cost CHECK (cost >= 0.00),
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE
);

-- 3. The Junction Table: Manages the Many-to-Many connection between Users and Subscriptions
CREATE TABLE user_subscriptions (
    user_id INT,
    subscription_id INT,
    start_date DATE NOT NULL,
    next_billing_date DATE NOT NULL,
    status ENUM('active', 'paused', 'cancelled') DEFAULT 'active',
    PRIMARY KEY (user_id, subscription_id),
    -- Referential Integrity: If a user deletes an account, clean up their subscriptions automatically
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id) ON DELETE RESTRICT
);