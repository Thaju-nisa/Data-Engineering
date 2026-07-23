"""
Food Delivery Analytics
Converted from FoodDeliveryAnalysis.ipynb (Databricks notebook)
Generated as a lightweight, output-free .py script for version control.
"""


# ----------------------------------------------------------------------
# # Food Delivery Analytics
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# ## 1. Scenario
# Three messy exports have landed from different systems (App/CRM, Orders/Payments, Restaurant Partner Catalog). Build a
# **Bronze → Silver → Gold** pipeline and finish with a dashboard an ops manager could use to track
# daily business health.
#
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# ## 2. The three datasets
#
# | File | Rows | Grain | Notes |
# |---|---|---|---|
# | `delivery_customers_messy.csv` | ~1,000 | 1 row per customer | App/CRM export |
# | `delivery_orders_messy.csv` | ~10,000 | 1 row per order | Orders/Payments export |
# | `delivery_restaurants_messy.csv` | ~16 | 1 row per restaurant | Restaurant partner catalog, deliberately small so students can eyeball every issue |
#
# Keys: `orders.customer_id → customers.customer_id`, `orders.restaurant_id → restaurants.restaurant_id`.
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# ## 3. Known data quality issues
#
# Have students discover most of this themselves first — via `display()`, `.describe()`,
# `dbutils.data.summarize()`, and `GROUP BY` counts — before you hand over this list.
# ----------------------------------------------------------------------

import pandas as pd
import numpy as np          
import pyspark.sql.functions as F
#delivery_customers_messy.csv
df_dcustomermessy_bronze=spark.read.format("csv").option("header","true").option("inferSchema","true").load("/Volumes/fooddeliveryanalytics/basic/rawdata/delivery_customers_messy.csv")
df_dcustomermessy_bronze.display()
df_dcustomermessy_bronze.describe()
#dbutils.data.summarize(df_dcustomermessy)
df_dcustomermessy_bronze.groupBy("customer_id").count().display()

#delivery_orders_messy.csv
df_dordersmessy_bronze=spark.read.format("csv").option("header","true").option("inferSchema","true").load("/Volumes/fooddeliveryanalytics/basic/rawdata/delivery_orders_messy.csv")
df_dordersmessy_bronze.display()
df_dordersmessy_bronze.describe()
#dbutils.data.summarize(df_dordersmessy)
df_dordersmessy_bronze.groupBy("order_id").count().display()

#delivery_orders_messy.csv
df_drestaurantmessy_bronze=spark.read.format("csv").option("header","true").option("inferSchema","true").load("/Volumes/fooddeliveryanalytics/basic/rawdata/delivery_restaurants_messy.csv")
df_drestaurantmessy_bronze.display()
df_drestaurantmessy_bronze.describe()
#dbutils.data.summarize(df_drestaurantmessy)
df_drestaurantmessy_bronze.groupBy("restaurant_id").count().display()

# ----------------------------------------------------------------------
#
# Add Ingestion metadata
# ----------------------------------------------------------------------

from pyspark.sql.functions import current_timestamp

df_dcustomermessy_bronze = (df_dcustomermessy_bronze.withColumn('ingest_time', current_timestamp()))
df_dordersmessy_bronze = (df_dordersmessy_bronze.withColumn('ingest_time', current_timestamp()))
df_drestaurantmessy_bronze = (df_drestaurantmessy_bronze.withColumn('ingest_time', current_timestamp()))

# ----------------------------------------------------------------------
# ##Save As Delta Table in Bronze_Layer
# ----------------------------------------------------------------------

df_dcustomermessy_bronze.write.format('delta').mode('overwrite').saveAsTable('fooddeliveryanalytics.bronze.bronze_customer')
df_dordersmessy_bronze.write.format('delta').mode('overwrite').saveAsTable('fooddeliveryanalytics.bronze.bronze_orders')
df_drestaurantmessy_bronze.write.format('delta').mode('overwrite').saveAsTable('fooddeliveryanalytics.bronze.bronze_restaurant')

