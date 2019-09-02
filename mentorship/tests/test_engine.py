from pandas import DataFrame

from mentorship.engine import run_pipeline


def multiply_by_two(dataframe: DataFrame) -> DataFrame:
    return dataframe * 2


def multiply_by_three(dataframe: DataFrame) -> DataFrame:
    return dataframe * 3


def test_pipeline():
    data = {"column1": [1, 2, 3]}
    df = DataFrame(data=data)
    result = run_pipeline(df, steps=[multiply_by_two, multiply_by_three])
    assert all(result == df * 6)
