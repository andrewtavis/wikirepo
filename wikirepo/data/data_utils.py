"""
Utility functions for querying data

Contents
--------
  0. No Class
      _get_fxn_idx
      _get_dir_fxns_dict
      _check_data_assertions
      _get_max_workers

      incl_dir_idxs
      gen_base_df
      assign_to_column
      gen_base_and_assign_to_column
      assign_to_cols
      gen_base_and_assign_to_cols

      query_wd_prop
      query_repo_dir

      interp_by_subset
      sum_df_prop_vals
      split_col_val_dates
      count_df_prop_vals
"""

import os
import inspect
import importlib
from ast import literal_eval

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from wikirepo import utils
from wikirepo.data import lctn_utils, time_utils, wd_utils
from wikirepo.data.geographic import continent


def _get_dir_fxns_dict(dir_name=None):
    """
    Generates a jump table dictionary of all modules in the cwd and the get_ functions within

    Note: indexes all data querying functions within wikirepo directories

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

    Returns
    -------
        fxns_dict : dict
            A dictionary with keys being module names and contents being dictionaries of standardized indexes and functions
    """
    data_directory = os.path.dirname(os.path.abspath(__file__))
    target_directory = data_directory + "/" + dir_name
    modules = os.listdir(target_directory)
    target_modules = [m[:-3] for m in modules if (m[: len("__")] != "__")]

    try:
        import_path = (
            "wikirepo." + target_directory.split("wikirepo/")[2].replace("/", ".") + "."
        )
    except:
        import_path = (
            "wikirepo." + target_directory.split("wikirepo/")[1].replace("/", ".") + "."
        )

    fxns_dict = {}
    for mod in target_modules:
        script = importlib.import_module(import_path + mod)
        name_fxn_list = [
            [fxn[0], getattr(script, fxn[0])]
            for fxn in inspect.getmembers(script, inspect.isfunction)
        ]

        indexed_fxn_dict = {}
        for n_f in name_fxn_list:
            if n_f[0][: len("query_")] == "query_":
                indexed_fxn_dict[n_f[0]] = n_f[1]

        fxns_dict[mod] = indexed_fxn_dict

    return fxns_dict


def _check_data_assertions(timespan=None, interval=None, **kwargs):
    """
    Checks standardized data assertions across functions given local functional arguments

    Parameters
    ----------
        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

    Returns
    -------
        The results of a series of standardized assertions
    """
    assert (interval == None) or (interval in time_utils.incl_intervals()), (
        "Please provide None for no time interval or a value for 'interval' from the following list of possible arguments: "
        + ", ".join(time_utils.incl_intervals())
        + "."
    )

    if timespan != None:
        assert (
            interval != None
        ), "A 'timespan' has been provided, but no value for the 'interval' by which it should be segmented."


def _get_max_workers(multicore):
    if multicore == True:
        return None  # the number of processors on the machine

    elif multicore == False:
        return 1

    else:
        return multicore


def incl_dir_idxs(dir_name=None, descriptions=False):
    """
    Returns the included indexes in the given directory - the file names of its scripts

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        descriptions : bool (default=False)
            Whether also return the descriptions of the indexes

    Returns
    -------
        included_indexes : list
            A list of included indexes as derived by module names
    """
    return list(_get_dir_fxns_dict(dir_name).keys())


