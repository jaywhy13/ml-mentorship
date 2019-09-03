import sys
from typing import Dict, Callable
from mentorship.gmail.api import GmailApi
from mentorship.email_classification.pipeline import get_pipeline_steps
from mentorship.engine import osemn_pipeline

from pandas import DataFrame

api = GmailApi()
api.initialize()


def download_emails():

    emails = api.get_messages()
    from pprint import pprint

    pprint(emails)


def download_labels():
    labels = api.get_labels()
    from pprint import pprint

    pprint(labels)


def run_pipeline():
    obtain_step, scrub_step, explore_step, model_step, interpret_step = (
        get_pipeline_steps()
    )
    osemn_pipeline(
        input_data=DataFrame(),
        obtain_step=obtain_step,
        scrub_step=scrub_step,
        explore_step=explore_step,
        model_step=model_step,
        interpret_step=interpret_step,
    )


TASK_REGISTRY: Dict[str, Callable] = {
    "download_emails": download_emails,
    "download_labels": download_labels,
    "run_pipeline": run_pipeline,
}

if __name__ == "__main__":

    task_name = sys.argv[1]
    task_function = TASK_REGISTRY.get(task_name)
    if task_function:
        task_function()
    else:
        raise Exception(f"Unknown task {task_name}")
