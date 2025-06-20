import uuid
import yaml
from datetime import datetime
import os

def track_lineage(source_info, schema, destination, transformation_steps, user="etl_user", job_name="semi_structured_etl_job"):
    # Generate a unique ID for this ETL run
    run_id = str(uuid.uuid4())

    # Prepare the lineage dictionary
    lineage = {
        "job": {
            "name": job_name,
            "namespace": "etl_namespace"
        },
        "inputs": [
            {
                "name": source_info.get("source", "unknown_source"),
                "namespace": "source",
                "facets": {
                    "schema": {
                        "fields": schema
                    }
                }
            }
        ],
        "outputs": [
            {
                "name": destination,
                "namespace": "mysql"
            }
        ],
        "run": {
            "runId": run_id,
            "facets": {
                "source": source_info,
                "transformations": transformation_steps,
                "user": user,
                "runTime": str(datetime.now())
            }
        }
    }

    # Save lineage YAML to a logs directory
    os.makedirs("logs", exist_ok=True)
    lineage_file = f"logs/lineage_output_{run_id}.yaml"

    with open(lineage_file, "w") as f:
        yaml.dump(lineage, f, sort_keys=False)

    print(f"✅ Lineage tracked successfully and saved to: {lineage_file}")