# ----------------------------------------------------------------------
# ### `delivery_customers_messy.csv`
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#  **Inconsistent casing** in `membership_status` (`Gold`/`gold`, `Silver`/`silver`, `Regular`/`regular`, plus a `Basic` tier that doesn't fit the pattern).[](url)
# ----------------------------------------------------------------------

bronze_customer = spark.read.table('fooddeliveryanalytics.bronze.bronze_customer')
bronze_orders = spark.read.table('fooddeliveryanalytics.bronze.bronze_orders')
bronze_restaurant = spark.read.table('fooddeliveryanalytics.bronze.bronze_restaurant')

# ----------------------------------------------------------------------
# **Mixed date formats** in `date_of_birth` and `signup_date`
# ----------------------------------------------------------------------

from pyspark.sql.functions import try_to_date, col, coalesce

df_silver_customer1 = bronze_customer.withColumn(
    'date_of_birth',
    coalesce(
        try_to_date(col('date_of_birth'),'yyyy-MM-dd'),
        try_to_date(col('date_of_birth'),'dd-MM-yyyy'),
        try_to_date(col('date_of_birth'),'yyyy-MM-dd'),
        try_to_date(col('date_of_birth'),'MM-dd-yyyy'),
        try_to_date(col('date_of_birth'),'MM/dd/yyyy'),
        try_to_date(col('date_of_birth'),'yyyy/MM/dd'),
        try_to_date(col('date_of_birth'),'dd/MM/yyyy')
    )
)



df_silver_customer1.display()

df_silver_customer = df_silver_customer1.withColumn(
    'signup_date',
    coalesce(
        try_to_date(col('signup_date'),'yyyy-MM-dd'),
        try_to_date(col('signup_date'),'dd-MM-yyyy'),
        try_to_date(col('signup_date'),'yyyy-MM-dd'),
        try_to_date(col('signup_date'),'MM-dd-yyyy'),
        try_to_date(col('signup_date'),'MM/dd/yyyy'),
        try_to_date(col('signup_date'),'yyyy/MM/dd'),
        try_to_date(col('signup_date'),'dd/MM/yyyy')
    )
)




df_silver_customer.display()

df_silver_customer.select('membership_status').distinct().display()

from pyspark.sql.functions import upper, trim,when, col

df_silver_customer = df_silver_customer.withColumn(
    "membership_status",
    upper(trim(col("membership_status")))
)


df_silver_customer = df_silver_customer.withColumn(
        'membership_status',when(col('membership_status')=='gold','Gold').
        when(col('membership_status')=='regular','Regular').
        when(col('membership_status')=='silver','Silver').
        otherwise(col('membership_status')))


df_silver_customer = df_silver_customer.withColumn(
        'membership_status',when(col('membership_status')=='BASIC','REGULAR').
        otherwise(col('membership_status')))

df_silver_customer.select('membership_status').distinct().display()

# ----------------------------------------------------------------------
# **Duplicate `customer_id`s**
# ----------------------------------------------------------------------

from pyspark.sql.functions import count ,countDistinct

df_silver_customer.select(count('customer_id'),countDistinct('customer_id')).display()

df_silver_customer = df_silver_customer.dropDuplicates(['customer_id'])

from pyspark.sql.functions import count ,countDistinct

df_silver_customer.select(count('customer_id'),countDistinct('customer_id')).display()

# ----------------------------------------------------------------------
# **`phone`** mixes real numbers, the literal string `not_available`, and blanks.
# ----------------------------------------------------------------------

df_silver_customer = df_silver_customer.withColumn(
        'phone',when(col('phone')=='not_available',None).
        otherwise(col('phone')))

df_silver_customer.display()

# ----------------------------------------------------------------------
# **`wallet_balance`** mixes numeric values with junk strings (`"fifty"`, `"zero"`, `"na"`, blank)
# ----------------------------------------------------------------------

df_silver_customer = df_silver_customer.withColumn(
        'wallet_balance',when(col('wallet_balance')=='na','0').
        when(col('wallet_balance')=='zero','0').
        when(col('wallet_balance').isNull(),'0').
        when(col('wallet_balance')=='fifty','50').
        otherwise(col('wallet_balance')))

df_silver_customer.display()

