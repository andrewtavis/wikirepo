"""
Functions querying organizational information

This is done via 'P463' (member of) applied to locations

Contents
--------
  0. No Class
      query_prop_data
"""

from wikirepo.data import data_utils

pid = "P463"
sub_pid = bool  # assign boolean values
col_name = None  # col_name is None for no data col
col_prefix = "mem"  # columns will be generated and prefixed from values
ignore_char = ""
span = True


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

    org_renames = [
        ("mem_world_trade_organization", "mem_wto"),
        ("mem_european_union", "mem_eu"),
        ("mem_organisation_for_economic_cooperation_and_development", "mem_oecd"),
        ("mem_united_nations", "mem_un"),
        ("mem_world_health_organization", "mem_who"),
        ("mem_international_monetary_fund", "mem_imf"),
    ]

    for o_r in org_renames:
        if o_r[0] in df.columns:
            df.rename(columns={o_r[0]: o_r[1]}, inplace=True)

    df.fillna(value=False, inplace=True)

    return df, ents_dict
