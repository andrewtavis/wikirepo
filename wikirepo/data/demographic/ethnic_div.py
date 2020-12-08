# =============================================================================
# Functions querying 'P172' (ethnic group) information
#
# This is done by querying 'P1107' (proportion) from each 'P172'
#
# Contents
# --------
#   0. No Class
#       query_prop_data
# =============================================================================

from wikirepo.data import data_utils

pid = 'P172'
sub_pid = 'P1107'
col_name = None # col_name is None for no data col
col_prefix = 'eth' # columns will be generated and prefixed from values
ignore_char = ''
span = False

def query_prop_data(dir_name=None,
                    ents_dict=None,
                    depth=0,
                    locations=None, 
                    time_lvl=None, 
                    timespan=None):
    """
    Queries data for the module property for given region(s) over given depth, time_lvl and timespan
    """
    df, ents_dict = data_utils.query_wd_prop(dir_name=dir_name,
                                             ents_dict=ents_dict,
                                             depth=depth,
                                             locations=locations, 
                                             time_lvl=time_lvl, 
                                             timespan=timespan,
                                             pid=pid,
                                             sub_pid=sub_pid,
                                             col_name=col_name,
                                             col_prefix=col_prefix,
                                             ignore_char=ignore_char,
                                             span=span)

    return df, ents_dict