def gen_base_df(
    locations=None, depth=None, timespan=None, interval=None, col_name="data"
):
    """
    Generates a baseline dataframe to be filled with queried data

    Parameters
    ----------
        locations : str, list, or lctn_utils.LocationsDict (contains strs) : optional (default=None)
            The locations to query

        depth : int (default=None)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        col_name : str (default=data)
            The name of the column into which queried data should be merged

    Returns
    -------
        base_df : pd.DataFrame
            A df that is ready to have queried data added to it
    """
    if type(locations) == str:
        locations = [locations]

    if type(locations) == list:
        assert (
            depth == 0
        ), """The user has provided locations with depth 0, but the 'depth' argument is not 0.
        If a greater depth is required, use lctn_utils.gen_lctns_dict."""

    elif type(locations) == lctn_utils.LocationsDict:
        if depth != None:
            depth_check = lctn_utils.derive_depth(locations, depth=0)
            assert (
                depth_check == depth
            ), "The given depth and the derived depth of the LocationsDict do not match. Please check the geographic depth you want to analyze."

        else:
            depth = lctn_utils.derive_depth(locations, depth=0)

    df_cols = lctn_utils.depth_to_cols(depth=depth)
    # qids that will have values assigned through a LocationsDict lookup
    qid_cols = lctn_utils.depth_to_qid_cols(depth=depth)
    df_cols += qid_cols

    if interval:
        df_cols += [time_utils.interval_to_col_name(interval)]

    base_df = pd.DataFrame(columns=df_cols)
    for col in qid_cols:
        base_df[col] = base_df[col].astype(object)

    if depth == 0:
        base_df[lctn_utils.depth_to_col_name(depth=depth)] = locations

    current_depth = 0
    current_qid_col = lctn_utils.depth_to_qid_col_name(depth=current_depth)

    if type(locations) == lctn_utils.LocationsDict or type(locations) == dict:
        current_depth_qids = [q for q in locations.keys()]

    elif type(locations) == list:
        current_depth_qids = [lctn_utils.lctn_lbl_to_qid(lctn) for lctn in locations]
    base_df[current_qid_col] = current_depth_qids

    # Assign labels for the above QIDs
    if type(locations) == lctn_utils.LocationsDict or type(locations) == dict:
        base_df[lctn_utils.depth_to_col_name(depth=current_depth)] = [
            list(lctn_utils.iter_key_items(node=locations, kv=q))[0]["lbl"]
            for q in current_depth_qids
        ]

    elif type(locations) == list:
        base_df[lctn_utils.depth_to_col_name(depth=current_depth)] = locations

    while current_depth < depth:
        assign_qid_col = lctn_utils.depth_to_qid_col_name(depth=current_depth + 1)
        assign_lbl_col = lctn_utils.depth_to_col_name(depth=current_depth + 1)

        for q in [qid for qid in current_depth_qids if qid != np.nan]:
            # Assign a list that will directly be exploded
            key_items = list(lctn_utils.iter_key_items(node=locations, kv=q))[0]
            key_subs = list(lctn_utils.iter_key_items(node=key_items, kv="sub_lctns"))[
                0
            ]
            key_sub_qids = list(key_subs.keys())
            if key_sub_qids == []:
                # Assign to locations that don't have sub_lctns for pd.explode
                key_sub_qids = np.nan

            base_df.at[
                base_df[base_df[current_qid_col] == q].index[0], assign_qid_col
            ] = key_sub_qids

            base_df = base_df.explode(assign_qid_col)
            base_df.reset_index(drop=True, inplace=True)
            base_df[assign_qid_col] = base_df[assign_qid_col].astype(str)

            if type(key_sub_qids) == list:
                for sub_q in base_df.loc[base_df[current_qid_col] == q, assign_qid_col]:
                    # For each sub_qid, assign the lbl
                    base_df.loc[
                        base_df[base_df[assign_qid_col] == sub_q].index[0],
                        assign_lbl_col,
                    ] = list(lctn_utils.iter_key_items(node=locations, kv=sub_q))[0][
                        "lbl"
                    ]

        current_depth_qids = list(base_df[assign_qid_col])
        current_qid_col = assign_qid_col

        current_depth += 1

    if interval:
        time_col = time_utils.interval_to_col_name(interval=interval)

        if type(locations) == lctn_utils.LocationsDict or type(locations) == dict:
            # Find the valis times for the sub_lctn and assign them
            final_sub_lctn_qid_col = lctn_utils.depth_to_qid_col_name(depth=depth)
            for q in base_df[final_sub_lctn_qid_col]:
                if q != "nan":  # is str because of astype(str)
                    key_items = list(lctn_utils.iter_key_items(node=locations, kv=q))[0]
                    key_vts = list(
                        lctn_utils.iter_key_items(node=key_items, kv="valid_timespan")
                    )[0]

                    base_df.at[
                        base_df[base_df[final_sub_lctn_qid_col] == q].index[0], time_col
                    ] = key_vts

            base_df = base_df.explode(time_col)

        elif type(locations) == list:
            base_df[time_col] = [
                time_utils.make_timespan(interval=interval, timespan=timespan)
            ] * len(base_df)

            base_df = base_df.explode(time_col)
            base_df = time_utils.truncate_date_col(
                df=base_df, col=time_col, interval=interval
            )

    if col_name != None:
        base_df[col_name] = [np.nan] * len(base_df)

    # Drop all columns except for the last to allow for assignment
    for col in qid_cols[:-1]:
        base_df.drop(col, axis=1, inplace=True)

    base_df = base_df.replace("nan", np.nan)
    base_df.reset_index(drop=True, inplace=True)

    return base_df


