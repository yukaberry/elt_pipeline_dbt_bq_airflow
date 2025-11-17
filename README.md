# ⚙️ Project : Modern Data ELT pipele for e-commerce dataset, olist, with dbt, BigQuery and Airflow (Cloud Composer)

End-to-End Production-Grade Orchestration on Google Cloud

This project implements a complete modern data engineering pipeline, orchestrated with Airflow running on Google Cloud Composer, transforming data using dbt Core, and storing curated data in BigQuery.

The pipeline is built to match real production standards used by data teams.

# 🧱🏗️ Architecture Overview

```yml
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

```

☁️ GCS and Cloud Composer : Assets are synchronized through GCS buckets used by Cloud Composer

```yml
/home/airflow/gcs/dags/      → Airflow DAG code
/home/airflow/gcs/plugins/   → dbt + Python dependencies
/home/airflow/gcs/data/      → dbt project (models/, sources/, manifest.json)
```

# 🎯 Target

- Build a fully **automated ELT pipeline** using **dbt**

- **Orchestrate** dbt models with **Airflow** on **Cloud Composer**

- Use **BigQuery** as the warehouse for both raw and transformed data

- Implement **service account** impersonation, OAuth, and IAM best practices

- Solve real **production** issues in distributed cloud environments

- Produce an **end-to-end** portfolio-ready **data engineering** system

# 🧮 Features


✴️ Cloud Composer (managed Airflow)

✴️ GCS bucket syncing for code deployment

✴️ Fully automated dbt execution in DAG

✴️ BigQuery sources, staging, and marts

✴️ Incremental model dependency resolution using manifest.json

✴️ IAM-secure service account impersonation

✴️ End-to-end logs, retries, and failure handling

----

# 🔧 Cloud Components Used

| Component          | Purpose                                |
| ------------------ | -------------------------------------- |
| **Cloud Composer** | Orchestration (managed Airflow)        |
| **BigQuery**       | Data warehouse                         |
| **dbt Core**       | SQL transformations, lineage, tests    |
| **GCS Buckets**    | Store DAGs, dbt project, logs          |
| **IAM**            | Secure authentication between services |

# 📁 Folder Structure in GCS


```yml
gs://<composer-bucket>/dags/
    ├── dbt_dag.py
    ├── models/
        ├── marts/
            ├──dim_product_translated_name.sql
        ├── staging/
            ├──stg_olist_product_src.sql
            ├──stg_translated_product_name_src.sql

    ├── macros/
        ├── norm_key.sql
    ├── dbt_project.yml
    └── _src.yml


gs://<raw-data-bucket>/data/
    ├── profiles/
        ├── profiles.yml
    ├── target/
        ├──manifest.json

```
# TODO change this title
# What I Successfully Built (What Engineers Care About)

#### 1. Cloud Composer Environment Setup
I fully configured Composer, including:

- Environment creation in europe-west1
- Determining high-resilience vs standard resilience
- Installing Python/dbt dependencies through PyPI
- Configuring Composer Workers to run dbt


#### 2. GCS Bucket Architecture

| Folder     | Purpose                        |
| ---------- | ------------------------------ |
| `dags/`    | DAG files + dbt project        |
| `data/`    | manifests, seeds, static files |
| `plugins/` | Python libs & dbt installation |


#### 3. Deploying dbt inside Cloud Composer

- Packaging dbt into Cloud Composer

- Adding dbt-bigquery

- Ensuring all dependencies match Python version in Composer

- Moving dbt project into dags/ so Airflow can execute dbt commands


#### 4. Orchestrating dbt via Airflow

The DAG dynamically creates a task per dbt model, using ```manifest.json```. This ensures proper dependencies between staging → dim → fact models.


```yml
dbt_tasks[node_id] = BashOperator(
    task_id=task_id,
    bash_command=(
        "cd /home/airflow/gcs/dags/ && "
        "dbt run "
        f"--models {node_info['name']} "
        "--target dev "
        # "--full-refresh " Drop and recreate ALL “table” and “incremental” models
    ),
)
```

#### 5. BigQuery Configuration

- Raw dataset: ```olist_raw```

- Transformed dataset: ```olist_dbt```

- OAuth authentication for local dbt

- Service account impersonation for Airflow execution



---
#

