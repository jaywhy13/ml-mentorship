from typing import Callable, List

from pandas import DataFrame

Step = Callable[[DataFrame], DataFrame]


def run_pipeline(input_data: DataFrame, steps: List[Step]) -> DataFrame:
    output = input_data
    for step in steps:
        output = step(output)
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
