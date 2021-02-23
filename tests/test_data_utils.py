"""
Data Utilities Tests
--------------------
"""

import pandas as pd

from wikirepo.data import data_utils


def test_interp_by_subset(df):
    df_interp = data_utils.interp_by_subset(
        df=df, depth=1, col_name="sub_abbr", method="pad", limit_direction="both"
    )
    assert df_interp["sub_abbr"].isnull().values.any() == False


def test_sum_df_prop_vals(df):
    df.loc[
        df.loc[(df["sub_lctn"] == "Berlin") & (df["year"] == "2009")].index,
        "population",
    ] = 100

    df.loc[
        df.loc[(df["sub_lctn"] == "Berlin") & (df["year"] == "2010")].index,
        "population",
    ] = 100

    df.loc[
        df.loc[(df["sub_lctn"] == "Hamburg") & (df["year"] == "2009")].index,
        "population",
    ] = 100

    df.loc[
        df.loc[(df["sub_lctn"] == "Hamburg") & (df["year"] == "2010")].index,
        "population",
    ] = 100

    df_test = data_utils.sum_df_prop_vals(
        df=df,
        target_lctn="Berlin",
        vals_lctn="Hamburg",
        lctn_col="sub_lctn",
        time_col="year",
        prop_col="population",
        subtract=False,
        drop_vals_lctn=True,
    )

    assert (
        df_test.loc[df_test.loc[df_test["sub_lctn"] == "Berlin"].index[0], "population"]
        > df.loc[df.loc[df["sub_lctn"] == "Berlin"].index[0], "population"]
    )
    assert "Hamburg" not in list(df_test["sub_lctn"])

    df_test = data_utils.sum_df_prop_vals(
        df=df,
        target_lctn="Berlin",
        vals_lctn="Hamburg",
        lctn_col="sub_lctn",
        time_col=None,
        prop_col="population",
        subtract=True,
        drop_vals_lctn=True,
    )

    assert (
        df_test.loc[df_test.loc[df_test["sub_lctn"] == "Berlin"].index[0], "population"]
        < df.loc[df.loc[df["sub_lctn"] == "Berlin"].index[0], "population"]
    )
    assert "Hamburg" not in list(df_test["sub_lctn"])