# ----------------------------------------------------------------------
# **City/state mismatches** — a handful of customers have a state that doesn't match their city, same "reference data conformance" issue as before.
# ----------------------------------------------------------------------

from pyspark.sql import Row

reference_data = [
    Row(city="Kochi", state="Kerala"),
    Row(city="Chennai", state="Tamil Nadu"),
    Row(city="Bengaluru", state="Karnataka"),
    Row(city="Mumbai", state="Maharashtra"),
    Row(city="Hyderabad", state="Telangana")
]

df_reference = spark.createDataFrame(reference_data)

from pyspark.sql.window import Window
import pyspark.sql.functions as F

city_state_mode = (
    df_silver_customer.groupBy("city", "state").count()
      .withColumn(
          "rn",
          F.row_number().over(
              Window.partitionBy("city").orderBy(F.desc("count"))
          )
      )
      .filter(F.col("rn") == 1)
      .select(
          F.col("city").alias("_city"),
          F.col("state").alias("state_mode")
      )
)

df_silver_customer = (
    df_silver_customer.alias("c")
      .join(
          city_state_mode.alias("m"),
          F.col("c.city") == F.col("m._city"),
          "left"
      )
      .withColumn(
          "state",
          F.coalesce(F.col("m.state_mode"), F.col("c.state"))
      )
      .drop("_city", "state_mode")
)

df_silver_customer = df_silver_customer.withColumnRenamed("state", "old_state")

df_silver_customer = (
    df_silver_customer.join(city_state_mode, df_silver_customer.city == city_state_mode._city, "left")
      .withColumn(
          "state",
          F.coalesce(F.col("state_mode"), F.col("old_state"))
      )
      .drop("_city", "state_mode", "old_state")
)

df_silver_customer = df_silver_customer.select(
    "customer_id",
    "customer_name",
    "email",
    "phone",
    "gender",
    "date_of_birth",
    "city",
    "state",
    "signup_date",
    "wallet_balance",
    "membership_status",
    "ingest_time"
)

df_silver_customer = (
    df_silver_customer.alias("c")
    .join(
        city_state_mode.alias("m"),
        F.col("c.city") == F.col("m._city"),
        "left"
    )
    .withColumn(
        "correct_state",
        F.coalesce(F.col("m.state_mode"), F.col("c.state"))
    )
)

df_silver_customer = (
    df_silver_customer
    .drop("state", "_city", "state_mode")
    .withColumnRenamed("correct_state", "state")
)

df_silver_customer.display()

# ----------------------------------------------------------------------
# ### `delivery_orders_messy.csv`
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# **`order_status` casing**: `Delivered` vs `delivered`, plus `Cancelled`, `Returned`, `Failed`
# ----------------------------------------------------------------------

silver_order_df=bronze_orders.select('order_id','order_date','customer_id','restaurant_id','restaurant_name','cuisine_type','items_count','order_value','delivery_fee','discount','total_amount','payment_method','delivery_time_mins','order_status','ingest_time')

silver_order_df.select('order_status').distinct().display()

from pyspark.sql.functions import col,when


silver_order_df = silver_order_df.withColumn(
        'order_status',when(col('order_status')=='delivered','Delivered').
        otherwise(col('order_status')))

silver_order_df.display()

df_revenue = silver_order_df.filter(
    F.col("order_status") == "Delivered"
)

df_revenue.select(
    F.sum("total_amount").alias("order_value")
).show()

# ----------------------------------------------------------------------
# **Negative `items_count`** (data entry errors, or should they mean something like "removed items"?) — students must decide a rule.
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.filter(
 col("items_count") >= 0
)

silver_order_df.display()

# ----------------------------------------------------------------------
# **`order_value` is `"err"` in ~45% of rows** — needs cast-to-null-on-failure so the pipeline doesn't crash, plus a decision on how to impute or exclude these for revenue calcs.
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.withColumn(
        'order_value',when(col('order_value')=='err',None).
        otherwise(col('order_value')))

silver_order_df = silver_order_df.withColumn(
    "order_value",
    F.col("order_value").cast("double")
)

silver_order_df.display()

df_revenue = silver_order_df.filter(
    F.col("order_value").isNotNull()
)

silver_order_df = silver_order_df.fillna(
    {"order_value": 0}
)