✅ Design and implement ELT data pipelines
✅ A dbt project with tests, docs, and lineage
✅ Designing partitioned and clustered tables (BigQuery)
✅ Query optimization
✅ Setting up CI/CD to run dbt automatically on push
✅ Scheduling dbt jobs with Airflow

---

# 🛠️ Problems and Solutions : Airflow + dbt + BigQuery Integration

This section documents the major issues encountered while orchestrating dbt models through Cloud Composer (Airflow) with BigQuery and GCS, and how each was diagnosed and resolved.

### Composer couldn’t impersonate service account


#### Error
```yml
iam.serviceAccounts.getAccessToken denied
```
#### Solution
Grant Airflow Worker SA

# TODO
```bash
gcloud

```


### 1️⃣ Airflow Could Not Find manifest.json

#### Error
```yml
FileNotFoundError: [Errno 2] No such file or directory: '/home/airflow/gcs/dags/target/manifest.json'
```
#### Cause
The dbt project was not copied correctly into the GCS bucket used by Cloud Composer.
Missing files and folders under 'dag' folder :

- models/model_file_name.sql etc ...
- dbt_project.yml
- sources files (_src.yml)
- target/manifest.json

#### Solution

```bash
gs://<composer-bucket>/dags/
```

```yml
dags/
 ├── dbt_dag.py
 ├── dbt_project.yml
 ├── models/
      ├──staging/
      ├──marts/
 ├── macros/
 ├── seeds/
 ├── target/manifest.json
```

### 2️⃣ dbt Could Not Find Sources in BigQuery
dbt sources failing inside Composer
#### Error

```bash
Model ... depends on a source named 'olist_raw.orders' which was not found
```

#### Cause
sources YAML file (_src.yml) was not uploaded to GCS → Composer environment.

#### Solution

```yml
dags/
├── models/
  ├──staging/
  ├──marts/
  ├──_src.yml
```

### 3️⃣ Profiles Directory Not Found

#### Error

```yml
Invalid value for '--profiles-dir': Path 'home/airflow/gcs/data/profiles' does not exist.
```
#### Cause
profiles.yml was missing

#### Solution

```yml
dags/
  ├── models/
data/
  ├── profiles/
    ├──profiles.yml
```
```bash
gs://<composer-bucket>/data/profiles/profiles.yml
```


### 4️⃣ Duplicate Model Names

#### Error
There were 2 exactly the same sql file but in the differnt file location. dbt pick up all sql files from 'models/'

```bash
dbt found two models with the name "stg_olist_product_src".(from manual work trigger project, instead of using Airflow)
...
- models/staging/stg_olist_product_src.sql
- models/stg_olist_product_src.sql
```

#### Solution

Removed the duplicate file

```bash
gsutil rm gs://<composer-bucket>/dags/models/stg_olist_product_src.sql
```

Before
```yml
dags/
├── models/
  ├──staging/stg_olist_product_src.sql
  ├──stg_olist_product_src.sql
```
⬇️

After
```yml
dags/
├── models/
  ├──staging/stg_olist_product_src.sql
```

### 5️⃣ View vs Table Conflict in BigQuery

#### Error
```yml
Trying to create view `olist_dbt.dim_product_translated_name`,
but it currently exists as a TABLE.
```

#### Cause
This model had previously been materialized as a **table** when dbt was run locally.
Inside Composer, dbt tried to create it as a **view** (based on **dbt_project.yml** config), leading to a conflict.

#### Solution

Manually delete table(olist_dbt.dim_product_translated_name) from BigQuery


### 📊 Outcome: Fully Working Production-Style Pipeline
✔ Airflow schedules dbt runs

✔ dbt models are executed in dependency order

✔ Raw → Staging → Dim → Fact models are materialized in BigQuery

✔ Airflow retries, logs, and error handling fully operational

✔ IAM-secure environment using impersonation

✔ GCS syncing ensures fully automated deployments


# What I Learnt From Issues

- GCS ↔ Composer file sync
- Managing distributed systems (Airflow + dbt + GCS + BigQuery)
- Deep understanding of IAM, impersonation, and service account auth
- Debugging complex Airflow → dbt subprocess errors
- Cloud Composer file system structure
- Using dbt’s manifest.json to build DAGs
- Organising GCS buckets for automated DAG deployment
- Running dbt Core in production-grade cloud environments

---
