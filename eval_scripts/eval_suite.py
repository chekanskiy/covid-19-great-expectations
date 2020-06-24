import great_expectations as ge
import os

# PROJECT_PATH = os.environ.get("PROJECT_PATH")
PROJECT_PATH = "/Users/chekanskiy/Documents/projects/covid-19-exploration"

def validate_rki_report_parse(**kwargs):
    # TODO Refactor to run GE in a container
    # pass configs as parameters and do the actual work in a docker
    # the goal is to distribute work and minimise work performed in Airflow

    context = ge.data_context.DataContext()
    batch_kwargs_file = {"path": os.path.join(PROJECT_PATH, "data-processed/tmp_rki_report.csv"),
                         "datasource": "covid-silver"}

    batch_file = context.get_batch(batch_kwargs_file, "tmp_rki_report.error")

    results = context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[batch_file],
        run_id=f"airflow:{kwargs['dag']}:{kwargs['ds']}"
    )

    if not results["success"]:
        raise Exception("Validation of the source data is not successful")

validate_rki_report_parse()