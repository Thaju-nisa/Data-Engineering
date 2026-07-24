#!/usr/bin/env python
# coding: utf-8

# ## Ecom_NB
# 
# null

# In[1]:


# Welcome to your new notebook
# Type here in the cell editor to add code!
path = "Files/bronze/"

customers_raw = spark.read.parquet(path + "customers.parquet")
orders_raw = spark.read.parquet(path + "orders.parquet")
payments_raw = spark.read.parquet(path + "payments.parquet")
support_raw = spark.read.parquet(path + "support_tickets.parquet")
web_raw = spark.read.parquet(path + "web_activities.parquet")


# In[2]:


# Save as Bronze Delta Tables

customers_raw.write.format("delta").mode("overwrite").saveAsTable("My_Schema.bronze_customers")
orders_raw.write.format("delta").mode("overwrite").saveAsTable("My_Schema.bronze_orders")
payments_raw.write.format("delta").mode("overwrite").saveAsTable("My_Schema.bronze_payments")
support_raw.write.format("delta").mode("overwrite").saveAsTable("My_Schema.bronze_support")
web_raw.write.format("delta").mode("overwrite").saveAsTable("My_Schema.bronze_web")




# In[12]:


# Silver Layer - Clean & Normalize

from pyspark.sql.functions import *
from pyspark.sql.types import DoubleType

# Clean customers
customers = spark.table("My_Schema.bronze_customers")

customers_clean = (
    customers
        .withColumn("email", lower(trim(col("EMAIL"))))
        .withColumn("name", initcap(trim(col("name"))))
        .withColumn(
            "gender",
            when(lower(col("gender")).isin("f", "female"), "Female")
            .when(lower(col("gender")).isin("m", "male"), "Male")
            .otherwise("Other")
        )
        .withColumn("dob", to_date(regexp_replace(col("dob"), "/", "-")))
        .withColumn("location", initcap(col("location")))
        .dropDuplicates(["customer_id"])
        .dropna(subset=["customer_id", "email"])
)

customers_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("My_Schema.silver_customers")

# Clean orders
orders=spark.table("My_Schema.bronze_orders")

orders_clean = (
    orders
        .withColumn(
            "order_date",
            when(
                col("order_date").rlike("^\\d{4}/\\d{2}/\\d{2}$"),
                to_date(col("order_date"), "yyyy/MM/dd")
            )
            .when(
                col("order_date").rlike("^\\d{2}-\\d{2}-\\d{4}$"),
                to_date(col("order_date"), "dd-MM-yyyy")
            )
            .when(
                col("order_date").rlike("^\\d{8}$"),
                to_date(col("order_date"), "yyyyMMdd")
            )
            .otherwise(
                to_date(col("order_date"), "yyyy-MM-dd")
            )
        )
        .withColumn("amount", col("amount").cast(DoubleType()))
        .withColumn("amount", when(col("amount") < 0, None).otherwise(col("amount")))
        .withColumn("status", initcap(col("status")))
        .dropna(subset=["customer_id", "order_date"])
        .dropDuplicates(["order_id"])
)

orders_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("My_Schema.silver_orders")


#Clean Peyments

# Clean payments
payments = spark.table("My_Schema.bronze_payments")

payments_clean = (
    payments
        .withColumn("payment_date", to_date(regexp_replace(col("payment_date"), "/", "-")))
        .withColumn("payment_method", initcap(col("payment_method")))
        .replace({"creditcard": "Credit Card"}, subset=["payment_method"])
        .withColumn("payment_status", initcap(col("payment_status")))
        .withColumn("amount", col("amount").cast(DoubleType()))
        .withColumn("amount", when(col("amount") < 0, None).otherwise(col("amount")))
        .dropna(subset=["customer_id", "payment_date", "amount"])
)

payments_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("My_Schema.silver_payments")


# Clean support
support = spark.table("My_Schema.bronze_support")

support_clean = (
    support
        .withColumn("ticket_date", to_date(regexp_replace(col("ticket_date"), "/", "-")))
        .withColumn("issue_type", initcap(trim(col("issue_type"))))
        .withColumn("resolution_status", initcap(trim(col("resolution_status"))))
        .replace({"NA": None, "": None}, subset=["issue_type", "resolution_status"])
        .dropDuplicates(["ticket_id"])
        .dropna(subset=["customer_id", "ticket_date"])
)

support_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("My_Schema.silver_support")


# Clean web
web = spark.table("My_Schema.bronze_web")

web_clean = (
    web
        .withColumn("session_time", to_date(regexp_replace(col("session_time"), "/", "-")))
        .withColumn("page_viewed", lower(col("page_viewed")))
        .withColumn("device_type", initcap(col("device_type")))
        .dropDuplicates(["session_id"])
        .dropna(subset=["customer_id", "session_time", "page_viewed"])
)

web_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("My_Schema.silver_web")




# -------- GOLD --------

cust = spark.table("My_Schema.silver_customers").alias("c")
orders = spark.table("My_Schema.silver_orders").alias("o")
payments = spark.table("My_Schema.silver_payments").alias("p")
support = spark.table("My_Schema.silver_support").alias("s")
web = spark.table("My_Schema.silver_web").alias("w")

customer360 = (
    cust
        .join(orders, "customer_id", "left")
        .join(payments, "customer_id", "left")
        .join(support, "customer_id", "left")
        .join(web, "customer_id", "left")
        .select(
            "customer_id",
            "c.name",
            "c.email",
            "c.gender",
            "c.dob",
            "c.location",
            "o.order_id",
            "o.order_date",
            "o.amount",
            "o.status",
            "p.payment_method",
            "p.payment_status",
            "s.ticket_id",
            "s.issue_type",
            "s.ticket_date",
            "s.resolution_status",
            "w.page_viewed",
            "w.device_type",
            "w.session_time"
        )
)

customer360.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("My_Schema.gold_customer360")