def assign_to_column(
    df=None,
    locations=None,
    depth=None,
    interval=None,
    col_name="data",
    props=None,
    assign="all",
    span=False,
):
    """
    Assigns Wikidata property values to a designated column of a given df

    Parameters
    ----------
        df : pd.DataFrmae
            A df (likely base_df) to which values should be assigned

        locations : str, list, or lctn_utils.LocationsDict (contains strs) : optional (default=None)
            The locations to query

        depth : int (default=None)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        col_name : str
            A column in df to which properties should be assigned

        props : list or dict
            The properties to be assigned

        assign : str (default=all)
            The type of assignment

        span : bool (default=False)
            Whether to check for P580 'start time' and P582 'end time' to create spans

    Returns
    -------
        df : pd.DataFrame
            The df after assignment
    """
    valid_assigns = ["all", "most_recent", "repeat"]

    if type(locations) == str:
        locations = [locations]

    if type(locations) == list:
        assert (
            depth == 0
        ), """The user has provided locations with depth 0, but the 'depth' argument is not 0.
        If a greater depth is required, use lctn_utils.gen_lctns_dict."""

    elif type(locations) == lctn_utils.LocationsDict:
        if depth != None:
            depth_check = lctn_utils.derive_depth(locations, depth=0)
            assert (
                depth_check == depth
            ), "The given depth and the derived depth of the LocationsDict do not match. Please check the geographic depth you want to analyze."

    # Column made up of QIDs for assignment
    assignment_col = lctn_utils.depth_to_qid_col_name(depth=depth)

    if assign == "all":
        # Assign a value over rows by matching times
        for q in df[assignment_col].unique():
            if type(q) == str:  # is a valid location
                for t in props[q].keys():
                    if type(props[q][t]) == list:
                        # Multiple values to assign
                        df.loc[
                            df[
                                (df[assignment_col] == q)
                                & (df[time_utils.interval_to_col_name(interval)] == t)
                            ].index[0],
                            col_name,
                        ] = ", ".join([str(i) for i in props[q][t]])

                    else:
                        df.loc[
                            df[
                                (df[assignment_col] == q)
                                & (df[time_utils.interval_to_col_name(interval)] == t)
                            ].index[0],
                            col_name,
                        ] = props[q][t]

    elif assign == "most_recent":  # interval and timespan are None
        # Assign the most recent value formatted with the date it's coming from
        for q in df[assignment_col].unique():
            if type(q) == str:  # is a valid location
                if len(props[q].keys()) == 1:
                    # Select the singular value even if it is 'no date'
                    assignment_times = list(props[q].keys())
                else:
                    # Select the documented times
                    assignment_times = sorted(
                        [k for k in props[q].keys() if k != "no date"]
                    )[::-1]

                if assignment_times == []:
                    # There were multiple 'no date' values, so select the first
                    assignment_times = list(list(props[q].keys())[0])

                most_recent_t = assignment_times[0]
                if type(props[q][most_recent_t]) == list:
                    # Multiple values to assign
                    if span:
                        # We don't want the time for most recent span values
                        df.loc[
                            df.loc[df[assignment_col] == q].index, col_name
                        ] = ", ".join([str(i) for i in props[q][most_recent_t]])

                    else:
                        df.loc[df.loc[df[assignment_col] == q].index, col_name] = (
                            ", ".join([str(i) for i in props[q][most_recent_t]])
                            + f" ({most_recent_t})"
                        )

                else:
                    if span:
                        # We don't want the time for most recent span values
                        df.loc[df.loc[df[assignment_col] == q].index, col_name] = props[
                            q
                        ][most_recent_t]

                    else:
                        df.loc[
                            df.loc[df[assignment_col] == q].index, col_name
                        ] = f"{props[q][most_recent_t]} ({most_recent_t})"

    elif assign == "repeat":
        # Assign one value over multiple rows
        for q in df[assignment_col].unique():
            if type(q) == str:  # is a valid location
                indexes_to_assign = df.loc[df[assignment_col] == q].index
                if type(props[q]) == list:
                    # Multiple values to assign
                    df.loc[indexes_to_assign, col_name] = [
                        ", ".join([str(i) for i in props[q]])
                    ] * len(indexes_to_assign)

                else:
                    df.loc[indexes_to_assign, col_name] = [props[q]] * len(
                        indexes_to_assign
                    )

    else:
        ValueError(
            "An invalid argument was passed to the 'assign' argument - please choose from one from "
            + ", ".join(valid_assigns)
        ) + "."

    df.replace(to_replace="nan", value=np.nan, inplace=True)
    # QID columns will be transferred for all properties, but all except one will be dropped
    df.rename(columns={assignment_col: "qid"}, inplace=True)

    return df


