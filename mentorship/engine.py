import os
from typing import Callable, List

from pandas import DataFrame
from termcolor import cprint

Step = Callable[[DataFrame], DataFrame]

DEBUG_PIPELINE = bool(int(os.getenv("DEBUG_PIPELINE", "0")))


def run_pipeline(input_data: DataFrame, steps: List[Step]) -> DataFrame:
    output = input_data
    for index, step in enumerate(steps):
        cprint(f">>>> Running step {index + 1}: {step.__name__}\n", "green")
        output = step(output)
        if DEBUG_PIPELINE:
            import pdb

            pdb.set_trace()
        print("")
    return output


def osemn_pipeline(
    input_data: DataFrame,
    obtain_step: Step,
    scrub_step: Step,
    explore_step: Step,
    model_step: Step,
    interpret_step: Step,
) -> DataFrame:
    return run_pipeline(
        input_data,
        steps=[obtain_step, scrub_step, explore_step, model_step, interpret_step],
    )
