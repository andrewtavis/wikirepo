"""
Functions querying 'P172' (ethnic group) information

This is done by querying 'P1107' (proportion) from each 'P172'

Contents
--------
  0. No Class
      query_prop_data
"""

from wikirepo.data import data_utils

pid = "P172"
sub_pid = "P1107"
col_name = None  # col_name is None for no data col
col_prefix = "eth"  # columns will be generated and prefixed from values
ignore_char = ""
span = False


def query_prop_data(
    dir_name=None, ents_dict=None, locations=None, depth=0, timespan=None, interval=None
):
    """
    Queries data for the module property for given location(s), depth, timespan and interval
    """
    df, ents_dict = data_utils.query_wd_prop(
        dir_name=dir_name,
        ents_dict=ents_dict,
        locations=locations,
        depth=depth,
        timespan=timespan,
        interval=interval,
        pid=pid,
        sub_pid=sub_pid,
        col_name=col_name,
        col_prefix=col_prefix,
        ignore_char=ignore_char,
        span=span,
    )

    return df, ents_dict