def gen_base_and_assign_to_column(
    locations=None,
    depth=None,
    timespan=None,
    interval=None,
    col_name="data",
    props=None,
    assign=None,
    span=False,
):
    """
    Combines data_utils.gen_base_df and data_utils.assign_to_column
    """
    df = gen_base_df(
        locations=locations,
        depth=depth,
        timespan=timespan,
        interval=interval,
        col_name=col_name,
    )

    df = assign_to_column(
        df=df,
        locations=locations,
        depth=depth,
        interval=interval,
        col_name=col_name,
        props=props,
        assign=assign,
        span=span,
    )

    return df


def assign_to_cols(
    df=None,
    locations=None,
    depth=None,
    sub_pid=None,
    interval=None,
    col_prefix="d",
    props=None,
    assign="all",
    span=False,
):
    """
    Assigns Wikidata property values from a qualifier to a designated column of a given df

    Parameters
    ----------
        df : pd.DataFrmae
            A df (likely base_df) to which values should be assigned

        locations : str, list, or lctn_utils.LocationsDict (contains strs) : optional (default=None)
            The locations to query

        depth : int (default=None)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        sub_pid : str (default=None)
            The Wikidata property that subsets time values

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        col_prefix : str (default=d)
            The prefix for columns that are a created from sub_prop values

        props : list or dict
            The properties to be assigned

        assign : str (default=all)
            The type of assignment

        span : bool (default=False)
            Whether to check for P580 'start time' and P582 'end time' to create spans

    Returns
    -------
        df : pd.DataFrame
            The df after assignment
    """
    valid_assigns = ["all", "most_recent"]

    if type(locations) == str:
        locations = [locations]

    if type(locations) == list:
        assert (
            depth == 0
        ), """The user has provided locations with depth 0, but the 'depth' argument is not 0.
        If a greater depth is required, use lctn_utils.gen_lctns_dict."""

    elif type(locations) == lctn_utils.LocationsDict:
        if depth != None:
            depth_check = lctn_utils.derive_depth(locations, depth=0)
            assert (
                depth_check == depth
            ), "The given depth and the derived depth of the LocationsDict do not match. Please check the geographic depth you want to analyze."

    # Column made up of QIDs for assignment
    assignment_col = lctn_utils.depth_to_qid_col_name(depth=depth)

    if assign == "all":
        # Assign a value over rows by matching times
        for q in df[assignment_col]:
            if type(q) == str:  # is a valid location
                for t in props[q].keys():
                    # props[q][t] is a dictionary qualified values
                    for k in props[q][t].keys():
                        sub_col = col_prefix + "_" + k.replace(" ", "_").lower()
                        if sub_col not in df.columns:
                            df[sub_col] = [np.nan] * len(df)

                        df.loc[
                            df[
                                (df[assignment_col] == q)
                                & (df[time_utils.interval_to_col_name(interval)] == t)
                            ].index[0],
                            sub_col,
                        ] = props[q][t][k]

    elif assign == "most_recent":  # interval and timespan are None
        # Assign the most recent value formatted with the date it's coming from
        for q in df[assignment_col]:
            if type(q) == str:  # is a valid location
                if len(props[q].keys()) == 1:
                    # Select the singular value even if it is 'no date'
                    assignment_times = list(props[q].keys())
                else:
                    # Select the documented times
                    assignment_times = sorted(
                        [k for k in props[q].keys() if k != "no date"]
                    )[::-1]

                if assignment_times == []:
                    # There were multiple 'no date' values, so select the first
                    assignment_times = list(list(props[q].keys())[0])

                most_recent_t = assignment_times[0]
                # props[q][most_recent_t] is a dictionary qualified values

                for k in props[q][most_recent_t].keys():
                    sub_col = col_prefix + "_" + k.replace(" ", "_").lower()
                    if sub_col not in df.columns:
                        df[sub_col] = [np.nan] * len(df)

                    if span == True and sub_pid == bool:
                        # We don't want the date if it's a spanned boolean value
                        df.loc[df[(df[assignment_col] == q)].index[0], sub_col] = props[
                            q
                        ][most_recent_t][k]

                    else:
                        df.loc[
                            df[(df[assignment_col] == q)].index[0], sub_col
                        ] = f"{props[q][most_recent_t][k]} ({most_recent_t})"

    else:
        ValueError(
            "An invalid argument was passed to the 'assign' argument - please choose from one from "
            + ", ".join(valid_assigns)
        ) + "."

    df.replace(to_replace="nan", value=np.nan, inplace=True)
    # QID columns will be transferred for all properties, but all except one will be dropped
    df.rename(columns={assignment_col: "qid"}, inplace=True)

    return df