# ----------------------------------------------------------------------
# - **`total_amount` is entirely blank** — must be **derived** in Silver/Gold as `order_value + delivery_fee - (order_value * discount)`, same pattern as the retail project's `total_amount`.
# ----------------------------------------------------------------------

from pyspark.sql import functions as F

silver_order_df = (
    silver_order_df
    .withColumn("order_value", F.expr("try_cast(order_value AS DOUBLE)"))
    .withColumn("delivery_fee", F.col("delivery_fee").cast("double"))
    .withColumn("discount", F.col("discount").cast("double"))
)

silver_order_df = silver_order_df.withColumn(
    "total_amount",
    F.col("order_value")
    + F.col("delivery_fee")
    - (F.col("order_value") * F.col("discount"))
)
silver_order_df.display()

# ----------------------------------------------------------------------
# **Missing `restaurant_id`**
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.fillna(
    {"restaurant_id": "UNKNOWN"}
)
silver_order_df.display()

# ----------------------------------------------------------------------
#  **Mixed date formats** in `order_date`
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.withColumn(
    'order_date',
    coalesce(
        try_to_date(col('order_date'),'yyyy-MM-dd'),
        try_to_date(col('order_date'),'dd-MM-yyyy'),
        try_to_date(col('order_date'),'yyyy-MM-dd'),
        try_to_date(col('order_date'),'MM-dd-yyyy'),
        try_to_date(col('order_date'),'MM/dd/yyyy'),
        try_to_date(col('order_date'),'yyyy/MM/dd'),
        try_to_date(col('order_date'),'dd/MM/yyyy')
    )
)




silver_order_df.display()

# ----------------------------------------------------------------------
# **`delivery_time_mins`** mixes numbers with `"na"` and blanks.
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.withColumn(
        'delivery_time_mins',when(col('delivery_time_mins')=='na','0').
        when(col('delivery_time_mins').isNull(),'0').
        otherwise(col('delivery_time_mins')))

silver_order_df.display()

# ----------------------------------------------------------------------
# **Blank `payment_method`** for some rows.
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.withColumn(
        'payment_method',when(col('payment_method').isNull(),'Unknown').
        otherwise(col('payment_method')))

silver_order_df.display()

# ----------------------------------------------------------------------
#  **`cuisine_type` on the order table is intentionally noisy/random**
# ----------------------------------------------------------------------

silver_order_df = silver_order_df.join(
    bronze_restaurant,
    "restaurant_id",
    "left"
)

silver_order_df.display()

bronze_restaurant.cuisine_type

silver_order_df.display()

# ----------------------------------------------------------------------
# ### `delivery_restaurants_messy.csv`
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# **Cuisine casing inconsistent** (`American`/`american`, `Continental`/`continental`, etc.)
# ----------------------------------------------------------------------

silver_restaurant_df=bronze_restaurant.select('restaurant_id','restaurant_name','cuisine_type','city','rating','avg_delivery_time_mins','cost_for_two','is_active','ingest_time')
silver_restaurant_df.display()

from pyspark.sql import functions as F

silver_restaurant_df = silver_restaurant_df.withColumn(
    "cuisine_type",
    F.initcap(F.col("cuisine_type"))
)
silver_restaurant_df.display()

# ----------------------------------------------------------------------
# **A duplicate restaurant row**
# ----------------------------------------------------------------------

from pyspark.sql.functions import count, countDistinct

silver_restaurant_df.select(count('restaurant_id'),countDistinct('restaurant_id')).display()

silver_restaurant_df = silver_restaurant_df.dropDuplicates()

from pyspark.sql.functions import count, countDistinct

silver_restaurant_df.select(count('restaurant_id'),countDistinct('restaurant_id')).display()

# ----------------------------------------------------------------------
# **`cost_for_two`** mixes numbers with the string `not_available`.
# ----------------------------------------------------------------------

silver_restaurant_df.select("cost_for_two").distinct().display()

silver_restaurant_df = silver_restaurant_df.withColumn(
    "cost_for_two",
    when((col("cost_for_two")) == "not_available",
        None
    ).otherwise(col("cost_for_two")))

