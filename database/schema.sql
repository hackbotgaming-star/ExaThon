-- SIGNALFIRE AI: Relational Schema for Retail Operations
-- Compatible with Exasol Personal and DuckDB

-- 1. Sales
CREATE TABLE IF NOT EXISTS sales (
    sale_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sale_date DATE NOT NULL,
    region VARCHAR(30) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    units_sold INTEGER NOT NULL
);

-- 2. Orders
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    region VARCHAR(30) NOT NULL,
    channel VARCHAR(30) NOT NULL,
    order_total DECIMAL(12, 2) NOT NULL,
    status VARCHAR(30) NOT NULL
);

-- 3. Deliveries
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    carrier VARCHAR(50) NOT NULL,
    dispatch_date DATE NOT NULL,
    delivery_date DATE,
    promised_days INTEGER NOT NULL,
    actual_days INTEGER,
    delay_days INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL,
    region VARCHAR(30) NOT NULL
);

-- 4. Customer Complaints
CREATE TABLE IF NOT EXISTS customer_complaints (
    complaint_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50),
    complaint_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    region VARCHAR(30) NOT NULL,
    resolution_status VARCHAR(30) NOT NULL
);

-- 5. Refunds
CREATE TABLE IF NOT EXISTS refunds (
    refund_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    refund_date DATE NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    reason VARCHAR(100) NOT NULL,
    region VARCHAR(30) NOT NULL
);

-- 6. Inventory
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    snapshot_date DATE NOT NULL,
    region VARCHAR(30) NOT NULL,
    stock_level INTEGER NOT NULL,
    reorder_threshold INTEGER NOT NULL,
    stockout_flag INTEGER NOT NULL
);

-- 7. Suppliers
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id VARCHAR(50) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    lead_time_days INTEGER NOT NULL,
    defect_rate_pct DECIMAL(5, 2) NOT NULL,
    reliability_score DECIMAL(5, 2) NOT NULL
);

-- 8. Customer Retention
CREATE TABLE IF NOT EXISTS customer_retention (
    cohort_id VARCHAR(50) PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    region VARCHAR(30) NOT NULL,
    active_customers INTEGER NOT NULL,
    repeat_purchase_rate DECIMAL(6, 4) NOT NULL,
    churn_rate DECIMAL(6, 4) NOT NULL
);

-- 9. Investigations & Findings Tracking
CREATE TABLE IF NOT EXISTS investigations (
    investigation_id VARCHAR(50) PRIMARY KEY,
    finding_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    suspected_cause VARCHAR(500),
    verified_conclusion VARCHAR(1000),
    notes VARCHAR(2000),
    updated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL
);
