import os
import json
import pendulum # better datetime library Airflow uses, supports timezones.
from airflow import DAG
from airflow.operators.bash import BashOperator

### WHAT THIS DOES
# 1. Looks for the manifest.json file
# 2. Parses only models from manifest.json
# 3. Runs the dbt run command with prod profile

HOME = os.environ["HOME"] # Get my home directory from the OS, NOT my dbt project folder.
# /home/airflow/gcs/data: exists inside Cloud Composer, on Google Cloudâ€™s workers(== GCS bucket structure).
# '/home/airflow/gcs/' : default
# /data :GCS's bucket
manifest_path = os.path.join("/home/airflow/gcs/data", "target/manifest.json") # path to manifest.json

with open(manifest_path) as f:
    # load manifest.json into py dict
    manifest = json.load(f)
    # Keys = node IDs like "model.project_name.model_name"
    # Values = metadata dicts with fields like:'resource_type, package_name,name,depends_on'
    # extract only nodes. (dbt nodes are models, seeds, tests, snapshots, etc.)
    nodes = manifest["nodes"]

# Build an Airflow DAG
with DAG(
    # The name that shows up in the UI
    dag_id="olist_dbt_project",
    # Start date of the DAG
    start_date=pendulum.today(),
    # "30 18 * * *", 18:30
    schedule_interval='*/10 * * * *', # every 10 mins
    # â€“ Airflow will NOT backfill all missed runs between start_date and now; it will only run from â€œnowâ€ forward.
    catchup=False,
) as dag:

    # store Airflow tasks indexed by node_id.
    dbt_tasks = dict()

    # # Create a task only for dbt models
    for node_id, node_info in nodes.items():

        if node_info["resource_type"] != "model":
            continue

        task_id = ".".join(
            [
                node_info["resource_type"],
                node_info["package_name"],
                node_info["name"],
            ]
        )

        dbt_tasks[node_id] = BashOperator(
            task_id=task_id,
            bash_command=(
                # GCS folder where models(sql) are
                "cd /home/airflow/gcs/dags/ && "
                "dbt run "
                f"--models {node_info['name']} "
                "--target dev" #"--target prod"
            ),
        )


        # Wire up dependencies based on dbt graph
        for node_id, node_info in nodes.items():
            if node_info["resource_type"] != "model":
                continue

            upstream_nodes = node_info["depends_on"]["nodes"]
            if upstream_nodes:
                for upstream_node in upstream_nodes:
                    if upstream_node in dbt_tasks:
                        dbt_tasks[upstream_node] >> dbt_tasks[node_id]

if __name__ == "__main__":
    dag.cli()