from pyspark.sql import functions as F

silver_restaurant_df = silver_restaurant_df.withColumn(
    "cost_for_two",
    F.expr("try_cast(cost_for_two AS DOUBLE)")
)

silver_restaurant_df.display()

# ----------------------------------------------------------------------
# **`avg_delivery_time_mins`** mixes numbers with `"na"`.
# ----------------------------------------------------------------------

silver_restaurant_df = silver_restaurant_df.withColumn(
    "avg_delivery_time_mins",
    when((col("avg_delivery_time_mins")) == "na",
        None
    ).otherwise(col("avg_delivery_time_mins")))

from pyspark.sql import functions as F

silver_restaurant_df = silver_restaurant_df.withColumn(
    "avg_delivery_time_mins",
    F.expr("try_cast(avg_delivery_time_mins AS DOUBLE)")
)

silver_restaurant_df.display()

# ----------------------------------------------------------------------
# **`is_active`** is wildly inconsistent: `Yes`/`yes`/`Y`, `No`/`N`, and even `1`/`0`
# ----------------------------------------------------------------------

silver_restaurant_df.select('is_active').distinct().display()

silver_restaurant_df = silver_restaurant_df.withColumn(
    "is_active",
    when((col("is_active")) == "Y","True").
    when((col("is_active")) == "yes","True").
    when((col("is_active")) == "1","True").
    when((col("is_active")) == "N","False").
    when((col("is_active")) == "0","False").
    when((col("is_active")) == "No","False").
    otherwise(col("is_active")))

silver_restaurant_df.display()

silver_restaurant_df.select('is_active').distinct().display()

# ----------------------------------------------------------------------
# **Leading/trailing whitespace** in some `restaurant_name`
# ----------------------------------------------------------------------

from pyspark.sql import functions as F

silver_restaurant_df = silver_restaurant_df.withColumn(
    "restaurant_name",
    F.trim(F.col("restaurant_name"))
)



silver_restaurant_df.display()

# ----------------------------------------------------------------------
#  **Occasional missing `rating`**.
# ----------------------------------------------------------------------

from pyspark.sql import functions as F

restaurant_dim = silver_restaurant_df.select(
    "restaurant_id",
    F.col("cuisine_type")
)

silver_order_df = silver_order_df.drop("cuisine_type")

silver_order_df = silver_order_df.join(
    restaurant_dim,
    "restaurant_id",
    "left"
)
silver_order_df.display()

silver_order_df = silver_order_df.drop("ingest_time")
silver_order_df = silver_order_df.drop("restaurant_name")

# ----------------------------------------------------------------------
# #Saving the file to silver schema
# ----------------------------------------------------------------------

df_silver_customer.write.format("delta").mode("overwrite").saveAsTable("fooddeliveryanalytics.silver.silver_customer")

silver_restaurant_df.write.format("delta").mode("overwrite").saveAsTable("fooddeliveryanalytics.silver.silver_restaurant")

silver_order_df.write.format("delta").mode("overwrite").saveAsTable("fooddeliveryanalytics.silver.silver_order")

# ----------------------------------------------------------------------
# #Gold Layer - Building fact and Dimension Table
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# STEP 1: Load Silver Tables
# ----------------------------------------------------------------------

customers_df = spark.read.table("fooddeliveryanalytics.silver.silver_customer")
orders_df = spark.read.table("fooddeliveryanalytics.silver.silver_order")
restaurant_df = spark.read.table("fooddeliveryanalytics.silver.silver_restaurant")

customers_df.display()
orders_df.display()
restaurant_df.display()

# ----------------------------------------------------------------------
# Step 2: Create Customer Dimension
# ----------------------------------------------------------------------

dim_customer = customers_df.select(
    "customer_id",
    "customer_name",
    "email",
    "phone",
    "gender",
    "date_of_birth",
    "city",
    "state",
    "membership_status"
)

dim_customer.display()

# ----------------------------------------------------------------------
# Create Orders Dimension
# ----------------------------------------------------------------------

dim_order=orders_df.select(
    "order_id",
    "order_date",
    "customer_id",
    "restaurant_id",
    "cuisine_type",
    "payment_method",
    "is_active",
    "order_status"
)

