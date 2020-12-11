# =============================================================================
# A function that calls and cobmines data from Wikidata
#
# Note: the purpose of this module is for a wikirepo.data.query() function call
#
# Contents
# --------
#   0. No Class
#       query
# =============================================================================

from ast import literal_eval

import pandas as pd
from tqdm.auto import tqdm

from wikirepo import utils
from wikirepo.data import data_utils, lctn_utils, time_utils, wd_utils

def query(ents_dict=None, 
          depth=None, 
          locations=None, 
          time_lvl=None, 
          timespan=None,
          climate_props=False,
          demographic_props=False, 
          economic_props=False, 
          electoral_poll_props=False,
          electoral_result_props=False, 
          geographic_props=False, 
          institutional_props=False,
          political_props=False,
          misc_props=False,
        #   multicore=True,
          verbose=True):
    """
    Queries Wikidata properties based on module arguments for locations given a depth, time_lvl, and timespan
        
    Parameters
    ----------
        ents_dict : wd_utils.EntitiesDict : optional (default=None)
            A dictionary with keys being Wikidata QIDs and values being their entities

        depth : int (default=0, no sub_locations)
            The depth from the given lbls or qids that data should go
            Note: this uses 'P150' (contains administrative territorial entity)

        locations : str, list, or lctn_utils.LocationsDict (contains strs) : optional (default=None)
            The locations to query either as strings for indexed locations or Wikidata QIDs

        time_lvl : str
            The time level over which queries will be made
            Note: see data.query_time for options

        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if None, then only the most recent data for the time_lvl will be queried
            Note 2: if True, then the full timespan from 1-1-1 to the current day will be queried 
            Note 3: passing a single entry will query for that date only

        climate_props : str or list (contains strs) : optional (default=False)
            String representations of data/climate modules for data_utils.query_repo_dir

        demographic_props : str or list (contains strs) : optional (default=False)
            String representations of data/demographic modules for data_utils.query_repo_dir

        economic_props : str or list (contains strs) : optional (default=False)
            String representations of data/economic modules for data_utils.query_repo_dir

        electoral_poll_props : str or list (contains strs) : optional (default=False)
            String representations of data/electoral_polls modules for data_utils.query_repo_dir

        electoral_result_props : str or list (contains strs) : optional (default=False)
            String representations of data/electoral_results modules for data_utils.query_repo_dir

        geographic_props : str or list (contains strs) : optional (default=False)
            String representations of data/geographic modules for data_utils.query_repo_dir

        institutional_props : str or list (contains strs) : optional (default=False)
            String representations of data/institutional modules for data_utils.query_repo_dir

        political_props : str or list (contains strs) : optional (default=False)
            String representations of data/political modules for data_utils.query_repo_dir

        misc_props : str or list (contains strs) : optional (default=False)
            String representations of data/misc (miscellaneous) modules for data_utils.query_repo_dir

        verbose : bool (default=True)
            Whether to show a tqdm progress bar for the query
            Note: passing 'full' calls progress bars for each data_utils.query_repo_dir

        Potential later arguments:
            multicore : bool or int (default=False)
                Whether to make use of multiple processes and threads, and how many to use
                Note: True uses all available

            source : bool (default=False)
                Whether to add columns for sources for all data

    Returns
    -------
        df_merge : pd.DataFrame
            A df of locations and data given timespan and data source arguments
    """
    local_args = locals()

    # Baseline args that do not have imbedded lower level functional arguments
    # These are passed directly
    baseline_args = ['ents_dict', 'depth', 'locations', 
                     'time_lvl', 'timespan', 'verbose']
    
    if type(locations) == lctn_utils.LocationsDict:
        if depth == None:
            depth = locations.get_depth()
        # if time_lvl == None:
        #     time_lvl = locations.get_time_lvl()
        # if timespan == None:
        #     timespan = locations.get_timespan()

    query_args = [arg for arg in local_args.keys() \
                    if (arg not in baseline_args) and (local_args[arg] != False \
                                                        and local_args[arg] != None)]

    # Initialize a merge df, a dictionary of parameters, and an entities dictionary
    df_merge = None
    query_params = {}
    if ents_dict == None:
        ents_dict = wd_utils.EntitiesDict()

    if type(locations) == str:
        locations = [locations]
    
    disable = not verbose
    for arg in tqdm(query_args, desc='Directories queried', unit='dir', disable=disable):
        sub_directory = arg[:-len('_props')]
        
        if sub_directory == 'electoral_poll' or sub_directory == 'electoral_result':
            sub_directory += 's'
        
        query_params['dir_name'] = sub_directory
        query_params['depth'] = depth
        if type(locations) == lctn_utils.LocationsDict:
            query_params['locations'] = literal_eval(str(locations._print()))
        else:
            query_params['locations'] = locations
        query_params['ents_dict'] = literal_eval(str(ents_dict._print()))
        query_params['time_lvl'] = time_lvl
        
        # The following is necessary for passing tuples with datetime.date objects to literal_evel
        # Convert to a tuple of tuples, and then back again in the lower fxns via time_utils.make_timespan() in data_utils.gen_base_df()
        timespan = f"{timespan}".replace('datetime.date', '')
        timespan = literal_eval(timespan)
        query_params['timespan'] = timespan

        if verbose == 'full':
            query_params['verbose'] = True
        elif verbose == True:
            query_params['verbose'] = False
        else:
            query_params['verbose'] = False
        
        # Included indexes for the given data type
        incl_indexes = data_utils.incl_dir_idxs(dir_name=sub_directory)
        
        # Assigning True for the specific data indexes to be queried, which is passed to data_utils.query_repo_dir
        query_arg_indexes = local_args[arg]
        if query_arg_indexes == True:
            for i in incl_indexes:
                query_params[i] = True

        else:
            if type(query_arg_indexes) == str:
                query_arg_indexes = [query_arg_indexes]
            for i in query_arg_indexes:
                if i in incl_indexes:
                    query_params[i] = True
                else:
                    utils.check_str_args(arguments=i, valid_args=incl_indexes)

        # Pass the created dictionary as kwargs for data_utils.query_repo_dir
        if df_merge is not None:
            # geo cols are queried as a list, and time as a string
            if time_lvl is not None:
                merge_on = lctn_utils.depth_to_cols(depth=depth) + \
                    [time_utils.t_lvl_to_col_name(time_lvl=time_lvl)]
            else:
                merge_on = lctn_utils.depth_to_cols(depth=depth)
            
            df_dir_props, new_ents_dict = data_utils.query_repo_dir(**literal_eval(str(query_params)))

            try:
                df_merge = pd.merge(df_merge, df_dir_props, on=merge_on)
            except:
                pass

        else:
            df_merge, new_ents_dict = data_utils.query_repo_dir(**literal_eval(str(query_params)))

        for i in incl_indexes:
            query_params.pop(i, None)

        for k in new_ents_dict.keys():
            if k not in ents_dict.keys():
                ents_dict[k] = new_ents_dict[k]
    
    # Reduce QID columns to just one directly after the last locations column
    qid_cols = [col for col in list(df_merge.columns) if col[:len('qid')] == 'qid']
    first_qid_col = qid_cols[0]
    df_merge.rename(columns={first_qid_col: 'keep_this_col'}, inplace=True)
    df_merge = df_merge.loc[:,~df_merge.columns.duplicated()] # qid columns can be named the same
    qid_cols = [col for col in list(df_merge.columns) if col[:len('qid')] == 'qid']
    for col in list(set(qid_cols)):
        df_merge.drop(col, axis=1, inplace=True)

    df_merge.rename(columns={'keep_this_col': 'qid'}, inplace=True)

    return df_merge