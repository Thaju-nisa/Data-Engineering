# Food Delivery Analytics — Project

## 1. Scenario
Three messy exports have landed from different systems (App/CRM, Orders/Payments, Restaurant Partner Catalog). Build a
**Bronze → Silver → Gold** pipeline and finish with a dashboard an ops manager could use to track
daily business health.

## 2. The three datasets

| File | Rows | Grain | Notes |
|---|---|---|---|
| `delivery_customers_messy.csv` | ~1,000 | 1 row per customer | App/CRM export |
| `delivery_orders_messy.csv` | ~10,000 | 1 row per order | Orders/Payments export |
| `delivery_restaurants_messy.csv` | ~16 | 1 row per restaurant | Restaurant partner catalog, deliberately small so students can eyeball every issue |

Keys: `orders.customer_id → customers.customer_id`, `orders.restaurant_id → restaurants.restaurant_id`.

## 3. Known data quality issues (answer key / rubric)

Have students discover most of this themselves first — via `display()`, `.describe()`,
`dbutils.data.summarize()`, and `GROUP BY` counts — before you hand over this list.

### `delivery_customers_messy.csv`
- **Inconsistent casing** in `membership_status` (`Gold`/`gold`, `Silver`/`silver`, `Regular`/`regular`, plus a `Basic` tier that doesn't fit the pattern).
- **Duplicate `customer_id`s** (~18 rows) — needs a dedup rule (e.g. keep latest by `signup_date`).
- **Mixed date formats** in `date_of_birth` and `signup_date` (`DD-MM-YYYY`, `MM/DD/YYYY`, `YYYY/MM/DD`, `YYYY-MM-DD` all mixed within the same column).
- **`phone`** mixes real numbers, the literal string `not_available`, and blanks.
- **`wallet_balance`** mixes numeric values with junk strings (`"fifty"`, `"zero"`, `"na"`, blank) — needs cast-with-null-handling, not a hard cast.
- **City/state mismatches** — a handful of customers have a state that doesn't match their city, same "reference data conformance" issue as before.

### `delivery_orders_messy.csv`
- **`order_status` casing**: `Delivered` vs `delivered`, plus `Cancelled`, `Returned`, `Failed` — needs standardization and a decision on which statuses count as real revenue.
- **Negative `items_count`** (data entry errors, or should they mean something like "removed items"?) — students must decide a rule.
- **`order_value` is `"err"` in ~45% of rows** — needs cast-to-null-on-failure so the pipeline doesn't crash, plus a decision on how to impute or exclude these for revenue calcs.
- **`total_amount` is entirely blank** — must be **derived** in Silver/Gold as `order_value + delivery_fee - (order_value * discount)`, same pattern as the retail project's `total_amount`.
- **Missing `restaurant_id`** (~2% of rows) — orphaned orders that won't join to the restaurant dimension.
- **Mixed date formats** in `order_date` again.
- **`delivery_time_mins`** mixes numbers with `"na"` and blanks.
- **Blank `payment_method`** for some rows.
- **`cuisine_type` on the order table is intentionally noisy/random** — reinforces that cuisine should come from the restaurant dimension, never re-derived from the transactional table.

### `delivery_restaurants_messy.csv`
- **Cuisine casing inconsistent** (`American`/`american`, `Continental`/`continental`, etc.) — standardize once here.
- **A duplicate restaurant row** (`R004` "Noodle House" appears twice, with cuisine `Mexican` vs `MEXICAN`) — dedup on `restaurant_id` after normalizing text case.
- **`cost_for_two`** mixes numbers with the string `not_available`.
- **`avg_delivery_time_mins`** mixes numbers with `"na"`.
- **`is_active`** is wildly inconsistent: `Yes`/`yes`/`Y`, `No`/`N`, and even `1`/`0` — great exercise in mapping many representations to one boolean.
- **Leading/trailing whitespace** in some `restaurant_name` values (e.g. `" Taco Fiesta "`).
- **Occasional missing `rating`**.

## 4. Medallion architecture design

### Bronze (raw ingestion)
Load each CSV as-is into Delta, one table per source, adding `_ingest_timestamp` and `_source_file`. No cleaning.
`bronze.customers_raw`, `bronze.orders_raw`, `bronze.restaurants_raw`.

### Silver (cleaned, conformed, deduplicated)
- Standardize casing (`membership_status`, `order_status`, `cuisine_type`, `is_active`, `payment_method`).
- Parse all date columns robustly (coalesce across multiple `to_date` format attempts).
- Cast numeric columns with null-on-failure (`order_value`, `wallet_balance`, `cost_for_two`, `delivery_time_mins`, `avg_delivery_time_mins`).
- Deduplicate customers and restaurants on their business key.
- Map `is_active` to a true boolean.
- Derive `total_amount` in orders.
- Result: `silver.customers`, `silver.orders`, `silver.restaurants` — clean, one row per business key, correct types.

### Gold (business-ready, star schema)
- `gold.dim_customer`, `gold.dim_restaurant`, `gold.dim_date`
- `gold.fact_orders` at the order grain, FK'd to the dimensions, excluding/flagging cancelled or orphaned orders.
- Pre-aggregated helper tables for dashboard speed: `gold.daily_order_summary`, `gold.cuisine_performance`, `gold.restaurant_performance`.

## 5. Suggested dashboard (final deliverable)
Build with **Databricks Lakeview Dashboards** on top of the Gold tables.

Suggested tiles:
- **KPI cards**: Total Orders, Total Revenue, Active Customers, Average Order Value, Average Delivery Time
- **Orders trend** — line chart, orders/revenue by day or week (tests date parsing)
- **Cuisine performance** — bar chart of revenue by cuisine type (tests cuisine standardization)
- **Order status breakdown** — donut of Delivered vs Cancelled vs Returned vs Failed (tests status cleaning)
- **Payment method mix** — bar chart including an "Unknown" bucket (tests null handling)
- **Top restaurants** — ranked table by revenue and by order count
- **City-wise performance** — revenue by city (tests city/state conformance fix)
- **Delivery time distribution** — histogram (tests numeric cleaning of `delivery_time_mins`)
- Filters for date range, city, and cuisine