def gen_base_and_assign_to_cols(
    locations=None,
    depth=None,
    sub_pid=None,
    timespan=None,
    interval=None,
    col_name=None,
    col_prefix="d",
    props=None,
    assign=None,
    span=False,
):
    """
    Combines data_utils.gen_base_df and data_utils.assign_to_cols
    """
    df = gen_base_df(
        locations=locations,
        depth=depth,
        timespan=timespan,
        interval=interval,
        col_name=None,
    )  # col_name is None to prevent a data col

    df = assign_to_cols(
        df=df,
        locations=locations,
        depth=depth,
        sub_pid=sub_pid,
        interval=interval,
        col_prefix=col_prefix,  # prefixed columns are instead assigned
        props=props,
        assign=assign,
        span=span,
    )

    return df


def query_wd_prop(
    dir_name=None,
    ents_dict=None,
    locations=None,
    depth=None,
    timespan=None,
    interval=None,
    pid=None,
    sub_pid=None,
    col_name=None,
    col_prefix=None,
    ignore_char="",
    span=False,
):
    """
    Queries a Wikidata property for the given continent(s)

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        ents_dict : wd_utils.EntitiesDict : optional (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        locations : str, list, or lctn_utils.LocationsDict (contains strs) : optional (default=None)
            The locations to query

        depth : int (default=None)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        pid : str (default=None)
            The Wikidata property that is being queried

        sub_pid : str (default=None)
            The Wikidata property that subsets time values

        col_name : str (default=None)
            The name of the column into which queried data should be merged

        col_prefix : str (default=None)
            The prefix for columns that are a created from sub_pid values
            Note: only use col_name or col_prefix

        ignore_char : str
            Characters in the output that should be ignored

        span : bool (default=False)
            Whether to check for P580 'start time' and P582 'end time' to create spans

    Returns
    -------
        df, ents_dict : pd.DataFrame, wd_utils.EntitiesDict
            A df of location names and the given property for the given timespan with an updated EntitiesDict
    """
    if ents_dict == None:
        ents_dict = wd_utils.EntitiesDict()

    if type(locations) == str:
        locations = [locations]

    if type(locations) == list:
        qids = [
            lctn_utils.lctn_lbl_to_qid(lctn) if not wd_utils.is_wd_id(lctn) else lctn
            for lctn in locations
        ]

    elif type(locations) == lctn_utils.LocationsDict:
        qids = locations.get_keys_at_depth(depth)

    elif type(locations) == dict:
        qids = lctn_utils.get_qids_at_depth(lctns_dict=locations, depth=depth)
    qids = utils._make_var_list(qids)[0]

    if col_prefix == None:
        t_to_p_dict = wd_utils.t_to_prop_val_dict(
            dir_name=dir_name,
            ents_dict=ents_dict,
            qids=qids,
            pid=pid,
            sub_pid=sub_pid,
            timespan=timespan,
            interval=interval,
            ignore_char=ignore_char,
            span=span,
        )

        # Assignment via a single column col_name
        if interval is not None:
            df = gen_base_and_assign_to_column(
                locations=locations,
                depth=depth,
                timespan=timespan,
                interval=interval,
                col_name=col_name,
                props=t_to_p_dict,
                assign="all",
                span=span,
            )

        else:
            df = gen_base_and_assign_to_column(
                locations=locations,
                depth=depth,
                timespan=timespan,
                interval=interval,
                col_name=col_name,
                props=t_to_p_dict,
                assign="most_recent",
                span=span,
            )  # to remove the time from span props

    else:
        t_to_p_dict = wd_utils.t_to_prop_val_dict_dict(
            dir_name=dir_name,
            ents_dict=ents_dict,
            qids=qids,
            pid=pid,
            sub_pid=sub_pid,
            timespan=timespan,
            interval=interval,
            ignore_char=ignore_char,
            span=span,
        )

        # Assignment via generated columns prefixed as col_prefix
        if interval is not None:
            df = gen_base_and_assign_to_cols(
                locations=locations,
                depth=depth,
                sub_pid=sub_pid,
                timespan=timespan,
                interval=interval,
                col_name=col_name,  # col_name is None to disable single column
                col_prefix=col_prefix,
                props=t_to_p_dict,
                assign="all",
                span=span,
            )

        else:
            df = gen_base_and_assign_to_cols(
                locations=locations,
                depth=depth,
                sub_pid=sub_pid,
                timespan=timespan,
                interval=interval,
                col_name=col_name,  # col_name is None to disable single column
                col_prefix=col_prefix,
                props=t_to_p_dict,
                assign="most_recent",
                span=span,
            )  # to remove the time from boolean span props

    return df, ents_dict


