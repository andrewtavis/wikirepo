"""
Functions querying 'PXYZ' (freedom house category) information

This is done via 'P1552' (has quality) applied to regions
Idealy a property would be created for this that would allow it to be traced over time

Contents
--------
  0. No Class
      query_prop_data
"""

from wikirepo.data import data_utils

pid = "P1552"
sub_pid = None
col_name = "fh_category"
col_prefix = None
ignore_char = " country"
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
