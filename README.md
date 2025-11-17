# ⚙️ Project : Modern Data ELT pipele for e-commerce dataset, olist, with dbt, BigQuery and Airflow (Cloud Composer)

End-to-End Production-Grade Orchestration on Google Cloud

This project implements a complete modern data engineering pipeline, orchestrated with Airflow running on Google Cloud Composer, transforming data using dbt Core, and storing curated data in BigQuery.

The pipeline is built to match real production standards used by data teams.

# 🧱🏗️ Architecture Overview

Google Cloud Composer (Airflow)
        │
        │  Schedules + Orchestrates
        ▼
Airflow DAG → BashOperator → dbt Core
        │
        │  SQL Transformations + Tests
        ▼
 BigQuery (raw → staging → marts)
        │
        ▼
 Curated analytical tables

☁️ GCS and Cloud Composer : Assets are synchronized through GCS buckets used by Cloud Composer

/home/airflow/gcs/dags/      → Airflow DAG code
/home/airflow/gcs/plugins/   → dbt + Python dependencies
/home/airflow/gcs/data/      → dbt project (models/, sources/, manifest.json)

# 🎯 Target

- Build a fully **automated ELT pipeline** using **dbt**

- **Orchestrate** dbt models with **Airflow** on **Cloud Composer**

- Use **BigQuery** as the warehouse for both raw and transformed data

- Implement **service account** impersonation, OAuth, and IAM best practices

- Solve real **production** issues in distributed cloud environments

- Produce an **end-to-end** portfolio-ready **data engineering** system



#

✅ Design and implement ELT data pipelines
✅ A dbt project with tests, docs, and lineage
✅ Designing partitioned and clustered tables (BigQuery)
✅ Query optimization
✅ Setting up CI/CD to run dbt automatically on push
✅ Scheduling dbt jobs with Airflow



# Problems and Solutions

#
