# ⚙️ Project : Modern Data ELT pipele for e-commerce dataset, olist, with dbt, BigQuery and Airflow (Cloud Composer)

🚀 End-to-End Production-Grade Orchestration on Google Cloud

This project demonstrates a fully automated **ELT pipeline** built using **dbt, Airflow (Cloud Composer), Google Cloud Storage, and BigQuery**. It highlights modern data engineering practices including orchestration, CI/CD automation, dependency management, dbt modeling, and scalable warehouse design.

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

# 🧮 Key Features

### Orchestration & Automation

✴️ Cloud Composer (Managed Airflow) used to orchestrate dbt workflows end-to-end.

✴️ Automated dbt model execution via Airflow DAGs (staging → dims → marts).

✴️ Dependency resolution via ```manifest.json```, ensuring correct execution order.

✴️ Retries, timeouts, logging, and error handling for production readiness.

### Deployment & Infrastructure

✴️ GCS bucket code syncing used for deploying dbt models and DAG files to Composer.

✴️ IAM-secure service account impersonation for least-privilege access to BigQuery and GCS.

### dbt Data Modeling

✴️ BigQuery as the warehouse with:**Source models, Staging models (materialized as views), Dim / mart models (materialized as tables)**

✴️ dbt tests, documentation, lineage, and model configurations.

✴️ Support for incremental, full-refresh, and dependency-driven execution.

### BigQuery Engineering

✴️ Partitioned and clustered table design for efficient cost-optimised querying.

✴️ SQL transformations optimised for scalable analytical workloads.

✴️ Performance-aware modeling following ELT best practices.





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



# What I build

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

# 🛠️ Problems and Solutions : Airflow + dbt + BigQuery Integration

This section documents the major issues encountered while orchestrating dbt models through Cloud Composer (Airflow) with BigQuery and GCS, and how each was diagnosed and resolved.

### Composer couldn’t impersonate service account


#### Error
```yml
iam.serviceAccounts.getAccessToken denied
```
#### Solution
Grant Airflow Worker SA, run this command on the terminal.


```bash

gcloud iam service-accounts add-iam-policy-binding \
  dbt-olist-project@< project ID here >.iam.gserviceaccount.com \
  --member="<your emial address >@gmail.com" \
  --role="roles/iam.serviceAccountTokenCreator"


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

### 6. Airflow Timeout & Zombie Task Issue

#### Cause
dbt models took longer than the default time limi, Airflow workers stopped while dbt was running long BigQuery jobs. The Airflow scheduler assumed the task died → marked it as zombie.Even though dbt finished and created some views/tables(not compelted) in BigQuery, Airflow still failed the task.

#### How I diagnosed
- Airflow UI showed tasks red (failed) even though BigQuery tables were partly successfully created.
- dbt logs inside the task output showed:```"Completed successfully"```, ```PASS=1 ERROR=0```
- **Cloud Logging** / Scheduler logs showed **zombie** detection
- No actual dbt errors. was **not dbt-related**, but **Airflow execution + timeout** related.

#### Solution

Airflow configuration overrides in Cloud Composer

```yml
[celery]
task_soft_time_limit = 3000
task_time_limit = 36000
worker_prefetch_multiplier = 1

[scheduler]
scheduler_zombie_task_threshold = 600
scheduler_heartbeat_sec = 10
```


dbt models took longer to execute than Airflow’s default task timeout and heartbeat thresholds. **Cloud Composer** uses **CeleryExecutor**, and **Celery enforces strict timeouts**

- ```task_time_limit``` → Maximum wall-clock time allowed for a task

- ```task_soft_time_limit``` → When Celery sends a soft kill signal

- ```scheduler_zombie_task_threshold``` → How long Airflow waits before marking a task as “zombie” if it stops sending heartbeats


```python
from datetime import timedelta

dbt_run = BashOperator(
    execution_timeout=timedelta(minutes=40)
    )
```


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

- shos

---
#
