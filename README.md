# 2025 ITCS6190 Hands-on L13  

**Name (ID):** Kiyoung Kim (801426261)  
**Email:** kkim43@charlotte.edu

This project implements a **fully automated, event‑driven serverless ETL pipeline** using AWS S3, AWS Lambda, and AWS Glue (Spark).  
When a new CSV file arrives in S3, the entire pipeline runs automatically without any human action.

---

# 🌟 Project Goal

The goal of this hands‑on assignment is to simulate a real‑world cloud data engineering workflow:

1. **A new CSV file is uploaded** to an S3 landing bucket.  
2. **Lambda detects the new file** through an S3 ObjectCreated event trigger.  
3. **Lambda starts an AWS Glue ETL Spark job.**  
4. The Glue ETL job:  
   - Reads and cleans raw CSV data  
   - Runs **4 Spark SQL queries**, including 3 new analytics queries  
   - Writes all results to a processed S3 bucket  

This creates a **no‑touch, fully automated analytics pipeline**.

---

# 📁 Project Repository Structure

```
2025_ITCS6190_Hands-on_L13/
│
├── README.md
│
├── src/
│   ├── glue_etl_script.py
│   └── lambda_function.py
│
├── input/
│   └── reviews.csv
│
├── output/
│   ├── processed-data/
│   │   └── run-1763497006162-part-r-00000
│   │
│   └── Athena Results/
│       ├── product_rating_avg/
│       │   └── run-1763496820291-part-r-00000
│       ├── daily_review_counts/
│       │   └── run-1763496825513-part-r-00000
│       ├── top_5_customers/
│       │   └── run-1763496828123-part-r-00000
│       └── rating_distribution/
│           └── run-1763496832500-part-r-00000
│
└── screenshots/
    ├── l13_001.PNG
    ├── l13_002.PNG
    ├── l13_003.PNG
    ├── l13_004.PNG
    ├── l13_005.PNG
    ├── l13_006.PNG
    ├── l13_007.PNG
    ├── l13_008.PNG
    └── l13_009.PNG
```

---

# 🏗️ Architecture Diagram

```
S3 (Upload) → Lambda Trigger → Glue ETL Spark Job → S3 (Processed Results)
```

This pipeline is **serverless**, highly scalable, and requires zero manual intervention.

---

# ⚙️ Technologies Used

- **Amazon S3** – data lake storage  
- **AWS Lambda** – triggers ETL process automatically  
- **AWS Glue (Spark)** – ETL + data analytics  
- **PySpark / Spark SQL** – data cleaning & queries  
- **AWS IAM** – secure access control  

---

# 🚀 Detailed Setup & Deployment (Step-by-Step)

## 1️⃣ Create S3 Buckets
Two globally unique buckets:

- `handsonfinallanding-itcs6190-l13-handson-kkim43`  
- `handsonfinalprocessed-itcs6190-l13-handson-kkim43`

![s3 buckets](screenshots/l13_001.PNG)

---

## 2️⃣ Upload reviews.csv to Landing Bucket

Uploading this file triggers the Lambda function.

![upload csv](screenshots/l13_002.PNG)

---

## 3️⃣ Create IAM Role for Glue

Role name: **AWSGlueServiceRole-Reviews**

Attached policies:
- AWSGlueServiceRole  
- AmazonS3FullAccess (demo simplicity)

---

## 4️⃣ Create AWS Glue ETL Job

- Name: **process_reviews_job**  
- Script: `src/glue_etl_script.py`

![glue script](screenshots/l13_005.PNG)

---

## 5️⃣ Create Lambda Trigger Function

Function: **start_glue_job_trigger**  
Runtime: **Python 3.10**

Add inline IAM policy:

```json
{
  "Effect": "Allow",
  "Action": "glue:StartJobRun",
  "Resource": "*"
}
```

![lambda trigger](screenshots/l13_003.PNG)

---

## 6️⃣ Lambda CloudWatch Logs

Shows Glue job starting successfully.

![lambda logs](screenshots/l13_004.PNG)

---

# 🔥 Glue ETL: Data Processing & SQL Analytics

### ✔ Data Cleaning Performed:
- Convert rating to integer  
- Replace null values  
- Parse date  
- Create uppercase product_id  
- Fill missing review text  

### ✔ Spark SQL Queries (4 total)
1. **Product Rating Average (Required Provided Query)**  
2. **Daily Review Count (New Query)**  
3. **Top 5 Most Active Customers (New Query)**  
4. **Rating Distribution (New Query)**  

Results stored under:

```
output/Athena Results/
```

---

# 📈 Glue Job Monitoring

Job finished with status **SUCCEEDED**.

![glue monitoring](screenshots/l13_006.PNG)

---

# 📂 Output Files Generated

### Processed Clean Dataset
```
output/processed-data/
```

### Athena Results (4 analytics folders)
![processed output](screenshots/l13_007.PNG)

![athena results](screenshots/l13_008.PNG)

---

# 📄 Sample Output File

![sample file](screenshots/l13_009.PNG)

---

# 🧹 Cleanup Instructions

To avoid AWS charges:

- Delete both S3 buckets  
- Delete Glue job  
- Delete Lambda function  
- Delete IAM role  

---
