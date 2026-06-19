-- ============================================================
-- ADVANCED SQL — RFM, CLV, COHORT & WINDOW FUNCTIONS
-- Database: SQLite (ecommerce.db)
-- ============================================================


-- ─────────────────────────────────────────────────────────────
-- 1. RFM RAW METRICS (Recency, Frequency, Monetary per customer)
-- ─────────────────────────────────────────────────────────────
WITH customer_orders AS (
    SELECT
        customer_id,
        MAX(order_date)                              AS last_order_date,
        COUNT(order_id)                               AS frequency,
        ROUND(SUM(revenue), 2)                        AS monetary,
        (SELECT MAX(order_date) FROM orders WHERE status='Delivered') AS snapshot_date
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    customer_id,
    frequency,
    monetary,
    CAST((JULIANDAY(snapshot_date) - JULIANDAY(last_order_date)) AS INT) AS recency_days
FROM customer_orders
ORDER BY monetary DESC
LIMIT 20;


-- ─────────────────────────────────────────────────────────────
-- 2. CUSTOMER RANKING USING WINDOW FUNCTIONS
-- ─────────────────────────────────────────────────────────────
SELECT
    customer_id,
    ROUND(SUM(revenue), 2)                                   AS total_revenue,
    RANK()       OVER (ORDER BY SUM(revenue) DESC)           AS revenue_rank,
    NTILE(4)     OVER (ORDER BY SUM(revenue) DESC)           AS revenue_quartile,
    ROUND(
      SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (), 3
    )                                                         AS pct_of_total_revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 20;


-- ─────────────────────────────────────────────────────────────
-- 3. MONTH-OVER-MONTH REVENUE GROWTH (Window LAG function)
-- ─────────────────────────────────────────────────────────────
WITH monthly_rev AS (
    SELECT
        STRFTIME('%Y-%m', order_date) AS month,
        ROUND(SUM(revenue), 2)        AS revenue
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month)                       AS prev_month_revenue,
    ROUND(
      (revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
      / LAG(revenue) OVER (ORDER BY month), 1
    )                                                          AS mom_growth_pct
FROM monthly_rev
ORDER BY month;


-- ─────────────────────────────────────────────────────────────
-- 4. CUSTOMER LIFETIME VALUE (CLV) APPROXIMATION
-- ─────────────────────────────────────────────────────────────
WITH customer_metrics AS (
    SELECT
        customer_id,
        COUNT(order_id)                          AS total_orders,
        ROUND(SUM(revenue), 2)                   AS total_revenue,
        ROUND(AVG(revenue), 2)                   AS avg_order_value,
        CAST(
          (JULIANDAY(MAX(order_date)) - JULIANDAY(MIN(order_date))) / 365.0
          AS REAL
        )                                          AS customer_lifespan_years
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_orders,
    avg_order_value,
    total_revenue,
    ROUND(
      avg_order_value *
      (total_orders / (customer_lifespan_years + 0.08)) -- avoid div/0
    , 2)                                          AS estimated_annual_clv
FROM customer_metrics
ORDER BY estimated_annual_clv DESC
LIMIT 20;


-- ─────────────────────────────────────────────────────────────
-- 5. COHORT RETENTION (first purchase month vs activity)
-- ─────────────────────────────────────────────────────────────
WITH first_purchase AS (
    SELECT customer_id, MIN(STRFTIME('%Y-%m', order_date)) AS cohort_month
    FROM orders WHERE status='Delivered'
    GROUP BY customer_id
),
activity AS (
    SELECT
        o.customer_id,
        fp.cohort_month,
        STRFTIME('%Y-%m', o.order_date) AS order_month
    FROM orders o
    JOIN first_purchase fp ON o.customer_id = fp.customer_id
    WHERE o.status = 'Delivered'
)
SELECT
    cohort_month,
    COUNT(DISTINCT customer_id)                                  AS cohort_customers,
    COUNT(DISTINCT CASE WHEN order_month > cohort_month
          THEN customer_id END)                                   AS retained_customers,
    ROUND(
      COUNT(DISTINCT CASE WHEN order_month > cohort_month
            THEN customer_id END) * 100.0
      / COUNT(DISTINCT customer_id), 1
    )                                                              AS retention_pct
FROM activity
GROUP BY cohort_month
ORDER BY cohort_month;


-- ─────────────────────────────────────────────────────────────
-- 6. PRODUCT AFFINITY (frequently bought together — simplified)
-- ─────────────────────────────────────────────────────────────
SELECT
    a.product_id   AS product_a,
    b.product_id   AS product_b,
    COUNT(*)        AS times_bought_together
FROM order_items a
JOIN order_items b
    ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY times_bought_together DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- 7. RUNNING TOTAL OF REVENUE (Window function — cumulative sum)
-- ─────────────────────────────────────────────────────────────
SELECT
    STRFTIME('%Y-%m', order_date)             AS month,
    ROUND(SUM(revenue), 2)                     AS monthly_revenue,
    ROUND(
      SUM(SUM(revenue)) OVER (ORDER BY STRFTIME('%Y-%m', order_date)), 2
    )                                           AS cumulative_revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY month
ORDER BY month;