def query_repo_dir(
    dir_name=None,
    ents_dict=None,
    locations=None,
    depth=None,
    timespan=None,
    interval=None,
    verbose=True,
    **kwargs,
):
    """
    Generates a df of statistics for given a psk directory and geographic as well as time intervals

    Parameters
    ----------
        dir_name : str (default=None)
            The name of the directory within wikirepo.data

        ents_dict : wd_utils.EntitiesDict : optional (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        locations : str, list, or lctn_utils.LocationsDict (contains strs) : optional (default=None)
            The locations to query

        depth : int (default=None)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

        verbose : bool (default=True)
            Whether to show a tqdm progress bar for the query

    Returns
    -------
        df_data : pd.DataFrame
            A df of locations and data given timespan and demographic index arguments
    """
    local_args = locals()
    _check_data_assertions(**literal_eval(str(local_args)))

    modules_to_query = [
        arg
        for arg in list(local_args["kwargs"].keys())
        if arg in incl_dir_idxs(dir_name)
        and local_args["kwargs"].get(arg, False) == True
    ]

    df_data = None
    disable = not verbose
    for mod in tqdm(modules_to_query, desc=dir_name.capitalize(), disable=disable):
        module_fxns = _get_dir_fxns_dict(dir_name)[mod]
        query_fxn = [
            f for f in list(module_fxns.keys()) if f[: len("query_")] == "query_"
        ][
            0
        ]  # there can only be one per module

        if df_data is None:
            df_data, ents_dict = module_fxns[query_fxn](
                dir_name=dir_name,
                ents_dict=ents_dict,
                locations=locations,
                depth=depth,
                timespan=timespan,
                interval=interval,
            )

        else:
            if interval:
                merge_on = lctn_utils.depth_to_cols(depth) + [
                    time_utils.interval_to_col_name(interval)
                ]
            else:
                merge_on = lctn_utils.depth_to_cols(depth)

            df_props, ents_dict = module_fxns[query_fxn](
                dir_name=dir_name,
                ents_dict=ents_dict,
                locations=locations,
                depth=depth,
                timespan=timespan,
                interval=interval,
            )

            df_data = pd.merge(df_data, df_props, on=merge_on)

    return df_data, ents_dict


