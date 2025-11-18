# 2025 ITCS6190 Hands-on L13 (Serverless Spark ETL Pipeline on AWS)

**Name(ID):** Kiyoung Kim (801426261)  
**E-Mail:** kkim43@charlotte.edu

This project is a hands-on assignment demonstrating a fully automated, event-driven, serverless data pipeline using AWS.

The pipeline ingests a raw CSV file, processes it using a Spark ETL job, runs multiple SQL queries, and stores the final results back into S3 — with no manual steps required.

---

## Project Repository Structure

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

## Architecture

```
S3 (Upload) → Lambda Trigger → Glue ETL Spark Job → S3 (Processed Results)
```

---

## Technology Stack

- Amazon S3  
- AWS Lambda  
- AWS Glue (Spark)  
- PySpark / Spark SQL  
- AWS IAM  

---

## Overview

1. Upload `reviews.csv` to S3 landing bucket  
2. Lambda triggers automatically  
3. Glue ETL job starts  
4. Spark reads & cleans data  
5. Runs 4 SQL queries  
6. Writes results to S3 processed bucket  

---

## Execution Steps

(Your full pipeline steps go here — same as earlier README text.)

---

## Output

Located under `/output/`:

- `/processed-data/` → Clean dataset  
- `/Athena Results/` → 4 analytics folders  

---

## Cleanup

Delete:
- S3 buckets  
- Glue job  
- Lambda function  
- IAM role  