dim_order.display()

# ----------------------------------------------------------------------
# Create Restaurant Dimension
# ----------------------------------------------------------------------

dim_restaurant=restaurant_df.select(
    "restaurant_id",
    "restaurant_name",
    "cuisine_type",
    "city",
    "rating",
    "is_active",
    "avg_delivery_time_mins",
    "cost_for_two"
)

dim_restaurant.display()

spark.sql("DROP TABLE IF EXISTS fooddeliveryanalytics.gold.gold_dim_customer")
spark.sql("DROP TABLE IF EXISTS fooddeliveryanalytics.gold.gold_dim_order")
spark.sql("DROP TABLE IF EXISTS fooddeliveryanalytics.gold.gold_dim_restaurant")

# Saving to Gold Layer

dim_customer.write.format("delta")\
    .mode("overwrite") \
    .saveAsTable("fooddeliveryanalytics.gold.gold_dim_customer")

dim_order.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("fooddeliveryanalytics.gold.gold_dim_order")
dim_restaurant.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("fooddeliveryanalytics.gold.gold_dim_restaurant")

# ----------------------------------------------------------------------
# STEP3: Create Fact Table
# ----------------------------------------------------------------------

from pyspark.sql import functions as F

fact_orders = (
    orders_df.alias("o")
    .join(
        customers_df.alias("c"),
        F.col("o.customer_id") == F.col("c.customer_id"),
        "left"
    )
    .join(
        restaurant_df.alias("r"),
        F.col("o.restaurant_id") == F.col("r.restaurant_id"),
        "left"
    )
    .select(

        # Order Details
        F.col("o.order_id"),
        F.col("o.order_date"),
        F.col("o.customer_id"),
        F.col("o.restaurant_id"),
        F.col("o.order_status"),
        F.col("o.payment_method"),
        F.col("o.order_value"),
        F.col("o.delivery_fee"),
        F.col("o.discount"),
        F.col("o.total_amount"),
        F.col("o.delivery_time_mins"),

        # Customer Details
        F.col("c.customer_name"),
        F.col("c.city").alias("customer_city"),
        F.col("c.state").alias("customer_state"),
        F.col("c.membership_status"),
        

        # Restaurant Details
        F.col("r.restaurant_name"),
        F.col("r.cuisine_type"),
        F.col("r.city").alias("restaurant_city"),
        F.col("r.rating"),
        F.col("r.avg_delivery_time_mins"),
        F.col("r.cost_for_two"),
        F.col("r.is_active")
    )
)

fact_orders.display()

from pyspark.sql.functions import year, month, dayofmonth

order_enriched = fact_orders \
    .withColumn("Year", year("order_date")) \
    .withColumn("Month", month("order_date")) \
    .withColumn("Day", dayofmonth("order_date"))

order_enriched.display()

# ----------------------------------------------------------------------
# Applying Aggregate Functions
# ----------------------------------------------------------------------

from pyspark.sql.functions import sum, countDistinct, avg, min, max

gold_df = order_enriched.groupBy(
    "restaurant_id",
    "restaurant_name",
    "cuisine_type",
    "customer_id",
    "customer_name",
    "membership_status",
    "customer_city",
    "customer_state",
    "Year",
    "Month",
    "order_date",
    "order_status",
    "payment_method"
).agg(

    sum("total_amount").alias("Total_Revenue"),

    sum("order_value").alias("Total_Order_Value"),

    sum("delivery_fee").alias("Total_Delivery_Fee"),

    sum("discount").alias("Total_Discount"),

    countDistinct("order_id").alias("Total_Orders"),

    avg("total_amount").alias("Avg_Order_Value"),

    avg("delivery_time_mins").alias("Avg_Delivery_Time"),

    avg("rating").alias("Avg_Rating"),

    min("delivery_time_mins").alias("Min_Delivery_Time"),

    max("delivery_time_mins").alias("Max_Delivery_Time")
)

gold_df.display()

spark.sql("DROP TABLE IF EXISTS fooddeliveryanalytics.gold.gold_fact_orders")

gold_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("fooddeliveryanalytics.gold.gold_fact_orders")