def interp_by_subset(df=None, depth=None, col_name="data", **kwargs):
    """
    Subsets a df by a given geo_lvl and interpolates the given column

    Note: pd.DataFrame.interpolate and scipy.interpolate **kwargs are passed

    Parameters
    ----------
        df : pd.DataFrame (default=None)
            A dataframe to have a column interpolated

        depth : int (default=None)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        col_name : str
            A column in df that is to be interpolated

    Returns
    -------
        df_interpolated : pd.DataFrame
            The original df with the given column interpolated based on **kwargs
    """
    df_interpolated = pd.DataFrame()

    unique_lctns = list(df[lctn_utils.depth_to_col_name(depth)].unique())

    if (
        "method" in kwargs.keys()
        and "limit_direction" in kwargs.keys()
        and kwargs["method"] == "pad"
        and kwargs["limit_direction"] == "both"
    ):
        for lctn in unique_lctns:
            df_subset = df[df[lctn_utils.depth_to_col_name(depth)] == lctn].copy()
            unique_val = [
                val
                for val in df_subset[col_name].unique()
                if not (type(val) != str and np.isnan(val))
            ][0]
            df_subset[col_name] = [unique_val] * len(df_subset)

            df_interpolated = df_interpolated.append(df_subset)

    else:
        for lctn in unique_lctns:
            df_subset = df[df[lctn_utils.depth_to_col_name(depth)] == lctn].copy()
            df_subset.loc[:, col_name].interpolate(inplace=True, **kwargs)

            df_interpolated = df_interpolated.append(df_subset)

    return df_interpolated


