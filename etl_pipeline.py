from utils import extract, transform, validate, load, lineage
from datetime import datetime

def main():
    # Step 1: Extract structured data
    data, source_info = extract.get_data_from_source()
    
    # Step 2: Schema Inference
    schema = transform.infer_schema(data)
    
    # Step 3: Transform
    transformed_data = transform.transform_data(data)

    # Step 4: Data Quality
    #validate.validate_with_expectations(transformed_data)

    # Step 5: Load to MySQL
    load.load_to_mysql(transformed_data)

    # Step 6: Lineage Tracking
    lineage.track_lineage(
        source_info=source_info,
        schema=schema,
        destination="mysql.database.table",
        transformation_steps=transform.transformation_steps,
        user="ETL_JOB_USER",
        job_name="structured_etl_job"  # Changed job name
    )

if __name__ == "__main__":
    main()
