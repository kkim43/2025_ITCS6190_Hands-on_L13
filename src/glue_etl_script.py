import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_date, upper, coalesce, lit
from awsglue.dynamicframe import DynamicFrame

## Initialize contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# --- Define S3 Paths (Updated with your new names) ---
s3_input_path = "s3://handsonfinallanding-itcs6190-l13-handson-kkim43/"
s3_processed_path = "s3://handsonfinalprocessed-itcs6190-l13-handson-kkim43/processed-data/"
s3_analytics_path = "s3://handsonfinalprocessed-itcs6190-l13-handson-kkim43/Athena Results/"

# --- Read the data from the S3 landing zone ---
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [s3_input_path], "recurse": True},
    format="csv",
    format_options={"withHeader": True, "inferSchema": True},
)

# Convert to a standard Spark DataFrame for easier transformation
df = dynamic_frame.toDF()

# --- Perform Transformations ---
df_transformed = df.withColumn("rating", coalesce(col("rating").cast("integer"), lit(0)))
df_transformed = df_transformed.withColumn("review_date", to_date(col("review_date"), "yyyy-MM-dd"))
df_transformed = df_transformed.withColumn("review_text", coalesce(col("review_text"), lit("No review text")))
df_transformed = df_transformed.withColumn("product_id_upper", upper(col("product_id")))

# --- Write the full transformed data to S3 (Good practice) ---
glue_processed_frame = DynamicFrame.fromDF(df_transformed, glueContext, "transformed_df")
glueContext.write_dynamic_frame.from_options(
    frame=glue_processed_frame,
    connection_type="s3",
    connection_options={"path": s3_processed_path},
    format="csv"
)

# --- Run Spark SQL Query within the Job ---
df_transformed.createOrReplaceTempView("product_reviews")

df_analytics_result = spark.sql("""
    SELECT 
        product_id_upper, 
        AVG(rating) as average_rating,
        COUNT(*) as review_count
    FROM product_reviews
    GROUP BY product_id_upper
    ORDER BY average_rating DESC
""")

analytics_result_frame = DynamicFrame.fromDF(df_analytics_result.repartition(1), glueContext, "analytics_df")
glueContext.write_dynamic_frame.from_options(
    frame=analytics_result_frame,
    connection_type="s3",
    connection_options={"path": s3_analytics_path + "product_rating_avg/"},
    format="csv"
)

# --- Additional Spark SQL Queries ---

# 2. Date wise review count
df_daily = spark.sql("""
    SELECT 
        review_date,
        COUNT(*) AS review_count
    FROM product_reviews
    GROUP BY review_date
    ORDER BY review_date
""")

daily_frame = DynamicFrame.fromDF(df_daily.repartition(1), glueContext, "daily_df")
glueContext.write_dynamic_frame.from_options(
    frame=daily_frame,
    connection_type="s3",
    connection_options={"path": s3_analytics_path + "daily_review_counts/"},
    format="csv"
)

# 3. Top 5 Most Active Customers
df_top = spark.sql("""
    SELECT 
        customer_id,
        COUNT(*) AS total_reviews
    FROM product_reviews
    GROUP BY customer_id
    ORDER BY total_reviews DESC
    LIMIT 5
""")

top_frame = DynamicFrame.fromDF(df_top.repartition(1), glueContext, "top_df")
glueContext.write_dynamic_frame.from_options(
    frame=top_frame,
    connection_type="s3",
    connection_options={"path": s3_analytics_path + "top_5_customers/"},
    format="csv"
)

# 4. Overall Rating Distribution
df_rating = spark.sql("""
    SELECT 
        rating,
        COUNT(*) AS rating_count
    FROM product_reviews
    GROUP BY rating
    ORDER BY rating
""")

rating_frame = DynamicFrame.fromDF(df_rating.repartition(1), glueContext, "rating_df")
glueContext.write_dynamic_frame.from_options(
    frame=rating_frame,
    connection_type="s3",
    connection_options={"path": s3_analytics_path + "rating_distribution/"},
    format="csv"
)

job.commit()
