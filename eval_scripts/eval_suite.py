import great_expectations as ge
# import os
# PROJECT_PATH = os.environ.get("PROJECT_PATH")


def validate_rki_report_parse(configs):

    for config in configs["suites"]:
        print(config)
        context = ge.data_context.DataContext()
        batch_kwargs_file = config["batch_kwargs"]

        batch_file = context.get_batch(batch_kwargs_file, config["suit_name"])

        results = context.run_validation_operator(
            "action_list_operator",
            assets_to_validate=[batch_file],
            run_id=config["run_id"]
        )

        if config["severity"] == "critical":
            if not results["success"]:
                raise Exception("Validation of the source data is not successful")


if __name__ == "__main__":
    import json
    import argparse
    from urllib.parse import unquote

    # Set up CLI Arguments
    parser = argparse.ArgumentParser()

    # Required Arguments
    parser.add_argument("-c", "--config", required=True,
                        help="JSON configuration string for this operation")

    # Grab the Arguments
    args = parser.parse_args()

    jsonString = unquote(args.config).replace("'", '"')
    configs_parsed = json.loads(jsonString)

    validate_rki_report_parse(configs_parsed)
