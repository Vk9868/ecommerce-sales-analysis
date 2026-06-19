-- ============================================================
-- E-COMMERCE SALES ANALYSIS — SQL QUERIES
-- Author  : [Your Name]
-- Database: SQLite (ecommerce.db)
-- ============================================================


-- ─────────────────────────────────────────────────────────────
-- 1. OVERALL BUSINESS KPIs
-- ─────────────────────────────────────────────────────────────
SELECT
    COUNT(DISTINCT o.order_id)       AS total_orders,
    COUNT(DISTINCT o.customer_id)    AS unique_customers,
    ROUND(SUM(o.revenue), 2)         AS total_revenue,
    ROUND(AVG(o.revenue), 2)         AS avg_order_value,
    ROUND(SUM(oi.profit), 2)         AS total_profit,
    ROUND(SUM(oi.profit)*100.0 /
          NULLIF(SUM(o.revenue),0),2) AS profit_margin_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Delivered';


-- ─────────────────────────────────────────────────────────────
-- 2. MONTHLY REVENUE TREND (2023–2024)
-- ─────────────────────────────────────────────────────────────
SELECT
    STRFTIME('%Y-%m', order_date)    AS month,
    COUNT(order_id)                  AS total_orders,
    ROUND(SUM(revenue), 2)           AS monthly_revenue,
    ROUND(AVG(revenue), 2)           AS avg_order_value
FROM orders
WHERE status = 'Delivered'
GROUP BY month
ORDER BY month;


-- ─────────────────────────────────────────────────────────────
-- 3. TOP 10 PRODUCTS BY REVENUE
-- ─────────────────────────────────────────────────────────────
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity)                 AS units_sold,
    ROUND(SUM(oi.total), 2)          AS total_revenue,
    ROUND(SUM(oi.profit), 2)         AS total_profit,
    ROUND(AVG(p.rating), 1)          AS avg_rating
FROM order_items oi
JOIN products p   ON oi.product_id = p.product_id
JOIN orders   o   ON oi.order_id   = o.order_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- 4. REVENUE BY CATEGORY
-- ─────────────────────────────────────────────────────────────
SELECT
    p.category,
    COUNT(DISTINCT o.order_id)       AS orders,
    SUM(oi.quantity)                 AS units_sold,
    ROUND(SUM(oi.total), 2)          AS revenue,
    ROUND(SUM(oi.profit), 2)         AS profit,
    ROUND(SUM(oi.profit)*100.0 /
          NULLIF(SUM(oi.total),0),1) AS margin_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders   o ON oi.order_id   = o.order_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 5. CUSTOMER SEGMENT ANALYSIS
-- ─────────────────────────────────────────────────────────────
SELECT
    c.segment,
    COUNT(DISTINCT o.order_id)                         AS total_orders,
    COUNT(DISTINCT o.customer_id)                      AS customers,
    ROUND(SUM(o.revenue), 2)                           AS total_revenue,
    ROUND(SUM(o.revenue)/COUNT(DISTINCT o.customer_id),2) AS revenue_per_customer,
    ROUND(AVG(o.revenue), 2)                           AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.segment
ORDER BY total_revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 6. CITY-WISE PERFORMANCE
-- ─────────────────────────────────────────────────────────────
SELECT
    o.city,
    COUNT(DISTINCT o.order_id)   AS orders,
    COUNT(DISTINCT o.customer_id) AS customers,
    ROUND(SUM(o.revenue), 2)     AS revenue,
    ROUND(AVG(o.revenue), 2)     AS avg_order_value
FROM orders o
WHERE o.status = 'Delivered'
GROUP BY o.city
ORDER BY revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 7. ORDER STATUS DISTRIBUTION
-- ─────────────────────────────────────────────────────────────
SELECT
    status,
    COUNT(*)                         AS count,
    ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM orders), 1) AS pct
FROM orders
GROUP BY status
ORDER BY count DESC;


-- ─────────────────────────────────────────────────────────────
-- 8. PAYMENT METHOD PREFERENCE
-- ─────────────────────────────────────────────────────────────
SELECT
    payment_method,
    COUNT(*)                  AS orders,
    ROUND(SUM(revenue), 2)    AS revenue,
    ROUND(AVG(revenue), 2)    AS avg_order_value
FROM orders
WHERE status = 'Delivered'
GROUP BY payment_method
ORDER BY orders DESC;


-- ─────────────────────────────────────────────────────────────
-- 9. REPEAT CUSTOMERS (COHORT INSIGHT)
-- ─────────────────────────────────────────────────────────────
WITH customer_orders AS (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN order_count = 1  THEN '1 Order (One-time)'
        WHEN order_count <= 3 THEN '2–3 Orders'
        WHEN order_count <= 6 THEN '4–6 Orders'
        ELSE '7+ Orders (Loyal)'
    END                        AS customer_type,
    COUNT(*)                   AS customers,
    ROUND(AVG(order_count),1)  AS avg_orders
FROM customer_orders
GROUP BY customer_type
ORDER BY avg_orders;


-- ─────────────────────────────────────────────────────────────
-- 10. QUARTER-OVER-QUARTER GROWTH
-- ─────────────────────────────────────────────────────────────
SELECT
    STRFTIME('%Y', order_date)                    AS year,
    'Q' || CAST((CAST(STRFTIME('%m', order_date) AS INT)+2)/3 AS TEXT) AS quarter,
    COUNT(order_id)                               AS orders,
    ROUND(SUM(revenue), 2)                        AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY year, quarter
ORDER BY year, quarter;
