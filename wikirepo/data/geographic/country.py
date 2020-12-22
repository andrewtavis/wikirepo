"""
Functions querying 'P17' (country) information

Contents
--------
  0. No Class
      query_prop_data
"""

from wikirepo.data import data_utils, lctn_utils

pid = "P17"
sub_pid = None
col_name = "country"
col_prefix = None
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

    fixes = [
        ["Aruba", "Netherlands"],  # Territory
        ["Abkhazia", "Georgia"],  # Recognized by most states as a part of Georgia
        ["Denmark", "Denmark"],  # Fix
        ["Ghana", "Ghana"],  # Fix
        ["Guinea-Bissau", "Guinea-Bissau"],  # Fix
        ["Guernsey", "United Kingdom"],  # Territory
        ["Jersey", "United Kingdom"],  # Territory
        ["Nauru", "Nauru"],  # Fix
        [
            "Republic of Artsakh",
            "Azerbaijan",
        ],  # Recognized by most states as a part of Azerbaijan
        ["Sri Lanka", "Sri Lanka"],  # Fix
        ["South Ossetia", "Georgia"],  # Recognized by most states as a part of Georgia
        ["Transnistria", "Moldova"],  # Recognized by most states as a part of Moldova
        [
            "Turkish Republic of Northern Cyprus",
            "Cyprus",
        ],  # Recognized by most states as a part of Cyprus
        ["Western Sahara", "Morocco"],
    ]  # 80% is controlled by Morocco

    for f in fixes:
        if f[0] in list(df[lctn_utils.depth_to_col_name(depth)]):
            df.loc[
                df.loc[df[lctn_utils.depth_to_col_name(depth)] == f[0]].index, col_name
            ] = f[1]

    df[col_name] = df[col_name].replace("Kingdom of the Netherlands", "Netherlands")
    df[col_name] = df[col_name].replace("Kingdom of Denmark", "Denmark")
    df[col_name] = df[col_name].replace("Danish Realm", "Denmark")

    return df, ents_dict