def sum_df_prop_vals(
    df=None,
    target_lctn=None,
    vals_lctn=None,
    lctn_col=None,
    time_col=None,
    prop_col=None,
    subtract=False,
    drop_vals_lctn=False,
):
    """
    Adds or subtracts values in a dataframe for given locations

    Parameters
    ----------
        df : pd.DataFrame (default=None)
            A dataframe with property rows to be summed

        target_lctn : str (default=None)
            The name of the location to which values should be added
            Note: subtract=True subtracts from this location

        vals_lctn : str (default=None)
            The name of the location that has values to be added or subtracted

        lctn_col : str (default=None)
            The name of the column in which the locations are defined

        time_col : str (default=None)
            The name of the column in which times are defined

        prop_col : str (default=None)
            The name of the column in which property values are found

        subtract : bool (default=False)
            Whether values from vals_lctn should be subtracted from target_lctn

        drop_vals_lctn : bool (default=False)
            Whether rows with vals_lctn should be dropped from df

    Returns
    -------
        df_new : pd.DataFrame
            The dataframe post arithmetic operations
    """
    df_new = df.copy()

    if time_col:
        for t in df_new[time_col].unique():
            if subtract:
                df_new.loc[
                    df_new[
                        (df_new[lctn_col] == target_lctn) & (df_new[time_col] == t)
                    ].index,
                    prop_col,
                ] = (
                    df_new.loc[
                        df_new[
                            (df_new[lctn_col] == target_lctn) & (df_new[time_col] == t)
                        ].index,
                        prop_col,
                    ].values[0]
                    - df_new.loc[
                        df_new[
                            (df_new[lctn_col] == vals_lctn) & (df_new[time_col] == t)
                        ].index,
                        prop_col,
                    ].values[0]
                )

            else:
                df_new.loc[
                    df_new[
                        (df_new[lctn_col] == target_lctn) & (df_new[time_col] == t)
                    ].index,
                    prop_col,
                ] = (
                    df_new.loc[
                        df_new[
                            (df_new[lctn_col] == target_lctn) & (df_new[time_col] == t)
                        ].index,
                        prop_col,
                    ].values[0]
                    + df_new.loc[
                        df_new[
                            (df_new[lctn_col] == vals_lctn) & (df_new[time_col] == t)
                        ].index,
                        prop_col,
                    ].values[0]
                )

    else:
        if subtract:
            df_new.loc[df_new[df_new[lctn_col] == target_lctn].index, prop_col] = (
                df_new.loc[
                    df_new[df_new[lctn_col] == target_lctn].index, prop_col
                ].values[0]
                - df_new.loc[
                    df_new[df_new[lctn_col] == vals_lctn].index, prop_col
                ].values[0]
            )

        else:
            df_new.loc[df_new[df_new[lctn_col] == target_lctn].index, prop_col] = (
                df_new.loc[
                    df_new[df_new[lctn_col] == target_lctn].index, prop_col
                ].values[0]
                + df_new.loc[
                    df_new[df_new[lctn_col] == vals_lctn].index, prop_col
                ].values[0]
            )

    if drop_vals_lctn:
        df_new = df_new[df_new[lctn_col] != vals_lctn]

    return df_new


def split_col_val_dates(df=None, col=None):
    """
    Adds or subtracts values in a dataframe for given locations

    Parameters
    ----------
        df : pd.DataFrame (default=None)
            A dataframe with property rows to be summed

        col : str (default=None)
            The name of the column which should have its dates split to another column

    Returns
    -------
        df_new : pd.DataFrame
            The dataframe post splitting the date from the values
    """
    df_new = df.copy()

    col_index = df_new.columns.get_loc(col)
    df_new[f"{col}_date"] = [
        val.split(" (")[1] if val != np.nan else np.nan for val in df_new[col]
    ]
    df_new[col] = [
        val.split(" (")[0] if val != np.nan else np.nan for val in df_new[col]
    ]

    df_new[f"{col}_date"] = [
        d.replace(")", "") if d != np.nan else np.nan for d in df_new[f"{col}_date"]
    ]
    df_new[col] = [utils.round_if_int(utils.try_float(val)) for val in df_new[col]]

    cols = list(df_new.columns)
    cols.pop(df_new.columns.get_loc(f"{col}_date"))
    cols.insert(col_index + 1, f"{col}_date")

    df_new = df_new[cols]

    return df_new


def count_df_prop_vals(df=None, col=None, percent=False):
    """
    Returns value counts of df columns sorted alphabetically

    Parameters
    ----------
        df : pd.DataFrame (default=None)
            Regional data including population size

        col : str (default=None)
            The column in df in which counts should be made

        percent : bool (default=False)
            Whether to return percentage values

    Returns
    -------
        val_counts or pd.value_counts : dict or pd.value_counts
            Aggregate or percentage value counts
    """
    assert col in [s for s in df.columns], f"{col} is not a column in the data."

    if percent:
        return df[col].value_counts().sort_index() / len(df)
    else:
        return df[col].value_counts().sort_index()
